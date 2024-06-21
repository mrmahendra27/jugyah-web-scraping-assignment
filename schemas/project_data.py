from pydantic import BaseModel

class ProjectData(BaseModel):
    title: str
    url: str
    bhk_units: str
    launch_date: str
    property_cost_range: list
    description: str
    map_location: dict
    locality_guide: dict
    amenities: list
    seller_contacts: list