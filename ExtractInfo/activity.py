from ExtractInfo.converter_utils import (
    StringConverter,
    PhoneConverter,
    TimezoneConverter,
    FloatConverter,
    IntConverter,
    NotNullConverter,
)

from temporalio import activity


@activity.defn
def transform_data_helper(hospital):
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
