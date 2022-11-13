from pydantic import BaseModel


class Address(BaseModel):
    title: str
    pincode: str
    state: str
    fullAddress: str
    coordinates: str
    publishedBy: str
