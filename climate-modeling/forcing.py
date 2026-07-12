"""Environmental forcing generators. Each returns a dict at each t."""

import numpy as np


class DiurnalTemperature:
    """Full hourly cycle with day/night light flag."""

    def __init__(self, T_mean=20.0, amplitude=10.0, day_fraction=0.5, period=24.0):
        self.T_mean = T_mean
        self.amplitude = amplitude
        self.day_fraction = day_fraction
        self.period = period

    def __call__(self, t):
        T = self.T_mean + self.amplitude * np.sin(2 * np.pi * t / self.period)
        phase = (t % self.period) / self.period
        light = 1.0 if phase < self.day_fraction else 0.0
        return {'temperature': T, 'light': light}


class AggregatedForcingWrapper:
    """Replace temperature with its mean, keep the light cycle."""

    def __init__(self, full_forcing, T_mean):
        self.full_forcing = full_forcing
        self.T_mean = T_mean

    def __call__(self, t):
        raw = self.full_forcing(t)
        return {'temperature': self.T_mean, 'light': raw['light']}


class RampForcing:
    """Temperature ramps linearly T_start -> T_end over duration; diurnal on top."""

    def __init__(self, T_start=20.0, T_end=40.0, duration=100.0,
                 amplitude=5.0, day_fraction=0.5, period=24.0):
        self.T_start = T_start
        self.T_end = T_end
        self.duration = duration
        self.amplitude = amplitude
        self.day_fraction = day_fraction
        self.period = period

    def __call__(self, t):
        if t <= self.duration:
            trend = self.T_start + (self.T_end - self.T_start) * t / self.duration
        else:
            trend = self.T_end
        diurnal = self.amplitude * np.sin(2 * np.pi * t / self.period)
        T = trend + diurnal
        phase = (t % self.period) / self.period
        light = 1.0 if phase < self.day_fraction else 0.0
        return {'temperature': T, 'light': light}


class TrendForcing:
    """Constant diurnal + slow linear trend."""

    def __init__(self, T_start=20.0, trend_rate=0.02, amplitude=10.0,
                 day_fraction=0.5, period=24.0, duration=None):
        self.T_start = T_start
        self.trend_rate = trend_rate
        self.amplitude = amplitude
        self.day_fraction = day_fraction
        self.period = period
        # `duration` accepted for API compatibility; unused (open-ended trend)
        self.duration = duration

    def __call__(self, t):
        trend = self.T_start + self.trend_rate * t
        diurnal = self.amplitude * np.sin(2 * np.pi * t / self.period)
        T = trend + diurnal
        phase = (t % self.period) / self.period
        light = 1.0 if phase < self.day_fraction else 0.0
        return {'temperature': T, 'light': light}


class StochasticForcing:
    """Diurnal cycle plus Gaussian noise."""

    def __init__(self, T_mean=20.0, amplitude=10.0, noise_std=2.0,
                 day_fraction=0.5, period=24.0, seed=42):
        self.T_mean = T_mean
        self.amplitude = amplitude
        self.noise_std = noise_std
        self.day_fraction = day_fraction
        self.period = period
        self.rng = np.random.default_rng(seed)

    def __call__(self, t):
        diurnal = self.amplitude * np.sin(2 * np.pi * t / self.period)
        T = self.T_mean + diurnal + self.rng.normal(0, self.noise_std)
        phase = (t % self.period) / self.period
        light = 1.0 if phase < self.day_fraction else 0.0
        return {'temperature': T, 'light': light}


class FatTailedForcing:
    """Diurnal cycle plus Student's t noise. Heavy tails -> extreme heatwaves."""

    def __init__(self, T_mean=20.0, amplitude=8.0, df=3, scale=3.0,
                 day_fraction=0.5, period=24.0, seed=123):
        self.T_mean = T_mean
        self.amplitude = amplitude
        self.df = df
        self.scale = scale
        self.day_fraction = day_fraction
        self.period = period
        self.rng = np.random.default_rng(seed)

    def __call__(self, t):
        diurnal = self.amplitude * np.sin(2 * np.pi * t / self.period)
        noise = self.rng.standard_t(self.df) * self.scale
        T = self.T_mean + diurnal + noise
        phase = (t % self.period) / self.period
        light = 1.0 if phase < self.day_fraction else 0.0
        return {'temperature': T, 'light': light}
