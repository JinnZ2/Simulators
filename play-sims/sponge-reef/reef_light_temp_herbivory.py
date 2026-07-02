"""
Sponge reef — light spectrum + solar angle + temperature + herbivory.

Adds spectral attenuation (separate blue and red bands), oblique solar
angle, temperature-driven metabolism, and herbivory pressure to the
basic reef. Competition between the two sponge morphs plays out over
the depth gradient.

CC0 / for play. Extracted verbatim from legacy/Organize.md lines 1329-1735.
Non-stdlib: numpy, matplotlib, ipywidgets, scipy.ndimage, IPython.display.
"""

# ===================================================================
#  COMPLETE SPONGE REEF SIMULATOR
#  Light spectrum + Solar angle + Temperature + Herbivory + Competition
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox, Output, interactive
from IPython.display import display, clear_output
from scipy.ndimage import gaussian_filter

# -------------------------------------------------------------------
# 1. Enhanced Sponge agent
# -------------------------------------------------------------------
class Sponge:
    def __init__(self, mixo=False, max_biomass=2.0, feeding_eff=0.5, photo_eff_blue=0.4, photo_eff_red=0.2):
        self.is_mixo = mixo
        self.max_biomass = max_biomass
        self.biomass = np.random.uniform(0.2, 0.5)
        self.feeding_efficiency = feeding_eff
        # Photosynthesis efficiency per light type
        self.photo_eff_blue = photo_eff_blue
        self.photo_eff_red = photo_eff_red
        self.metabolic_cost_base = 0.01
        self.productivity = 0.0
        self.age = 0
        self.stress = 0.0  # bleaching stress (0-1)
        
    def step(self, light_blue, light_red, nutrient, temperature, herbivore_pressure, dt=0.1):
        self.age += dt
        
        # ---- Temperature effects ----
        # Optimal temperature ~ 25°C, stress if > 28°C or < 18°C
        temp_opt = 25.0
        temp_range = 5.0
        temp_stress = np.exp(-((temperature - temp_opt) / temp_range)**2)
        # Metabolic cost increases with temperature (Q10 ~2)
        temp_factor = 1.5 ** ((temperature - 25) / 10)
        metabolic_cost = self.metabolic_cost_base * temp_factor
        
        # ---- Bleaching (if mixo and temperature too high) ----
        if self.is_mixo and temperature > 28.0:
            self.stress += (temperature - 28.0) * 0.01 * dt
        else:
            self.stress *= (1 - dt * 0.1)  # recovery
        self.stress = np.clip(self.stress, 0, 1)
        # Reduce photosynthesis efficiency under stress
        photo_eff_blue_actual = self.photo_eff_blue * (1 - self.stress * 0.8)
        photo_eff_red_actual = self.photo_eff_red * (1 - self.stress * 0.8)
        
        # ---- Filter feeding ----
        feed_gain = self.feeding_efficiency * self.biomass * nutrient * dt
        
        # ---- Photosynthesis (if mixo) ----
        photo_gain = 0.0
        if self.is_mixo:
            # Combine blue and red light contributions
            photo_gain = (photo_eff_blue_actual * light_blue + photo_eff_red_actual * light_red) * self.biomass * dt
        
        # ---- Herbivory (grazing) ----
        graze_loss = herbivore_pressure * self.biomass * dt * 0.5
        
        # ---- Growth ----
        total_gain = feed_gain + photo_gain
        self.biomass += total_gain - graze_loss - metabolic_cost * self.biomass * dt
        self.biomass = np.clip(self.biomass, 0, self.max_biomass)
        
        # ---- Productivity ----
        self.productivity = total_gain * dt
        
        # ---- Return consumption (for nutrient depletion) ----
        return feed_gain, photo_gain, graze_loss

# -------------------------------------------------------------------
# 2. Enhanced Reef environment
# -------------------------------------------------------------------
class Reef:
    def __init__(self, size=30, depth_max=20, light_atten_blue=0.05, light_atten_red=0.15, solar_angle_deg=45):
        self.size = size
        self.depth_max = depth_max
        self.light_atten_blue = light_atten_blue
        self.light_atten_red = light_atten_red
        self.solar_angle = np.radians(solar_angle_deg)  # 0 = vertical
        
        # Depth grid
        self.depth = np.linspace(0, depth_max, size)
        self.depth_grid = np.tile(self.depth, (size, 1)).T
        
        # Light spectra (blue, red) with solar angle correction
        # Solar angle: steeper angle (higher latitude) reduces intensity
        zenith = max(0, self.solar_angle)  # angle from vertical
        sun_factor = np.cos(zenith)  # maximum 1 at zenith
        sun_factor = max(0.1, sun_factor)  # never zero
        
        self.light_blue = sun_factor * np.exp(-self.light_atten_blue * self.depth_grid)
        self.light_red = sun_factor * np.exp(-self.light_atten_red * self.depth_grid)
        
        # Temperature: warm at surface, cooler at depth (thermocline)
        self.temperature = 28.0 - self.depth_grid * 0.3 + np.random.randn(size, size) * 0.5
        self.temperature = np.clip(self.temperature, 15, 32)
        
        # Nutrients (plankton)
        self.nutrients = np.ones((size, size)) * 1.0
        self.nutrient_diffusion = 0.1
        self.nutrient_replenishment = 0.01
        
        # Sponge grid
        self.sponges = np.empty((size, size), dtype=object)
        self.sponges.fill(None)
        
        # Herbivore pressure (spatially uniform for now)
        self.herbivore_pressure = 0.0
        
        # History
        self.history = {'biomass_filter': [], 'biomass_mixo': [], 'nutrients_mean': [], 
                        'productivity': [], 'temp_mean': [], 'light_mean': []}
        
    def step(self, dt=0.1):
        # ---- Nutrient diffusion ----
        new_nutrients = self.nutrients.copy()
        new_nutrients[1:-1, 1:-1] += self.nutrient_diffusion * (
            self.nutrients[2:, 1:-1] + self.nutrients[:-2, 1:-1] +
            self.nutrients[1:-1, 2:] + self.nutrients[1:-1, :-2] -
            4 * self.nutrients[1:-1, 1:-1]
        ) * dt
        new_nutrients[-1, :] += self.nutrient_replenishment * dt
        self.nutrients = np.clip(new_nutrients, 0, 2.0)
        
        # ---- Sponge actions ----
        biomass_filter = 0.0
        biomass_mixo = 0.0
        total_productivity = 0.0
        
        sponge_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.sponges[i, j] is not None:
                    sponge_list.append((i, j, self.sponges[i, j]))
        
        # Competition: determine overgrowth (larger biomass wins space)
        # We'll process all sponges; if two adjacent, larger may overgrow smaller
        # For simplicity, we'll let them grow and reproduce; overgrowth is handled during reproduction.
        
        for i, j, sponge in sponge_list:
            # Get local conditions
            light_b = self.light_blue[i, j]
            light_r = self.light_red[i, j]
            nutrient = self.nutrients[i, j]
            temp = self.temperature[i, j]
            herb = self.herbivore_pressure
            
            # Sponge step (returns gains)
            feed_gain, photo_gain, graze_loss = sponge.step(light_b, light_r, nutrient, temp, herb, dt)
            
            # Deplete nutrients locally based on filtering
            # Assume each sponge consumes nutrients proportionally to its feed_gain
            self.nutrients[i, j] -= feed_gain * 0.5  # 50% of feed energy comes from local nutrients
            self.nutrients[i, j] = max(0, self.nutrients[i, j])
            
            # Accumulate biomass
            if sponge.is_mixo:
                biomass_mixo += sponge.biomass
            else:
                biomass_filter += sponge.biomass
            total_productivity += sponge.productivity
            
            # ---- Death ----
            if sponge.biomass <= 0 or sponge.stress > 0.95:
                self.sponges[i, j] = None
                continue
            
            # ---- Reproduction / Overgrowth ----
            if sponge.biomass > 1.2 and np.random.rand() < 0.02 * dt:
                # Find empty neighbor OR neighbor with smaller biomass (overgrowth)
                neighbors = [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
                np.random.shuffle(neighbors)
                for ni, nj in neighbors:
                    if 0 <= ni < self.size and 0 <= nj < self.size:
                        if self.sponges[ni, nj] is None:
                            # Spawn new sponge
                            new_mixo = sponge.is_mixo if np.random.rand() > 0.05 else not sponge.is_mixo
                            self.sponges[ni, nj] = Sponge(
                                mixo=new_mixo,
                                max_biomass=sponge.max_biomass,
                                feeding_eff=sponge.feeding_efficiency * (1 + np.random.uniform(-0.05, 0.05)),
                                photo_eff_blue=sponge.photo_eff_blue * (1 + np.random.uniform(-0.05, 0.05)),
                                photo_eff_red=sponge.photo_eff_red * (1 + np.random.uniform(-0.05, 0.05))
                            )
                            break
                        else:
                            # Overgrowth: if our sponge is larger than neighbor, take over
                            if sponge.biomass > self.sponges[ni, nj].biomass * 1.2:
                                # Kill neighbor and spawn new one
                                self.sponges[ni, nj] = Sponge(
                                    mixo=sponge.is_mixo,
                                    max_biomass=sponge.max_biomass,
                                    feeding_eff=sponge.feeding_efficiency * (1 + np.random.uniform(-0.02, 0.02)),
                                    photo_eff_blue=sponge.photo_eff_blue * (1 + np.random.uniform(-0.02, 0.02)),
                                    photo_eff_red=sponge.photo_eff_red * (1 + np.random.uniform(-0.02, 0.02))
                                )
                                # Give a small penalty to parent (cost of overgrowth)
                                sponge.biomass *= 0.9
                                break
        
        # ---- Record history ----
        self.history['biomass_filter'].append(biomass_filter)
        self.history['biomass_mixo'].append(biomass_mixo)
        self.history['nutrients_mean'].append(np.mean(self.nutrients))
        self.history['productivity'].append(total_productivity)
        self.history['temp_mean'].append(np.mean(self.temperature))
        self.history['light_mean'].append(np.mean(self.light_blue + self.light_red))
        
        return biomass_filter, biomass_mixo

# -------------------------------------------------------------------
# 3. Simulation runner
# -------------------------------------------------------------------
def run_simulation(size, depth, atten_b, atten_r, solar_angle, mixo_frac, feed_eff, photo_b, photo_r, herbivory, steps):
    # Create reef
    reef = Reef(size=size, depth_max=depth, light_atten_blue=atten_b, 
                light_atten_red=atten_r, solar_angle_deg=solar_angle)
    reef.herbivore_pressure = herbivory
    
    # Seed sponges
    total_cells = size * size
    n_sponges = int(total_cells * 0.3)
    positions = np.random.choice(total_cells, n_sponges, replace=False)
    for pos in positions:
        i = pos // size
        j = pos % size
        is_mixo = np.random.rand() < mixo_frac
        reef.sponges[i, j] = Sponge(
            mixo=is_mixo,
            max_biomass=2.0,
            feeding_eff=feed_eff,
            photo_eff_blue=photo_b,
            photo_eff_red=photo_r
        )
    
    # Run
    for t in range(steps):
        reef.step(dt=0.1)
    
    return reef

# -------------------------------------------------------------------
# 4. Enhanced plotting
# -------------------------------------------------------------------
def plot_reef_full(reef):
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1, 1, 1])
    
    # --- Row 0: Spatial maps ---
    # Sponge type map
    ax = fig.add_subplot(gs[0, 0])
    type_map = np.zeros((reef.size, reef.size))
    biomass_map = np.zeros((reef.size, reef.size))
    stress_map = np.zeros((reef.size, reef.size))
    for i in range(reef.size):
        for j in range(reef.size):
            if reef.sponges[i, j] is not None:
                type_map[i, j] = 1 if reef.sponges[i, j].is_mixo else 0.5
                biomass_map[i, j] = reef.sponges[i, j].biomass
                stress_map[i, j] = reef.sponges[i, j].stress
    im1 = ax.imshow(type_map, origin='lower', cmap='coolwarm', vmin=0, vmax=1, extent=[0, reef.size, 0, reef.size])
    ax.set_title('Sponge types (blue=mixo, red=filter)')
    ax.set_xlabel('x')
    ax.set_ylabel('y (depth)')
    ax.grid(alpha=0.2)
    
    # Biomass map
    ax = fig.add_subplot(gs[0, 1])
    im2 = ax.imshow(biomass_map, origin='lower', cmap='viridis', extent=[0, reef.size, 0, reef.size])
    ax.set_title('Biomass per cell')
    ax.set_xlabel('x')
    ax.set_ylabel('y (depth)')
    plt.colorbar(im2, ax=ax, fraction=0.05)
    
    # Temperature map
    ax = fig.add_subplot(gs[0, 2])
    im3 = ax.imshow(reef.temperature, origin='lower', cmap='RdBu_r', extent=[0, reef.size, 0, reef.size])
    ax.set_title('Water temperature (°C)')
    ax.set_xlabel('x')
    ax.set_ylabel('y (depth)')
    plt.colorbar(im3, ax=ax, fraction=0.05)
    
    # --- Row 1: Depth profiles ---
    ax = fig.add_subplot(gs[1, 0])
    depth_axis = np.linspace(0, reef.size, reef.size)
    ax.plot(np.mean(reef.light_blue, axis=1), depth_axis, 'b-', label='Blue light')
    ax.plot(np.mean(reef.light_red, axis=1), depth_axis, 'r-', label='Red light')
    ax.set_xlabel('Mean light intensity')
    ax.set_ylabel('Depth (grid index)')
    ax.set_title('Light spectra depth profiles')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.invert_yaxis()
    
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(np.mean(reef.temperature, axis=1), depth_axis, 'orange', lw=2)
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Depth (grid index)')
    ax.set_title('Thermocline profile')
    ax.grid(alpha=0.3)
    ax.invert_yaxis()
    
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(np.mean(reef.nutrients, axis=1), depth_axis, 'g-', lw=2)
    ax.set_xlabel('Nutrient concentration')
    ax.set_ylabel('Depth (grid index)')
    ax.set_title('Nutrient profile')
    ax.grid(alpha=0.3)
    ax.invert_yaxis()
    
    # --- Row 2: Time series ---
    time = np.arange(0, len(reef.history['biomass_filter']))
    
    ax = fig.add_subplot(gs[2, 0])
    ax.plot(time, reef.history['biomass_filter'], 'r-', label='Filter-feeders')
    ax.plot(time, reef.history['biomass_mixo'], 'b-', label='Mixotrophs')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Total biomass')
    ax.set_title('Biomass evolution')
    ax.legend()
    ax.grid(alpha=0.3)
    
    ax = fig.add_subplot(gs[2, 1])
    ax.plot(time, reef.history['productivity'], 'purple', lw=2)
    ax.set_xlabel('Time step')
    ax.set_ylabel('Productivity')
    ax.set_title('Total reef productivity')
    ax.grid(alpha=0.3)
    
    ax = fig.add_subplot(gs[2, 2])
    ax.plot(time, reef.history['nutrients_mean'], 'g-', label='Nutrients')
    ax.plot(time, reef.history['temp_mean'], 'orange', label='Temperature')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Mean value')
    ax.set_title('Environment means')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
# 5. Interactive wrapper
# -------------------------------------------------------------------
def interact_reef_full(size, depth, atten_b, atten_r, solar_angle, mixo_frac,
                        feed_eff, photo_b, photo_r, herbivory, steps):
    reef = run_simulation(size, depth, atten_b, atten_r, solar_angle, mixo_frac,
                          feed_eff, photo_b, photo_r, herbivory, steps)
    plot_reef_full(reef)
    
    # Summary
    total_biomass = sum(reef.history['biomass_filter'][-1] + reef.history['biomass_mixo'][-1])
    mixo_biomass = reef.history['biomass_mixo'][-1]
    filter_biomass = reef.history['biomass_filter'][-1]
    final_prod = reef.history['productivity'][-1]
    max_stress = np.max(stress_map) if 'stress_map' in locals() else 0
    print(f"\n{'='*60}")
    print(f"🌊 REEF SUMMARY (steps={steps})")
    print(f"Total biomass: {total_biomass:.2f}")
    print(f"  Mixotrophs: {mixo_biomass:.2f} ({mixo_biomass/total_biomass*100:.1f}%)")
    print(f"  Filter-feeders: {filter_biomass:.2f} ({filter_biomass/total_biomass*100:.1f}%)")
    print(f"Productivity: {final_prod:.3f}")
    print(f"Mean nutrient: {reef.history['nutrients_mean'][-1]:.3f}")
    print(f"Mean temp: {reef.history['temp_mean'][-1]:.1f}°C")
    print(f"Max bleaching stress: {max_stress:.2f}")
    print(f"{'='*60}")

# -------------------------------------------------------------------
# 6. Build widgets
# -------------------------------------------------------------------
style = {'description_width': 'initial'}
controls = {
    'size': IntSlider(value=30, min=20, max=50, step=2, description='Reef size (grid)', style=style),
    'depth': IntSlider(value=20, min=10, max=40, step=2, description='Max depth (m)', style=style),
    'atten_b': FloatSlider(value=0.05, min=0.01, max=0.2, step=0.01, description='Blue attenuation', style=style),
    'atten_r': FloatSlider(value=0.15, min=0.05, max=0.5, step=0.01, description='Red attenuation', style=style),
    'solar_angle': FloatSlider(value=45, min=0, max=80, step=5, description='Solar angle (deg)', style=style),
    'mixo_frac': FloatSlider(value=0.5, min=0, max=1, step=0.05, description='Initial mixo fraction', style=style),
    'feed_eff': FloatSlider(value=0.5, min=0.1, max=0.9, step=0.05, description='Feeding efficiency', style=style),
    'photo_b': FloatSlider(value=0.4, min=0, max=0.8, step=0.05, description='Photo eff. (blue)', style=style),
    'photo_r': FloatSlider(value=0.2, min=0, max=0.8, step=0.05, description='Photo eff. (red)', style=style),
    'herbivory': FloatSlider(value=0.1, min=0, max=0.5, step=0.01, description='Herbivore pressure', style=style),
    'steps': IntSlider(value=200, min=50, max=500, step=10, description='Simulation steps', style=style)
}

out = Output()
def update(**kwargs):
    with out:
        clear_output(wait=True)
        interact_reef_full(**kwargs)

interactive_widget = interactive(update, **controls)

display(HBox([VBox([controls[k] for k in controls]), out]))

# -------------------------------------------------------------------
# 7. Run default case
# -------------------------------------------------------------------
print("\n🚀 Running default: moderate light, 50% mixo, slight herbivory")
interact_reef_full(size=30, depth=20, atten_b=0.05, atten_r=0.15, solar_angle=45,
                   mixo_frac=0.5, feed_eff=0.5, photo_b=0.4, photo_r=0.2,
                   herbivory=0.1, steps=200)
