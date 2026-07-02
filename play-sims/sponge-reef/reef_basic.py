"""
Sponge reef productivity — basic.

Filter-feeders vs mixotrophs (photosynthetic sponges) on a 2D reef grid.
Light attenuates with depth; mixotrophs sit shallow and photosynthesise;
filter-feeders sit deep and pull suspended food. Interactive widget over
size / depth / attenuation / mixo fraction / feeding + photo efficiency.

CC0 / for play. Extracted verbatim from Organize.md lines 1022-1326.
Non-stdlib: numpy, matplotlib, ipywidgets, IPython.display.
"""

# ===================================================================
#  SPONGE REEF PRODUCTIVITY SIMULATOR
#  Filter-feeders vs Mixotrophs (photosynthetic sponges)
#  ===================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, fixed, Output, Button, HBox, VBox
from IPython.display import display, clear_output
import matplotlib.animation as animation
from scipy.ndimage import gaussian_filter

# -------------------------------------------------------------------
# 1. Reef environment
# -------------------------------------------------------------------
class Reef:
    def __init__(self, size=30, depth_max=20, light_attenuation=0.1):
        self.size = size
        self.depth_max = depth_max
        self.light_atten = light_attenuation
        
        # Create depth map (0 at top, depth_max at bottom)
        self.depth = np.linspace(0, depth_max, size)
        self.depth_grid = np.tile(self.depth, (size, 1)).T  # depth increases downward
        
        # Light intensity (exponential decay with depth)
        self.light = np.exp(-self.light_atten * self.depth_grid)
        
        # Nutrients (plankton) – initial uniform
        self.nutrients = np.ones((size, size)) * 1.0
        self.nutrient_diffusion = 0.1
        self.nutrient_replenishment = 0.01
        
        # Sponge grid: None or Sponge object
        self.sponges = np.empty((size, size), dtype=object)
        self.sponges.fill(None)
        
        # History for plotting
        self.history = {'biomass_filter': [], 'biomass_mixo': [], 'nutrients_mean': [], 'productivity': []}
        
    def step(self, dt=0.1):
        # ---- Diffusion of nutrients ----
        new_nutrients = self.nutrients.copy()
        # Simple 2D diffusion
        new_nutrients[1:-1, 1:-1] += self.nutrient_diffusion * (
            self.nutrients[2:, 1:-1] + self.nutrients[:-2, 1:-1] +
            self.nutrients[1:-1, 2:] + self.nutrients[1:-1, :-2] -
            4 * self.nutrients[1:-1, 1:-1]
        ) * dt
        # Replenishment from deep water (bottom boundary)
        new_nutrients[-1, :] += self.nutrient_replenishment * dt
        # Clamp
        self.nutrients = np.clip(new_nutrients, 0, 2.0)
        
        # ---- Sponge actions ----
        biomass_filter = 0.0
        biomass_mixo = 0.0
        total_productivity = 0.0
        
        # Collect all sponges to avoid modifying while iterating
        sponge_list = []
        for i in range(self.size):
            for j in range(self.size):
                if self.sponges[i, j] is not None:
                    sponge_list.append((i, j, self.sponges[i, j]))
        
        for i, j, sponge in sponge_list:
            # Get local light and nutrients
            light = self.light[i, j]
            nutrient = self.nutrients[i, j]
            
            # Sponge steps: feed, photosynthesize, grow, reproduce, die
            sponge.step(light, nutrient, dt)
            
            # Accumulate biomass
            if sponge.is_mixo:
                biomass_mixo += sponge.biomass
            else:
                biomass_filter += sponge.biomass
            
            total_productivity += sponge.productivity
            
            # If sponge dies, remove it
            if sponge.biomass <= 0:
                self.sponges[i, j] = None
            else:
                # Reproduction: if biomass > threshold, spawn a new sponge nearby
                if sponge.biomass > 1.5 and np.random.rand() < 0.01 * dt:
                    # Find empty adjacent cell
                    neighbors = [(i+1,j), (i-1,j), (i,j+1), (i,j-1), (i+1,j+1), (i-1,j-1), (i+1,j-1), (i-1,j+1)]
                    valid = [(ni, nj) for ni, nj in neighbors if 0 <= ni < self.size and 0 <= nj < self.size and self.sponges[ni, nj] is None]
                    if valid:
                        ni, nj = valid[np.random.randint(len(valid))]
                        # New sponge inherits type (with small mutation)
                        new_mixo = sponge.is_mixo if np.random.rand() > 0.05 else not sponge.is_mixo
                        self.sponges[ni, nj] = Sponge(
                            mixo=new_mixo,
                            max_biomass=sponge.max_biomass,
                            feeding_efficiency=sponge.feeding_efficiency * (1 + np.random.uniform(-0.1, 0.1)),
                            photosynthesis_efficiency=sponge.photosynthesis_efficiency * (1 + np.random.uniform(-0.1, 0.1))
                        )
        
        # ---- Record history ----
        self.history['biomass_filter'].append(biomass_filter)
        self.history['biomass_mixo'].append(biomass_mixo)
        self.history['nutrients_mean'].append(np.mean(self.nutrients))
        self.history['productivity'].append(total_productivity)
        
        return biomass_filter, biomass_mixo

# -------------------------------------------------------------------
# 2. Sponge agent
# -------------------------------------------------------------------
class Sponge:
    def __init__(self, mixo=False, max_biomass=2.0, feeding_efficiency=0.5, photosynthesis_efficiency=0.3):
        self.is_mixo = mixo
        self.max_biomass = max_biomass
        self.biomass = np.random.uniform(0.2, 0.5)
        self.feeding_efficiency = feeding_efficiency
        self.photosynthesis_efficiency = photosynthesis_efficiency
        self.productivity = 0.0
        self.metabolic_cost = 0.01
        
    def step(self, light, nutrient, dt):
        # ---- Filter feeding ----
        # Consume nutrients proportional to biomass and nutrient availability
        feed_gain = self.feeding_efficiency * self.biomass * nutrient * dt
        # ---- Photosynthesis (if mixo) ----
        photo_gain = 0.0
        if self.is_mixo:
            photo_gain = self.photosynthesis_efficiency * self.biomass * light * dt
        
        # ---- Growth ----
        total_gain = feed_gain + photo_gain
        self.biomass += total_gain
        # Reduce nutrients locally (filtering)
        # (We'll handle nutrient depletion in the reef step, but we can also subtract here)
        # For simplicity, we'll let the reef diffusion handle depletion, but we can directly subtract:
        # (We'll not modify nutrients here to keep it clean; reef will deplete based on biomass)
        
        # ---- Metabolism ----
        self.biomass -= self.metabolic_cost * self.biomass * dt
        self.biomass = np.clip(self.biomass, 0, self.max_biomass)
        
        # ---- Productivity (energy fixed per unit time) ----
        self.productivity = total_gain * dt  # per step
        
        # ---- Deplete nutrients (filtering) ----
        # We'll return the amount consumed so reef can subtract
        # We'll do this outside in the reef step for simplicity.
        # For now, we just compute gain.
        return feed_gain, photo_gain

# -------------------------------------------------------------------
# 3. Simulation runner
# -------------------------------------------------------------------
def run_simulation(reef_size, depth_max, light_atten, mixo_fraction, feeding_eff, photo_eff, steps=200):
    # Create reef
    reef = Reef(size=reef_size, depth_max=depth_max, light_attenuation=light_atten)
    
    # Seed sponges
    total_cells = reef_size * reef_size
    n_sponges = int(total_cells * 0.3)  # 30% occupancy
    positions = np.random.choice(total_cells, n_sponges, replace=False)
    for pos in positions:
        i = pos // reef_size
        j = pos % reef_size
        is_mixo = np.random.rand() < mixo_fraction
        reef.sponges[i, j] = Sponge(
            mixo=is_mixo,
            max_biomass=2.0,
            feeding_efficiency=feeding_eff,
            photosynthesis_efficiency=photo_eff
        )
    
    # Run steps
    for t in range(steps):
        reef.step(dt=0.1)
    
    return reef

# -------------------------------------------------------------------
# 4. Plotting function
# -------------------------------------------------------------------
def plot_reef(reef):
    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(2, 3, height_ratios=[1, 0.8])
    
    # ---- Sponge type map ----
    ax = fig.add_subplot(gs[0, 0])
    type_map = np.zeros((reef.size, reef.size))
    biomass_map = np.zeros((reef.size, reef.size))
    for i in range(reef.size):
        for j in range(reef.size):
            if reef.sponges[i, j] is not None:
                type_map[i, j] = 1 if reef.sponges[i, j].is_mixo else 0.5
                biomass_map[i, j] = reef.sponges[i, j].biomass
    im1 = ax.imshow(type_map, origin='lower', cmap='coolwarm', vmin=0, vmax=1, extent=[0, reef.size, 0, reef.size])
    ax.set_title('Sponge types (blue=mixo, red=filter)')
    ax.set_xlabel('x')
    ax.set_ylabel('y (depth)')
    
    # ---- Biomass map ----
    ax = fig.add_subplot(gs[0, 1])
    im2 = ax.imshow(biomass_map, origin='lower', cmap='viridis', extent=[0, reef.size, 0, reef.size])
    ax.set_title('Biomass per cell')
    ax.set_xlabel('x')
    ax.set_ylabel('y (depth)')
    plt.colorbar(im2, ax=ax, fraction=0.05)
    
    # ---- Light & nutrients ----
    ax = fig.add_subplot(gs[0, 2])
    ax.plot(np.mean(reef.light, axis=1), np.linspace(0, reef.size, reef.size), 'y-', label='Light')
    ax.plot(np.mean(reef.nutrients, axis=1), np.linspace(0, reef.size, reef.size), 'g-', label='Nutrients')
    ax.set_xlabel('Mean value')
    ax.set_ylabel('Depth (grid index)')
    ax.set_title('Depth profiles')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # ---- Biomass over time ----
    ax = fig.add_subplot(gs[1, 0])
    time = np.arange(0, len(reef.history['biomass_filter']))
    ax.plot(time, reef.history['biomass_filter'], 'r-', label='Filter-feeders')
    ax.plot(time, reef.history['biomass_mixo'], 'b-', label='Mixotrophs')
    ax.set_xlabel('Time step')
    ax.set_ylabel('Total biomass')
    ax.set_title('Biomass evolution')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # ---- Productivity ----
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(time, reef.history['productivity'], 'purple', lw=2)
    ax.set_xlabel('Time step')
    ax.set_ylabel('Productivity (energy fixed)')
    ax.set_title('Total reef productivity')
    ax.grid(alpha=0.3)
    
    # ---- Nutrient mean ----
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(time, reef.history['nutrients_mean'], 'g-', lw=2)
    ax.set_xlabel('Time step')
    ax.set_ylabel('Mean nutrient concentration')
    ax.set_title('Nutrient depletion')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------
# 5. Interactive control
# -------------------------------------------------------------------
def interact_reef(reef_size, depth_max, light_atten, mixo_fraction, feeding_eff, photo_eff, steps):
    reef = run_simulation(reef_size, depth_max, light_atten, mixo_fraction, feeding_eff, photo_eff, steps)
    plot_reef(reef)
    
    # Print summary
    total_biomass = sum(reef.history['biomass_filter'][-1] + reef.history['biomass_mixo'][-1])
    mixo_biomass = reef.history['biomass_mixo'][-1]
    filter_biomass = reef.history['biomass_filter'][-1]
    final_productivity = reef.history['productivity'][-1]
    print(f"\n{'='*50}")
    print(f"REEF SUMMARY (after {steps} steps)")
    print(f"Total biomass: {total_biomass:.2f}")
    print(f"  Mixotrophs: {mixo_biomass:.2f} ({mixo_biomass/total_biomass*100:.1f}%)")
    print(f"  Filter-feeders: {filter_biomass:.2f} ({filter_biomass/total_biomass*100:.1f}%)")
    print(f"Productivity: {final_productivity:.3f}")
    print(f"Nutrient level: {reef.history['nutrients_mean'][-1]:.3f}")
    print(f"{'='*50}")

# -------------------------------------------------------------------
# 6. Create widgets
# -------------------------------------------------------------------
style = {'description_width': 'initial'}
controls = {
    'reef_size': IntSlider(value=30, min=20, max=50, step=2, description='Reef size (grid)', style=style),
    'depth_max': IntSlider(value=20, min=10, max=40, step=2, description='Max depth (m)', style=style),
    'light_atten': FloatSlider(value=0.1, min=0.05, max=0.3, step=0.01, description='Light attenuation', style=style),
    'mixo_fraction': FloatSlider(value=0.5, min=0.0, max=1.0, step=0.05, description='Initial mixo fraction', style=style),
    'feeding_eff': FloatSlider(value=0.5, min=0.2, max=0.9, step=0.05, description='Feeding efficiency', style=style),
    'photo_eff': FloatSlider(value=0.3, min=0.0, max=0.8, step=0.05, description='Photosynthesis efficiency', style=style),
    'steps': IntSlider(value=200, min=50, max=500, step=10, description='Simulation steps', style=style)
}

# Create interactive output
out = Output()

def update(**kwargs):
    with out:
        clear_output(wait=True)
        interact_reef(**kwargs)

interactive_widget = interactive(update, **controls)

# Display
display(HBox([VBox([controls[k] for k in controls]), out]))

# -------------------------------------------------------------------
# 7. Run a default case automatically
# -------------------------------------------------------------------
print("\n🚀 Running default simulation (50% mixo, moderate light)...")
interact_reef(reef_size=30, depth_max=20, light_atten=0.1, mixo_fraction=0.5,
              feeding_eff=0.5, photo_eff=0.3, steps=200)
