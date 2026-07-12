"""Centralised parameters for the climate-modeling audit suite."""

GRASS_DEFAULTS = {
    "P_max": 10.0,        # max photosynthetic rate
    "T_opt": 25.0,        # optimal temperature (°C)
    "sigma": 8.0,         # width of photosynthesis curve
    "R_base": 0.5,        # base respiration at 20°C
    "Q10": 2.0,           # respiration temperature sensitivity
    "M": 0.1,             # maintenance respiration
    "G": 0.2,             # structural growth
    "initial_C": 100.0,
}

SIM_DEFAULTS = {
    "duration_hours": 200,
    "max_step": 0.5,
}

FORCING_DEFAULTS = {
    "T_mean": 20.0,
    "amplitude": 10.0,
    "day_fraction": 0.5,
}
