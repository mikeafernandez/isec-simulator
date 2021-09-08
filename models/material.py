from pydantic import BaseModel

class Material(BaseModel):

    name:           str
    id:             int   # Unique Material ID
    density:        float # g/cm^3
    molar_mass:     float # g/mol
    melting_point:  float # C
    heat_of_fusion: float # J/mol
    specific_heat:  float # J/g K
    t_conductivity: float # W/m K

    def __str__(self): 
        
        return f"""
        ------------------
        Name: {self.name}
        Id:   {self.id}
        Density: {self.density} (g/cm^3)
        Molar Mass: {self.melting_point} (g/mol)
        Heat Of Fusion: {self.heat_of_fusion} (J/mol)
        Specific Heat: {self.specific_heat} (J/g C)
        Thermal Conductivity: {self.t_conductivity} (W/m k)
        ------------------
        """
        
