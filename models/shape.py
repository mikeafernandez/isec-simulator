from pydantic import BaseModel, validator
from typing import Optional
from .material import Material
import math

class Cylinder(BaseModel):
    ## User Input
    diameter: float # cm
    height:   float # cm
    material: Material # What is it made of?

    ## Automatically Generated
    sa_circle: Optional[float] = None # cm^2
    volume:    Optional[float] = None # cm^3
    mass:      Optional[float] = None # g
    

    @validator("sa_circle", always=True)
    def calc_sa_circle(cls, v, values) -> float:
        return values["diameter"] * math.pi

    @validator("volume", always=True)
    def calc_volume(cls, v, values) -> float:
        return values["sa_circle"] * values["height"]
    
    @validator("mass", always=True)
    def calc_mass(cls, v, values) -> float:
        return values["volume"] * values["material"].density

    def __str__(self):

        return f"""
        -------------------------
        Diameter:  {self.diameter} (cm)
        Height:    {self.height} (cm)
        Material:  {self.material.name}
        SA Circle: {self.sa_circle} (cm^2)
        Volume:    {self.volume} (cm^3)
        Mass:      {self.mass} (g)
        -------------------------
        """

