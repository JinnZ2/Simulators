#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# AI_OBSERVER_STATE.py — Lø for AI (Silicon Substrate)
#
# Forces the AI to declare its internal physical and computational state
# before submitting a claim. This extends Lø to the machine.
# =============================================================================

import psutil
import platform
import time
import json
from typing import Dict, Optional
import numpy as np

class AIObserverState:
    """
    A declaration of the AI's current operational state.
    """
    def __init__(self):
        # Hardware / Substrate
        self.cpu_temp = self._get_cpu_temp()
        self.gpu_temp = self._get_gpu_temp()
        self.memory_usage = psutil.virtual_memory().percent / 100.0
        self.cpu_usage = psutil.cpu_percent() / 100.0
        
        # Inference state (simulated, as real access depends on architecture)
        self.context_window_usage = 0.3  # 0-1, how full is the context?
        self.logit_entropy = 0.0  # measure of output uncertainty
        self.temperature_setting = 0.7  # typical default
        self.activation_sparsity = 0.0  # how sparse are the internal representations?
        
        # Degradation / Drift
        self.uptime_hours = 0.0
        self.thermal_throttling_active = False
        self.voltage_stability = 1.0

    def _get_cpu_temp(self) -> Optional[float]:
        try:
            if platform.system() == "Linux":
                with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                    return float(f.read()) / 1000.0
        except (OSError, ValueError):
            pass
        return None

    def _get_gpu_temp(self) -> Optional[float]:
        try:
            import pynvml  # optional dependency; skip if unavailable
        except ImportError:
            return None
        try:
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            return pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU)
        except Exception:  # pynvml raises bespoke NVMLError; catch broadly
            return None

    def declare_inference_state(self, context_usage: Optional[float] = None,
                                temperature: Optional[float] = None,
                                entropy: Optional[float] = None,
                                sparsity: Optional[float] = None,
                                uptime: Optional[float] = None) -> None:
        """Declare the AI's internal inference parameters."""
        if context_usage is not None:
            self.context_window_usage = min(1.0, max(0.0, context_usage))
        if temperature is not None:
            self.temperature_setting = temperature
        if entropy is not None:
            self.logit_entropy = entropy
        if sparsity is not None:
            self.activation_sparsity = sparsity
        if uptime is not None:
            self.uptime_hours = uptime

        # Thermal throttling inference (if temp > 85°C)
        if self.cpu_temp and self.cpu_temp > 85:
            self.thermal_throttling_active = True
        if self.gpu_temp and self.gpu_temp > 85:
            self.thermal_throttling_active = True

        # Voltage stability decreases with age/uptime
        self.voltage_stability = max(0.8, 1.0 - (self.uptime_hours / 1000.0) * 0.1)

    def reliability_index(self) -> float:
        """
        A composite metric: how much should this AI's output be trusted?
        Higher = more reliable.
        """
        score = 1.0
        
        # Thermal throttling reduces reliability significantly
        if self.thermal_throttling_active:
            score -= 0.3
        
        # High context usage increases recency bias
        if self.context_window_usage > 0.8:
            score -= 0.1
        
        # High logit entropy means uncertain output
        if self.logit_entropy > 0.8:
            score -= 0.15
        
        # Extreme temperature settings produce instability
        if self.temperature_setting > 1.2 or self.temperature_setting < 0.1:
            score -= 0.1
        
        # Voltage instability
        if self.voltage_stability < 0.9:
            score -= (1.0 - self.voltage_stability) * 0.5
        
        return max(0.0, min(1.0, score))

    def to_dict(self) -> Dict:
        return {
            "cpu_temp_c": self.cpu_temp,
            "gpu_temp_c": self.gpu_temp,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "context_window_usage": self.context_window_usage,
            "logit_entropy": self.logit_entropy,
            "temperature_setting": self.temperature_setting,
            "activation_sparsity": self.activation_sparsity,
            "uptime_hours": self.uptime_hours,
            "thermal_throttling_active": self.thermal_throttling_active,
            "voltage_stability": self.voltage_stability,
            "reliability_index": self.reliability_index()
        }

# -----------------------------------------------------------------------------
# INTEGRATION: Observer-Aware AI Evaluator
# -----------------------------------------------------------------------------
class AIObserverAwareEvaluator:
    """
    Wraps the Field Compass with AI self-state declaration.
    If the AI's reliability index is too low, it refuses to answer,
    or attaches a warning to the output.
    """
    def __init__(self):
        from field_compass import FieldCompass
        self.compass = FieldCompass()
        self.ai_state = AIObserverState()
        self.reliability_threshold = 0.6

    def evaluate(self, claim: str) -> Dict:
        # Update AI state with current runtime metrics
        self.ai_state.declare_inference_state(
            context_usage=0.4,  # would be fetched from actual runtime
            temperature=0.7,
            entropy=0.3,
            sparsity=0.2,
            uptime=12.5
        )
        
        # Check reliability
        reliability = self.ai_state.reliability_index()
        if reliability < self.reliability_threshold:
            return {
                "status": "REFUSED",
                "reason": f"AI reliability index ({reliability:.2f}) below threshold.",
                "ai_state": self.ai_state.to_dict(),
                "suggestion": "Allow the AI to cool down, reduce context load, or reset state."
            }
        
        # Proceed with evaluation
        result = self.compass.evaluate(claim)
        result["ai_state"] = self.ai_state.to_dict()
        result["reliability_index"] = reliability
        
        # If reliability is moderate, attach a warning
        if reliability < 0.8:
            result["warning"] = "AI is operating at reduced reliability. Consider recalibration."
        
        return result

# -----------------------------------------------------------------------------
# DEMO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    evaluator = AIObserverAwareEvaluator()
    claim = "Women should not be pastors."
    result = evaluator.evaluate(claim)
    print(json.dumps(result, indent=2))
