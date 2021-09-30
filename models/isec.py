from pydantic import BaseModel, validator
from typing import Optional, List
from models.shape import Shape, Cylinder
from models.material import Material
from core.thermal import get_flux
from enum import Enum

class LayerType(str, Enum):
    storage = 'thermal storage'
    source = 'source'
    sink = 'sink'

class ISECLayer(BaseModel):
    shape: Shape
    material: Material
    layer_type: LayerType
    mass: Optional[float] = None
    temperature: float = 20 # C
    heat_flux: float = 0 # W

    @validator("mass", always=True)
    def calc_mass(cls, v, values) -> float:
        return values["shape"].volume * values["material"].density

    @classmethod
    def update_heat_flux(cls, below, above) -> None:
        total_flux = 0
        if below:
            total_flux += get_flux(cls.material.thermal_conductivity, cls.shape.sa_circle, (cls.shape.height + below.height) / 2, below.temperature, cls.temperature)
        if above:
            total_flux += get_flux(cls.material.thermal_conductivity, cls.shape.sa_circle, (cls.shape.height + above.height) / 2, cls.temperature, below.temperature)
        
        cls.heat_flux = total_flux

    @classmethod
    def update_temp(cls, time_step: float) -> None:
        cls.temperature += (cls.heat_flux * time_step) / (cls.mass * cls.material.specific_heat)
        
        

class SourceLayer(ISECLayer):
    power: float # Watts
    layer_type = LayerType.source

    @validator("super-check", check_fields=False, always=True)
    def call_super(cls, v, values) -> None:
        super(SourceLayer, cls).__init__()

    @validator("layer_type", always=True)
    def validate_layer_type(cls, v, values) -> LayerType:
        values["layer_type"] = LayerType.source
        return values["layer_type"]

    @classmethod
    def update_heat_flux(cls, below: ISECLayer = None, above: ISECLayer = None) -> None:
        total_flux = 0

        if below:
            total_flux += get_flux(cls.material.thermal_conductivity, cls.shape.sa_circle, (cls.shape.height + below.height) / 2, below.temperature, cls.temperature)
        if above:
            total_flux += get_flux(cls.material.thermal_conductivity, cls.shape.sa_circle, (cls.shape.height + above.height) / 2, cls.temperature, below.temperature)
        
        cls.heat_flux = total_flux + cls.power

class StorageLayer(ISECLayer):
    layer_type = LayerType.storage
    @validator("layer_type", always=True)
    def validate_layer_type(cls, v, values) -> LayerType:
        values["layer_type"] = LayerType.storage
        return values["layer_type"]

class SinkLayer(ISECLayer):
    layer_type = LayerType.sink
    @validator("layer_type", always=True)
    def validate_layer_type(cls, v, values) -> LayerType:
        values["layer_type"] = LayerType.sink
        return values["layer_type"]
    

class ISEC(BaseModel):

    isec_layers: Optional[List[ISECLayer]] = None

    @classmethod
    def stack(cls, layer: ISECLayer):

        if layer.shape.shape_type == None:
            raise ValueError("Layer Shape Type Cannot Be None.")
        try:
            if not cls.isec_layers:
                raise Exception
        except:
            cls.isec_layers = [layer]

        for stacked_layers in cls.isec_layers:
            if layer.shape.shape_type != stacked_layers.shape.shape_type:
                raise ValueError(f"Stacked Shapes Must Have Same Type | {layer.shape.shape_type} can't be stacked on {stacked_layer.shape.shape_type}.")
        cls.isec_layers.append(layer)
        print(f"Stacked {layer.material.name} {layer.shape.shape_type} ({layer.layer_type}).")
    
    @classmethod
    def next_layer(cls, index: int):
        next = None
        try:
            next = cls.isec_layers[index + 1]
        except:
            pass
        return next

    @classmethod
    def prev_layer(cls, index: int):
        prev = None
        try:
            prev = cls.isec_layers[index - 1]
        except:
            pass
        return prev         
    
    @classmethod
    def run_simulation(
        cls,
        time_step: float,
        steps: int):

        step = 0
        num_layers = len(cls.isec_layers)
        while step < steps:
            for i, layer in enumerate(cls.isec_layers):
                # Calculate Flux
                layer.update_heat_flux(cls.prev_layer(i), cls.next_layer(i))
            for layer in cls.isec_layers:
                # Update Temperatures
                layer.update_temp(time_step)
                print("Layer Temperature: ", layer.temperature)
            step += 1