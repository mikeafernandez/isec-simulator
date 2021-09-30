def get_flux(k: float, area: float, separation: float, t1: float, t2: float):
    dT_dx = (t2-t1) / separation # C / cm^2
    return  -1 * k * area * dT_dx # Watts
