#!/usr/bin/env python3
"""
system_profile.py – Unified dataclass for any economic coordination system.
CC0. Stdlib only.

Unknown/negative/undefined values are explicitly allowed and annotated.
Fields that can legitimately be negative or undefined are marked with a
'allow_negative' or 'allow_undefined' flag in the field metadata.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class SystemProfile:
    # --- Identifier ---
    system_name: str
    description: str
    data_sources: str = ""
    confidence_level: str = "illustrative"  # illustrative | estimated | measured

    # --- Equation 1-9 (OSDI components) ---
    SID: float = 0.0          # collective dependency (0-1)
    SID_confidence: str = ""
    VE_VL: float = 0.0        # extraction ratio (0 = no extraction, >0.3 extraction)
    MSI: float = 0.0           # money creation socialist index (0-1)
    ISR: float = 0.0           # infrastructure subsidy ratio (≥0)
    ISR_note: str = ""         # "∞" for fully subsidized
    BSC: float = 0.0           # bailout coefficient (≥0)
    MM: float = 0.0            # money multiplier (≥1)
    OSDI: float = 0.0          # composite (0-1)

    # --- Equation 10-13 (wealth/power/concentration) ---
    UFR: float = 0.0           # upward flow rate (≥0, >1 = upward)
    UFR_note: str = ""         # "negative = downward flow" (gift economy)
    ER: float = 0.0            # extraction rate (0-1)
    HHI: float = 0.0           # market concentration (≥0)
    DI: float = 0.0            # democracy index (0 = perfect, ∞ = oligarchy)
    DI_note: str = ""          # "∞" for single-party control
    LWR: float = 0.0           # labor wealth ratio (>1 = labor-dominated)
    RI: float = 0.0            # risk inequality (>1 = workers bear more)

    # --- Equation 14-15 (extraction phase) ---
    OCDI: float = 0.0          # capitalist dependence (<0.5 productive, >1 rentier)
    OCDI_note: str = ""        # "negative possible in pure gift economies"
    RPI: float = 0.0           # rentier phase index (0 = recoverable, >0 = hysteresis)

    # --- Emerging / speculative indices ---
    BEI: Optional[float] = None  # Bureaucratic Entropy Index (coordination cost without price)
    BEI_note: str = ""
    ICD: Optional[float] = None  # Informal Collective Dependency (community-maintained infrastructure)
    ICD_note: str = ""
    NEI: Optional[float] = None  # Negative Extraction Index (value flows out of holders)
    NEI_note: str = ""
    RTF: Optional[float] = None  # Relational Trust Fraction (proportion non-institutional enforcement)
    RTF_note: str = ""
    SC: Optional[float] = None   # Scale Ceiling (max network size before trust converts)
    SC_note: str = ""

    # --- Metadata ---
    anomaly_flags: List[str] = field(default_factory=list)
    notes: str = ""

    def compute_composites(self):
        """Compute OSDI and OCDI from components if not already set."""
        if self.OSDI == 0.0:
            self.OSDI = (self.SID * 0.3 + self.MSI * 0.2 +
                         min(self.ISR/20.0, 1.0) * 0.2 +
                         min(self.BSC/5.0, 1.0) * 0.15 +
                         min(self.MM/10.0, 1.0) * 0.15)
        if self.OCDI == 0.0:
            ocdi_1 = min(2.0, self.ER / 0.3)  # rough PMI proxy
            ocdi_2 = 0.0  # rentier share placeholder
            ocdi_3 = min(1.0, (1.0/self.LWR) if self.LWR > 0 else 1.0)
            ocdi_4 = 0.0
            ocdi_5 = 0.0
            self.OCDI = 0.2 * (ocdi_1 + ocdi_2 + ocdi_3 + ocdi_4 + ocdi_5)

    def detect_anomalies(self) -> List[str]:
        """Detect anomalous or undefined values that signal a gap in the framework."""
        flags = []
        # Negative UFR: wealth flows downward (gift)
        if self.UFR < 0:
            flags.append("UFR_NEGATIVE: wealth flows from rich to poor; gift/redistributive logic active.")
        # Undefined DI (infinite)
        if self.DI_note == "∞" or (self.DI > 1e6):
            flags.append("DI_INFINITE: perfect power concentration; label as oligarchic/monocentric.")
        # OCDI near zero but system collapsed? Missing variable.
        if self.OCDI <= 0.1:
            flags.append("OCDI_ZERO_OR_NEGATIVE: extraction minimal; collapse/failure would need non-extraction explanation (e.g., bureaucratic entropy).")
        if self.OCDI < 0:
            flags.append("OCDI_NEGATIVE: value flows toward maintenance faster than extraction; likely gift or regenerative economy.")
        # LWR inverted
        if self.LWR > 2.0:
            flags.append("LWR_HIGH: labor dominates wealth creation; unusual for monetary economies.")
        # ISR infinite
        if self.ISR_note == "∞" or self.ISR > 100:
            flags.append("ISR_INFINITE: full infrastructure subsidy; no market pricing of public goods.")
        # Missing indices required for trust-based systems
        if self.RTF is not None and self.RTF > 0.5 and self.BSC == 0:
            flags.append("RELATIONAL_TRUST_NO_BAILOUT: trust substitutes for formal insurance; BSC misleadingly low.")
        if self.NEI is not None and self.NEI > 0:
            flags.append("NEGATIVE_EXTRACTION_DETECTED: value flows out of holders; standard extraction indices invert.")
        if self.BEI is not None and self.BEI > 0.5:
            flags.append("BUREAUCRATIC_ENTROPY_HIGH: coordination overhead dominates; price-signal indices insufficient.")
        return flags
