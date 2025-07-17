import asyncio
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from dotenv import load_dotenv
import json

from temporalio.client import Client
import uuid

load_dotenv()


# Use of a file mimics the streaming incremental data
FILE_PATH = "./hospitals.json"


@csrf_exempt
def extract_data(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    city = request.GET.get("city")
    state = request.GET.get("state")

    if len(state) != 2 or not state.isalpha():
        return JsonResponse({"error": "state must be exactly 2 letters"}, status=400)

    api_key = os.environ.get("API_NINJAS_KEY")

    if not api_key:
        return JsonResponse({"error": "API key not set"}, status=500)
    url = f"https://api.api-ninjas.com/v1/hospitals?city={city}&state={state}"
    headers = {"X-Api-Key": api_key}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        hospitals = resp.json()

        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(hospitals, f, ensure_ascii=False, indent=2)

        return JsonResponse(hospitals, safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


output = []


async def process_hospital(client, hospital):
    result = await client.execute_workflow(
        "ConversionWorkflow",
        hospital,
        id=str(uuid.uuid4()),
        task_queue="conversion-queue",
    )

    output.append(result)
    return result


async def process_hospitals(hospitals):
    client = await Client.connect("host.docker.internal:7233", namespace="Conversion")

    results = []

    tasks = [
        asyncio.create_task(process_hospital(client, hospital))
        for hospital in hospitals
    ]

    for task in asyncio.as_completed(tasks):
        result = await task
        results.append(result)

    return results


@csrf_exempt
def transform_data(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)

    responses = []

    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                hospitals = json.load(f)
                responses = asyncio.run(process_hospitals(hospitals))
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

        responses = responses if len(responses) == len(output) else output
        return JsonResponse(responses, safe=False)
