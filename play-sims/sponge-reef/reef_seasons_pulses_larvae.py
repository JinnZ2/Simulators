"""
Sponge reef — seasons + nutrient pulses + larval dispersal.

Latitude-driven seasonal light and temperature cycles, discrete nutrient
pulses (upwelling/runoff), and larval production + advective dispersal
by currents. Interactive widget over lat / pulse frequency / feeding +
photo efficiency / herbivory / steps.

CC0 / for play. Extracted verbatim from legacy/Organize.md lines 1737-2261.
Non-stdlib: numpy, matplotlib, ipywidgets, scipy.ndimage, IPython.display.
"""

# ===================================================================
#  ULTIMATE SPONGE REEF SIMULATOR
#  Seasonal cycles + Nutrient pulses + Larval dispersal
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox, Output, interactive
from IPython.display import display, clear_output
from scipy.ndimage import gaussian_filter, convolve

# -------------------------------------------------------------------
# 1. Enhanced Sponge agent (with larval production)
# -------------------------------------------------------------------
class Sponge:
    def __init__(self, mixo=False, max_biomass=2.0, feeding_eff=0.5, 
                 photo_eff_blue=0.4, photo_eff_red=0.2):
        self.is_mixo = mixo
        self.max_biomass = max_biomass
        self.biomass = np.random.uniform(0.2, 0.5)
        self.feeding_efficiency = feeding_eff
        self.photo_eff_blue = photo_eff_blue
        self.photo_eff_red = photo_eff_red
        self.metabolic_cost_base = 0.01
        self.productivity = 0.0
        self.age = 0
        self.stress = 0.0
        self.larval_pool = 0.0  # accumulated larval biomass to release
        
    def step(self, light_blue, light_red, nutrient, temperature, herbivore_pressure, dt=0.1):
        self.age += dt
        
        # ---- Temperature effects ----
        temp_opt = 25.0
        temp_range = 5.0
        temp_stress = np.exp(-((temperature - temp_opt) / temp_range)**2)
        temp_factor = 1.5 ** ((temperature - 25) / 10)
        metabolic_cost = self.metabolic_cost_base * temp_factor
        
        # ---- Bleaching ----
        if self.is_mixo and temperature > 28.0:
            self.stress += (temperature - 28.0) * 0.01 * dt
        else:
            self.stress *= (1 - dt * 0.1)
        self.stress = np.clip(self.stress, 0, 1)
        photo_eff_blue_actual = self.photo_eff_blue * (1 - self.stress * 0.8)
        photo_eff_red_actual = self.photo_eff_red * (1 - self.stress * 0.8)
        
        # ---- Filter feeding ----
        feed_gain = self.feeding_efficiency * self.biomass * nutrient * dt
        
        # ---- Photosynthesis ----
        photo_gain = 0.0
        if self.is_mixo:
            photo_gain = (photo_eff_blue_actual * light_blue + 
                          photo_eff_red_actual * light_red) * self.biomass * dt
        
        # ---- Herbivory ----
        graze_loss = herbivore_pressure * self.biomass * dt * 0.5
        
        # ---- Growth ----
        total_gain = feed_gain + photo_gain
        self.biomass += total_gain - graze_loss - metabolic_cost * self.biomass * dt
        self.biomass = np.clip(self.biomass, 0, self.max_biomass)
        
        # ---- Larval production (if biomass > threshold) ----
        self.larval_pool = 0.0
        if self.biomass > 0.8:
            # Invest 5% of surplus biomass into larvae
            surplus = max(0, self.biomass - 0.8)
            larval_investment = surplus * 0.05 * dt
            self.biomass -= larval_investment
            self.larval_pool = larval_investment * 100  # larval units (scaling)
        
        # ---- Productivity ----
        self.productivity = total_gain * dt
        
        return feed_gain, photo_gain, graze_loss, self.larval_pool

# -------------------------------------------------------------------
# 2. Reef environment with seasons, pulses, and currents
# -------------------------------------------------------------------
class DynamicReef:
    def __init__(self, size=30, depth_max=20, lat_deg=0, 
                 light_atten_blue=0.05, light_atten_red=0.15):
        self.size = size
        self.depth_max = depth_max
        self.lat_deg = lat_deg  # latitude (for seasonality)
        self.light_atten_blue = light_atten_blue
        self.light_atten_red = light_atten_red
        
        # Depth grid
        self.depth = np.linspace(0, depth_max, size)
        self.depth_grid = np.tile(self.depth, (size, 1)).T
        
        # ---- Seasonality parameters ----
        self.day_of_year = 0.0
        self.year_length = 365.0  # steps per year (will be scaled)
        
        # ---- Currents (for larval dispersal) ----
        # Simple 2D current field (west-to-east with some shear)
        self.current_u = np.ones((size, size)) * 0.5  # x-direction (eastward)
        self.current_v = np.zeros((size, size))       # y-direction (vertical)
        # Add some eddies
        for i in range(size):
            for j in range(size):
                self.current_u[i, j] += 0.3 * np.sin(i/5) * np.cos(j/3)
                self.current_v[i, j] += 0.2 * np.cos(i/4) * np.sin(j/6)
        
        # ---- Initialise environment ----
        self.update_environment(0.0)
        
        # ---- Nutrients ----
        self.nutrients = np.ones((size, size)) * 0.8
        self.nutrient_diffusion = 0.1
        self.nutrient_replenishment = 0.005
        
        # ---- Sponge grid ----
        self.sponges = np.empty((size, size), dtype=object)
        self.sponges.fill(None)
        
        # ---- Herbivore pressure ----
        self.herbivore_pressure = 0.1
        
        # ---- Larval pool (for dispersal) ----
        self.larval_pool = np.zeros((size, size))  # larvae per cell
        
        # ---- History ----
        self.history = {'biomass_filter': [], 'biomass_mixo': [], 
                        'nutrients_mean': [], 'productivity': [],
                        'temp_mean': [], 'light_mean': [], 'day': []}
        
    def update_environment(self, day):
        """Update solar angle, temperature, and light based on day of year."""
        self.day_of_year = day % self.year_length
        # Solar declination: sinusoidal over year (max at summer)
        declination = 23.44 * np.sin(2 * np.pi * (day - 80) / self.year_length)
        # Solar angle at noon: 90 - latitude + declination
        solar_zenith = np.radians(90 - self.lat_deg + declination)
        solar_zenith = np.clip(solar_zenith, 0.1, np.pi/2)  # never night
        sun_factor = np.cos(solar_zenith)
        sun_factor = max(0.05, sun_factor)  # never zero
        
        # Light with solar angle
        self.light_blue = sun_factor * np.exp(-self.light_atten_blue * self.depth_grid)
        self.light_red = sun_factor * np.exp(-self.light_atten_red * self.depth_grid)
        
        # Temperature: seasonal + thermocline
        seasonal_temp = 5.0 * np.sin(2 * np.pi * (day - 15) / self.year_length)
        base_temp = 20.0 + seasonal_temp  # varies 15-25°C
        self.temperature = base_temp - self.depth_grid * 0.25 + np.random.randn(self.size, self.size) * 0.3
        self.temperature = np.clip(self.temperature, 10, 32)
        
        return sun_factor
    
    def apply_nutrient_pulse(self, strength=0.5, duration=10):
        """Upwelling pulse: nutrients rise from deep water."""
        # Pulse at depth (bottom layer)
        pulse_profile = np.exp(-self.depth / 5)  # strongest at bottom
        for i in range(self.size):
            self.nutrients[i, :] += strength * pulse_profile[i] * duration * 0.05
        self.nutrients = np.clip(self.nutrients, 0, 2.0)
        print(f"🌊 NUTRIENT PULSE! (strength={strength:.2f})")
    
    def disperse_larvae(self, dt=0.1):
        """Advect and diffuse larvae, then settle them."""
        # ---- Advection ----
        new_larvae = self.larval_pool.copy()
        # Simple upwind advection
        u = self.current_u
        v = self.current_v
        # x-advection
        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                if u[i, j] > 0:
                    flux_x = u[i, j] * self.larval_pool[i-1, j]
                else:
                    flux_x = u[i, j] * self.larval_pool[i+1, j]
                # y-advection
                if v[i, j] > 0:
                    flux_y = v[i, j] * self.larval_pool[i, j-1]
                else:
                    flux_y = v[i, j] * self.larval_pool[i, j+1]
                new_larvae[i, j] += (flux_x + flux_y) * dt
        
        # ---- Diffusion ----
        new_larvae += self.nutrient_diffusion * 0.5 * (
            self.larval_pool[2:, 1:-1] + self.larval_pool[:-2, 1:-1] +
            self.larval_pool[1:-1, 2:] + self.larval_pool[1:-1, :-2] -
            4 * self.larval_pool[1:-1, 1:-1]
        ) * dt
        
        # ---- Decay ----
        new_larvae *= (1 - 0.02 * dt)  # larval mortality
        
        # ---- Settlement ----
        # Larvae settle in empty cells
        for i in range(self.size):
            for j in range(self.size):
                if self.sponges[i, j] is None and new_larvae[i, j] > 0.1:
                    # Probabilistic settlement
                    settle_prob = min(1, new_larvae[i, j] * 0.1)
                    if np.random.rand() < settle_prob * dt * 10:
                        # Determine type: mixo fraction based on local light
                        light_avg = (self.light_blue[i, j] + self.light_red[i, j]) / 2
                        mixo_chance = 0.3 + 0.6 * light_avg / np.max(self.light_blue + self.light_red + 1e-6)
                        is_mixo = np.random.rand() < mixo_chance
                        self.sponges[i, j] = Sponge(
                            mixo=is_mixo,
                            max_biomass=2.0,
                            feeding_eff=np.random.uniform(0.3, 0.7),
                            photo_eff_blue=np.random.uniform(0.2, 0.5),
                            photo_eff_red=np.random.uniform(0.1, 0.3)
                        )
                        new_larvae[i, j] -= 0.5  # consume some larvae
        
        self.larval_pool = np.clip(new_larvae, 0, None)
    
    def step(self, dt=0.1, nutrient_pulse_prob=0.002):
        """Advance one time step."""
        # ---- Update seasonal environment ----
        self.update_environment(self.day_of_year + dt * 10)  # fast seasons
        
        # ---- Nutrient pulse (random upwelling) ----
        if np.random.rand() < nutrient_pulse_prob:
            self.apply_nutrient_pulse(strength=np.random.uniform(0.3, 1.0), duration=5)
        
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
        
        # Collect all sponges
        sponge_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.sponges[i, j] is not None:
                    sponge_list.append((i, j, self.sponges[i, j]))
        
        # Shuffle to avoid order bias
        np.random.shuffle(sponge_list)
        
        for i, j, sponge in sponge_list:
            # Get local conditions
            light_b = self.light_blue[i, j]
            light_r = self.light_red[i, j]
            nutrient = self.nutrients[i, j]
            temp = self.temperature[i, j]
            herb = self.herbivore_pressure
            
            # Step sponge
            feed_gain, photo_gain, graze_loss, larvae = sponge.step(
                light_b, light_r, nutrient, temp, herb, dt
            )
            
            # Deplete nutrients locally
            self.nutrients[i, j] -= feed_gain * 0.5
            self.nutrients[i, j] = max(0, self.nutrients[i, j])
            
            # Add larvae to larval pool (with some spread)
            if larvae > 0:
                # Spread larvae to nearby cells (current + diffusion handled in disperse)
                self.larval_pool[i, j] += larvae * 0.5
                # Also spread to neighbours
                for di, dj in [(1,0), (-1,0), (0,1), (0,-1)]:
                    ni, nj = i+di, j+dj
                    if 0 <= ni < self.size and 0 <= nj < self.size:
                        self.larval_pool[ni, nj] += larvae * 0.1
            
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
                neighbors = [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
                np.random.shuffle(neighbors)
                for ni, nj in neighbors:
                    if 0 <= ni < self.size and 0 <= nj < self.size:
                        if self.sponges[ni, nj] is None:
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
                            if sponge.biomass > self.sponges[ni, nj].biomass * 1.2:
                                self.sponges[ni, nj] = Sponge(
                                    mixo=sponge.is_mixo,
                                    max_biomass=sponge.max_biomass,
                                    feeding_eff=sponge.feeding_efficiency * (1 + np.random.uniform(-0.02, 0.02)),
                                    photo_eff_blue=sponge.photo_eff_blue * (1 + np.random.uniform(-0.02, 0.02)),
                                    photo_eff_red=sponge.photo_eff_red * (1 + np.random.uniform(-0.02, 0.02))
                                )
                                sponge.biomass *= 0.9
                                break
        
        # ---- Larval dispersal ----
        self.disperse_larvae(dt)
        
        # ---- Record history ----
        self.history['biomass_filter'].append(biomass_filter)
        self.history['biomass_mixo'].append(biomass_mixo)
        self.history['nutrients_mean'].append(np.mean(self.nutrients))
        self.history['productivity'].append(total_productivity)
        self.history['temp_mean'].append(np.mean(self.temperature))
        self.history['light_mean'].append(np.mean(self.light_blue + self.light_red))
        self.history['day'].append(self.day_of_year)
        
        return biomass_filter, biomass_mixo

# -------------------------------------------------------------------
# 3. Simulation runner (with seasons & pulses)
# -------------------------------------------------------------------
def run_dynamic_sim(size, depth, atten_b, atten_r, lat_deg, mixo_frac,
                    feed_eff, photo_b, photo_r, herbivory, pulse_freq, steps):
    # Create reef
    reef = DynamicReef(size=size, depth_max=depth, lat_deg=lat_deg,
                       light_atten_blue=atten_b, light_atten_red=atten_r)
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
    
    # Set pulse frequency (probability per step)
    pulse_prob = pulse_freq / 100.0  # 0-10% -> 0-0.1
    
    # Run
    for t in range(steps):
        reef.step(dt=0.1, nutrient_pulse_prob=pulse_prob)
    
    return reef

# -------------------------------------------------------------------
# 4. Enhanced plotting (with seasonal panel)
# -------------------------------------------------------------------
def plot_dynamic_reef(reef):
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(3, 3, height_ratios=[1, 1, 1])
    
    # ---- Row 0: Spatial maps ----
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
    im1 = ax.imshow(type_map, origin='lower', cmap='coolwarm', vmin=0, vmax=1, 
                    extent=[0, reef.size, 0, reef.size])
    ax.set_title('Sponge types (blue=mixo, red=filter)')
    ax.set_xlabel('x'); ax.set_ylabel('y (depth)')
    ax.grid(alpha=0.2)
    
    ax = fig.add_subplot(gs[0, 1])
    im2 = ax.imshow(biomass_map, origin='lower', cmap='viridis', extent=[0, reef.size, 0, reef.size])
    ax.set_title('Biomass per cell')
    ax.set_xlabel('x'); ax.set_ylabel('y (depth)')
    plt.colorbar(im2, ax=ax, fraction=0.05)
    
    ax = fig.add_subplot(gs[0, 2])
    im3 = ax.imshow(reef.larval_pool, origin='lower', cmap='plasma', extent=[0, reef.size, 0, reef.size])
    ax.set_title('Larval pool (settlement)')
    ax.set_xlabel('x'); ax.set_ylabel('y (depth)')
    plt.colorbar(im3, ax=ax, fraction=0.05)
    
    # ---- Row 1: Seasonal & environmental ----
    ax = fig.add_subplot(gs[1, 0])
    depth_axis = np.linspace(0, reef.size, reef.size)
    ax.plot(np.mean(reef.light_blue, axis=1), depth_axis, 'b-', label='Blue')
    ax.plot(np.mean(reef.light_red, axis=1), depth_axis, 'r-', label='Red')
    ax.set_xlabel('Light')
    ax.set_ylabel('Depth (index)')
    ax.set_title('Light spectra')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.invert_yaxis()
    
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(np.mean(reef.temperature, axis=1), depth_axis, 'orange', lw=2)
    ax.set_xlabel('Temperature (°C)')
    ax.set_ylabel('Depth (index)')
    ax.set_title('Thermocline')
    ax.grid(alpha=0.3)
    ax.invert_yaxis()
    
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(np.mean(reef.nutrients, axis=1), depth_axis, 'g-', lw=2)
    ax.set_xlabel('Nutrients')
    ax.set_ylabel('Depth (index)')
    ax.set_title('Nutrient profile')
    ax.grid(alpha=0.3)
    ax.invert_yaxis()
    
    # ---- Row 2: Time series ----
    time = np.arange(0, len(reef.history['biomass_filter']))
    day = np.array(reef.history['day'])
    
    ax = fig.add_subplot(gs[2, 0])
    ax.plot(time, reef.history['biomass_filter'], 'r-', label='Filter')
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
    ax.set_title('Total productivity')
    ax.grid(alpha=0.3)
    
    ax = fig.add_subplot(gs[2, 2])
    ax.plot(time, reef.history['temp_mean'], 'orange', label='Temp')
    ax.plot(time, reef.history['light_mean'], 'yellow', label='Light')
    ax.plot(time, reef.history['nutrients_mean'], 'g-', label='Nutrients')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Mean value')
    ax.set_title('Environmental dynamics')
    ax.legend()
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
# 5. Interactive wrapper
# -------------------------------------------------------------------
def interact_dynamic(size, depth, atten_b, atten_r, lat_deg, mixo_frac,
                     feed_eff, photo_b, photo_r, herbivory, pulse_freq, steps):
    reef = run_dynamic_sim(size, depth, atten_b, atten_r, lat_deg, mixo_frac,
                           feed_eff, photo_b, photo_r, herbivory, pulse_freq, steps)
    plot_dynamic_reef(reef)
    
    # Summary
    total = sum(reef.history['biomass_filter'][-1] + reef.history['biomass_mixo'][-1])
    mixo = reef.history['biomass_mixo'][-1]
    filt = reef.history['biomass_filter'][-1]
    prod = reef.history['productivity'][-1]
    print(f"\n{'='*60}")
    print(f"🌍 DYNAMIC REEF SUMMARY (steps={steps})")
    print(f"Total biomass: {total:.2f}  | Mixo: {mixo:.2f} ({mixo/total*100:.1f}%)")
    print(f"Productivity: {prod:.3f}")
    print(f"Mean temp: {reef.history['temp_mean'][-1]:.1f}°C")
    print(f"Light: {reef.history['light_mean'][-1]:.2f}")
    print(f"Nutrients: {reef.history['nutrients_mean'][-1]:.3f}")
    print(f"Larval pool total: {np.sum(reef.larval_pool):.1f}")
    print(f"{'='*60}")

# -------------------------------------------------------------------
# 6. Widgets
# -------------------------------------------------------------------
style = {'description_width': 'initial'}
controls = {
    'size': IntSlider(value=30, min=20, max=50, step=2, description='Reef size', style=style),
    'depth': IntSlider(value=20, min=10, max=40, step=2, description='Max depth (m)', style=style),
    'atten_b': FloatSlider(value=0.05, min=0.01, max=0.2, step=0.01, description='Blue atten.', style=style),
    'atten_r': FloatSlider(value=0.15, min=0.05, max=0.5, step=0.01, description='Red atten.', style=style),
    'lat_deg': FloatSlider(value=0, min=-60, max=60, step=5, description='Latitude (°)', style=style),
    'mixo_frac': FloatSlider(value=0.5, min=0, max=1, step=0.05, description='Initial mixo frac', style=style),
    'feed_eff': FloatSlider(value=0.5, min=0.1, max=0.9, step=0.05, description='Feeding eff.', style=style),
    'photo_b': FloatSlider(value=0.4, min=0, max=0.8, step=0.05, description='Photo eff. (blue)', style=style),
    'photo_r': FloatSlider(value=0.2, min=0, max=0.8, step=0.05, description='Photo eff. (red)', style=style),
    'herbivory': FloatSlider(value=0.1, min=0, max=0.5, step=0.01, description='Herbivory', style=style),
    'pulse_freq': FloatSlider(value=2.0, min=0, max=10, step=0.5, description='Pulse freq (%)', style=style),
    'steps': IntSlider(value=300, min=100, max=600, step=20, description='Steps', style=style)
}

out = Output()
def update(**kwargs):
    with out:
        clear_output(wait=True)
        interact_dynamic(**kwargs)

interactive_widget = interactive(update, **controls)
display(HBox([VBox([controls[k] for k in controls]), out]))

# -------------------------------------------------------------------
# 7. Run default dynamic case
# -------------------------------------------------------------------
print("\n🌊 RUNNING DYNAMIC REEF WITH SEASONS + PULSES + LARVAE")
interact_dynamic(size=30, depth=20, atten_b=0.05, atten_r=0.15, lat_deg=0,
                 mixo_frac=0.5, feed_eff=0.5, photo_b=0.4, photo_r=0.2,
                 herbivory=0.1, pulse_freq=2.0, steps=300)
