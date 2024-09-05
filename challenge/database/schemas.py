from datetime import datetime

from pydantic import BaseModel

from challenge.database.models.visibility import Visibility


class IssPosition(BaseModel):
    """
    IssPosition schema
    """
    name: str
    satellite_id: int
    latitude: float
    longitude: float
    altitude: float
    velocity: float
    visibility: Visibility
    footprint: float
    timestamp: datetime
    daynum: float
    solar_lat: float
    solar_lon: float
    units: str

    @classmethod
    def from_json(cls, json: dict):
        return IssPosition(name=json['name'], satellite_id=json['id'], latitude=json['latitude'],
                           longitude=json['longitude'], altitude=json['altitude'],
                           velocity=json['velocity'], visibility=Visibility(json['visibility']), footprint=json['footprint'],
                           timestamp=datetime.fromtimestamp(json['timestamp']), daynum=json['daynum'],
                           solar_lat=json['solar_lat'], solar_lon=json['solar_lon'], units=json['units'])

    class Config:
        from_attributes = True
