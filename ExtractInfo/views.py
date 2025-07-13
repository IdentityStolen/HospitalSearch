from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.

@csrf_exempt
def search_hospitals(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed'}, status=405)
    city = request.GET.get('city')
    state = request.GET.get('state')
    if not city or not state:
        return JsonResponse({'error': 'city and state are required'}, status=400)
    if len(state) != 2 or not state.isalpha():
        return JsonResponse({'error': 'state must be exactly 2 letters'}, status=400)
    api_key = os.environ.get('API_NINJAS_KEY')
    if not api_key:
        return JsonResponse({'error': 'API key not set'}, status=500)
    url = f'https://api.api-ninjas.com/v1/hospitals?city={city}&state={state}'
    headers = {'X-Api-Key': api_key}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return JsonResponse(resp.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
