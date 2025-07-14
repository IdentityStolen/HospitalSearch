from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from dotenv import load_dotenv
import json

from ExtractInfo.converter_utils import (
    StringConverter,
    PhoneConverter,
    TimezoneConverter,
    FloatConverter,
    IntConverter,
    NotNullConverter,
)

load_dotenv()


# Use of a file mimics the streaming incremental data
FILE_PATH = "./hospitals.json"


@csrf_exempt
def extract_data(request):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=405)
    city = request.GET.get("city")
    state = request.GET.get("state")
    # if not city or not state:
    #     return JsonResponse({'error': 'city and state are required'}, status=400)
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

        # Write hospitals to a local file
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(hospitals, f, ensure_ascii=False, indent=2)

        return JsonResponse(hospitals, safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def trasform_data_helper(hospital):
    cleaned_data = {}

    name = hospital.get("name", "")
    cleaned_data["name"] = StringConverter(name).convert()

    care_type = hospital.get("care_type", "")
    cleaned_data["care_type"] = StringConverter(care_type).convert()

    address = hospital.get("address", "")
    cleaned_data["address"] = StringConverter(address).convert()

    phone = hospital.get("phone_number", "")
    cleaned_data["phone"] = PhoneConverter(phone).convert()

    city = hospital.get("city", "")
    cleaned_data["city"] = StringConverter(city).convert()

    state = hospital.get("state", "")
    cleaned_data["state"] = StringConverter(state).convert()

    zipcode = hospital.get("zipcode", "")
    cleaned_data["zipcode"] = StringConverter(zipcode).convert()

    county = hospital.get("county", "")
    cleaned_data["county"] = StringConverter(county).convert()

    location_area_code = hospital.get("location_area_code", "")
    cleaned_data["location_area_code"] = StringConverter(location_area_code).convert()

    fips_code = hospital.get("fips_code", "")
    cleaned_data["fips_code"] = StringConverter(fips_code).convert()

    timezone = hospital.get("timezone", "")
    cleaned_data["timezone"] = TimezoneConverter(timezone).convert()

    latitude = hospital.get("latitude", "")
    cleaned_data["latitude"] = FloatConverter(latitude).convert()

    longitude = hospital.get("longitude", "")
    cleaned_data["longitude"] = FloatConverter(longitude).convert()

    ownership = hospital.get("ownership", "")
    cleaned_data["ownership"] = StringConverter(ownership).convert()

    bedcount = hospital.get("bedcount", "")
    cleaned_data["bedcount"] = NotNullConverter(IntConverter(bedcount)).convert()

    return cleaned_data


@csrf_exempt
def transform_data(request):
    responses = []

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            hospitals = json.load(f)
            for hospital in hospitals:
                responses.append(trasform_data_helper(hospital))
        os.remove(FILE_PATH)

    return JsonResponse(responses, safe=False)
