from ExtractInfo.converter_utils import (
    StringConverter,
    PhoneConverter,
    TimezoneConverter,
    FloatConverter,
    IntConverter,
    NotNullConverter,
    WebsiteConverter,
)
from typing import Dict
from temporalio import activity


conversion_strategy = {
    "name": StringConverter,
    "care_type": StringConverter,
    "address": StringConverter,
    "phone_number": PhoneConverter,
    "city": StringConverter,
    "state": StringConverter,
    "zipcode": StringConverter,
    "county": StringConverter,
    "location_area_code": StringConverter,
    "fips_code": StringConverter,
    "timezone": TimezoneConverter,
    "latitude": FloatConverter,
    "longitude": FloatConverter,
    "ownership": StringConverter,
    "bedcount": lambda x: NotNullConverter(IntConverter(x)),
    "website": WebsiteConverter,
}


@activity.defn
def transform_data_helper(hospital: Dict):
    cleaned_data = {}

    for k, v in hospital.items():
        converter_obj = conversion_strategy[k]
        cleaned_data[k] = converter_obj(v).convert()

    return cleaned_data
