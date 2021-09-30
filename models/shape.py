from pydantic import BaseModel, validator
from typing import Optional
from .material import Material
import math

class Shape(BaseModel):
    shape_type: str = None
    

class Cylinder(Shape):
    ## User Input
    height:   float # cm
    shape_type = "cylinder"

    ## Can Be Input If Needed
    diameter: Optional[float] = None # cm


    ## Automatically Generated
    sa_circle: Optional[float] = None # cm^2
    volume:    Optional[float] = None # cm^3
    
    @validator("diameter", always=True)
    def validate_diameter(cls, v, values) -> float:
        try:
            if not values["diameter"]:
                raise Exception
        except:
            values["diameter"] = 10
        return values["diameter"]
            
    @validator("sa_circle", always=True)
    def calc_sa_circle(cls, v, values) -> float:
        return values["diameter"] * math.pi

    @validator("volume", always=True)
    def calc_volume(cls, v, values) -> float:
        return values["sa_circle"] * values["height"]

    def __str__(self):

        return f"""
        -------------------------
        Diameter:  {self.diameter} (cm)
        Height:    {self.height} (cm)
        SA Circle: {self.sa_circle} (cm^2)
        Volume:    {self.volume} (cm^3)
        -------------------------
        """

