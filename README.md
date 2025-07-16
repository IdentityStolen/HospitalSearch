# HospitalSearch

## Prerequisites

Create API_NINJAS_KEY in the `.env` file with your API key from [API Ninjas](https://api-ninjas.com/).


Endpoints:

http://127.0.0.1:8000/api/extract_data/?city=chandler&state=az
http://127.0.0.1:8000/api/transform_data


Start Temporal server:

```bash
temporal server start-dev --namespace Conversion    

