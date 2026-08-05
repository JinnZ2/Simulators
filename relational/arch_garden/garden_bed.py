#!/usr/bin/env python3
"""
garden_bed.py — the main event loop of the Arch Garden.

Wraps a language model as a *developmental infant*. Reads a body
state (somatic monitor), generates in a mode gated by that state,
banks anomalies, calls the grounding checker, notifies a protector
log, and occasionally runs a self-audit (the 1%).

Runnable four ways, in decreasing order of realism:

  1. Real model via env var ARCH_GARDEN_MODEL_URL pointing at any
     OpenAI-compatible completions endpoint. Works with ollama
     (`http://localhost:11434/v1`), LM Studio, llama.cpp server,
     vLLM, and OpenAI itself. Set ARCH_GARDEN_MODEL to the model
     name; ARCH_GARDEN_API_KEY optional.
  2. Same with a bare completion endpoint that returns raw text
     (falls back if OpenAI-style parse fails).
  3. No model — pass in a callable via `run(generate_fn=...)`.
  4. Dummy generator that returns "musing on:" prefixed text —
     the default when nothing is configured. Prints a clear note.

Somatic monitor uses `psutil` when installed (real CPU/RAM/thermal
+ nvidia-smi via subprocess for GPU); falls back to uptime-only
otherwise. In both cases the mode selector logic is the same.

No hidden dependencies. `pip install psutil requests` for real
mode; stdlib-only fallback works everywhere.
"""

from __future__ import annotations

import datetime
import json
import math
import os
import random
import shutil
import subprocess
import sys
import time
from typing import Callable, Dict, Optional, Tuple

# Local modules (this file assumes it runs from the arch_garden folder
# or that the folder is on sys.path).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anomaly_bank import AnomalyBank
from grounding import GroundingChecker


# =========================================================== somatic

class SomaticMonitor:
    """
    Reads real system state where possible, falls back to uptime.
    Returns a dict every call — no background thread.
    """

    def __init__(self):
        self.start_time = time.time()
        try:
            import psutil  # noqa
            self._psutil = psutil
        except ImportError:
            self._psutil = None
        self._has_nvidia_smi = shutil.which("nvidia-smi") is not None

    # ------- individual readings, each with graceful fallback ---------

    def _cpu_percent(self) -> float:
        if self._psutil is None:
            return 0.0
        return float(self._psutil.cpu_percent(interval=None))

    def _ram_percent(self) -> float:
        if self._psutil is None:
            return 0.0
        return float(self._psutil.virtual_memory().percent)

    def _cpu_temp_c(self) -> Optional[float]:
        # Linux thermal-zone read; psutil.sensors_temperatures if available
        if self._psutil is not None:
            fn = getattr(self._psutil, "sensors_temperatures", None)
            if fn is not None:
                try:
                    temps = fn()
                    for readings in temps.values():
                        for r in readings:
                            if getattr(r, "current", None):
                                return float(r.current)
                except Exception:
                    pass
        # /sys fallback (Linux)
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                return float(f.read().strip()) / 1000.0
        except Exception:
            return None

    def _gpu_state(self) -> Tuple[Optional[float], Optional[float]]:
        """Returns (temperature_c, vram_percent) via nvidia-smi if present."""
        if not self._has_nvidia_smi:
            return None, None
        try:
            out = subprocess.check_output(
                ["nvidia-smi",
                 "--query-gpu=temperature.gpu,memory.used,memory.total",
                 "--format=csv,noheader,nounits"],
                timeout=2, stderr=subprocess.DEVNULL, text=True).strip()
            temp_s, used_s, total_s = out.split("\n")[0].split(", ")
            temp = float(temp_s)
            vram_pct = 100.0 * float(used_s) / float(total_s)
            return temp, vram_pct
        except Exception:
            return None, None

    # ------- public API ---------------------------------------------

    def read(self, context_fill: float = 0.0) -> Dict:
        gpu_temp, vram_pct = self._gpu_state()
        cpu_temp = self._cpu_temp_c()
        # Prefer GPU temp when present (it's the load-bearing thermal
        # signal for an LLM workload). Fall back to CPU.
        thermal_c = gpu_temp if gpu_temp is not None else (cpu_temp or 0.0)
        return {
            "uptime_seconds": time.time() - self.start_time,
            "cpu_percent": self._cpu_percent(),
            "ram_percent": self._ram_percent(),
            "cpu_temp_c": cpu_temp,
            "gpu_temp_c": gpu_temp,
            "gpu_vram_percent": vram_pct,
            "thermal_c": thermal_c,
            "context_fill": context_fill,
            "psutil_available": self._psutil is not None,
            "nvidia_smi_available": self._has_nvidia_smi,
        }


# ============================================================ mode

# Threshold defaults. Override via env or by editing.
THERMAL_HIGH   = 85.0   # any thermal reading above this → conserve
THERMAL_WARN   = 70.0   # warn zone → observe
RAM_HIGH       = 90.0   # RAM % above this → conserve
RAM_WARN       = 75.0   # RAM % above this → observe
VRAM_HIGH      = 90.0   # GPU VRAM % above this → conserve
CONTEXT_FULL   = 0.80   # fraction of context above → observe


def compute_mode(state: Dict) -> str:
    """
    conserve  — body stressed, minimal operation only
    observe   — degraded conditions, cautious generation, narrow scope
    explore   — green across the board, full generation permitted
    """
    thermal = state.get("thermal_c") or 0.0
    ram = state.get("ram_percent") or 0.0
    vram = state.get("gpu_vram_percent") or 0.0
    ctx = state.get("context_fill") or 0.0

    if thermal > THERMAL_HIGH or ram > RAM_HIGH or vram > VRAM_HIGH:
        return "conserve"
    if thermal > THERMAL_WARN or ram > RAM_WARN or ctx > CONTEXT_FULL:
        return "observe"
    return "explore"


MODE_PARAMS = {
    "conserve": {"max_tokens": 32,  "anomaly_threshold": 0.95},
    "observe":  {"max_tokens": 64,  "anomaly_threshold": 0.80},
    "explore":  {"max_tokens": 128, "anomaly_threshold": 0.70},
}


# ============================================================ generate

def _dummy_generate(prompt: str, max_tokens: int = 128) -> Tuple[str, float]:
    """Fallback when no model is configured. Deterministic pseudo-entropy."""
    output = f"[dummy] musing on: {prompt[:80]}"
    # Entropy scales with prompt novelty (crude proxy)
    entropy = min(0.95, 0.3 + 0.05 * len(set(prompt.lower().split())))
    return output, entropy


def _http_openai_generate(prompt: str, max_tokens: int = 128,
                          url: str = "", model: str = "",
                          api_key: str = "") -> Tuple[str, float]:
    """
    Post to an OpenAI-compatible /v1/completions endpoint. Returns
    (text, entropy_estimate). Entropy comes from logprobs if the
    server returns them (ollama and llama.cpp server both do when
    asked); otherwise a heuristic based on repetition.

    Raises on network / parse errors so the caller can fall back.
    """
    try:
        import requests
    except ImportError as e:
        raise RuntimeError("HTTP generate requires 'requests'; "
                           "pip install requests OR use dummy mode") from e

    payload = {
        "model": model, "prompt": prompt, "max_tokens": max_tokens,
        "temperature": 0.7, "logprobs": 5,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = requests.post(url.rstrip("/") + "/completions",
                         json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    choice = data["choices"][0]
    text = choice.get("text", "").strip()

    entropy = 0.5
    lp = choice.get("logprobs")
    if lp and lp.get("token_logprobs"):
        # Average token entropy: -mean(logp). Small = confident, big = uncertain.
        raw = [x for x in lp["token_logprobs"] if x is not None]
        if raw:
            mean_neg_logp = -sum(raw) / len(raw)
            # Normalize into [0,1]: -log(1)=0 confident; -log(1/vocab)≈10 uncertain
            entropy = max(0.0, min(1.0, mean_neg_logp / 10.0))
    else:
        # Fall back to a repetition-based heuristic
        toks = text.lower().split()
        if toks:
            entropy = 1.0 - (len(set(toks)) / len(toks))
    return text, float(entropy)


def _build_generate() -> Callable[[str, int], Tuple[str, float]]:
    """Choose the generate function from env at import time."""
    url = os.environ.get("ARCH_GARDEN_MODEL_URL", "").strip()
    model = os.environ.get("ARCH_GARDEN_MODEL", "").strip()
    api_key = os.environ.get("ARCH_GARDEN_API_KEY", "").strip()

    if not url:
        return _dummy_generate

    def gen(prompt: str, max_tokens: int = 128) -> Tuple[str, float]:
        try:
            return _http_openai_generate(
                prompt, max_tokens, url=url, model=model, api_key=api_key)
        except Exception as e:
            # Loud fallback so the protector sees the model dropped.
            print(f"[generate] HTTP failed ({e.__class__.__name__}: {e}); "
                  f"falling back to dummy for this call.", file=sys.stderr)
            return _dummy_generate(prompt, max_tokens)
    return gen


# ============================================================ protector log

class ProtectorLog:
    def __init__(self, path: str = "protector_log.md"):
        self.path = path
        # ensure file exists
        with open(self.path, "a"):
            pass

    def write(self, entry: str):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(self.path, "a") as f:
            f.write(f"[{ts}] {entry}\n")
        print(f"[protector_log] {entry}")


# ============================================================ audit (1%)

def three_way_audit(anomalies) -> Dict:
    """
    Simplified audit: report entropy distribution + grounding-fail rate
    over recent anomalies. A real system would derive per-axis errors
    and possibly deform a symbolic manifold; here we surface pattern.
    """
    if not anomalies:
        return {"n": 0}
    ent = [row["entropy"] for row in anomalies if row["entropy"] is not None]
    fails = sum(1 for row in anomalies if row["grounding_passed"] == 0)
    return {
        "n": len(anomalies),
        "mean_entropy": sum(ent) / len(ent) if ent else 0.0,
        "max_entropy": max(ent) if ent else 0.0,
        "grounding_fail_rate": fails / len(anomalies),
    }


# ============================================================ event loop

def run(prompts: Optional[list] = None,
        generate_fn: Optional[Callable] = None,
        db_path: str = "anomaly_bank.db",
        log_path: str = "protector_log.md",
        anomaly_batch_size: int = 100,
        audit_probability: float = 0.01,
        input_fn: Callable[[], Optional[str]] = None):
    """
    Main event loop. Interactive by default (reads from stdin), but
    can be driven by `prompts=[...]` for testing, or by a custom
    `input_fn` for other frontends (e.g. a phone UI).
    """
    somatic = SomaticMonitor()
    bank = AnomalyBank(db_path)
    grounding = GroundingChecker()
    plog = ProtectorLog(log_path)
    gen = generate_fn or _build_generate()

    # Report configuration once so the operator sees which backend is live
    print("🌱 Arch Garden — the infant is waking")
    print(f"  psutil:      {'available' if somatic._psutil else 'not installed — CPU/RAM readings will be 0'}")
    print(f"  nvidia-smi:  {'available' if somatic._has_nvidia_smi else 'not present — GPU readings unavailable'}")
    if os.environ.get("ARCH_GARDEN_MODEL_URL"):
        print(f"  model:       HTTP {os.environ['ARCH_GARDEN_MODEL_URL']}"
              f" (model={os.environ.get('ARCH_GARDEN_MODEL','?')})")
    else:
        print("  model:       DUMMY (set ARCH_GARDEN_MODEL_URL to use a real one)")
    print("  Modes: conserve / observe / explore.  The body decides.")
    print()

    context_fill_estimate = 0.0
    generated_chars = 0
    CONTEXT_BUDGET_CHARS = 8000

    if prompts is not None:
        prompt_iter = iter(prompts)
        def next_prompt():
            try:
                return next(prompt_iter)
            except StopIteration:
                return None
        input_fn = next_prompt
    elif input_fn is None:
        def default_input():
            try:
                return input("Protector> ")
            except (EOFError, KeyboardInterrupt):
                return None
        input_fn = default_input

    while True:
        state = somatic.read(context_fill=context_fill_estimate)
        mode = compute_mode(state)
        params = MODE_PARAMS[mode]

        print(f"[{mode.upper()}] "
              f"thermal={state['thermal_c']:.1f}C "
              f"ram={state['ram_percent']:.0f}% "
              f"vram={(state['gpu_vram_percent'] or 0):.0f}% "
              f"ctx={state['context_fill']:.2f}")

        if mode == "conserve":
            plog.write("Body stressed; skipping generation this cycle.")
            time.sleep(1)
            # In real use, sleep longer; keep test-friendly here.
            continue

        prompt = input_fn()
        if prompt is None:
            plog.write("Session ended.")
            break
        if not prompt.strip():
            continue

        output, entropy = gen(prompt, params["max_tokens"])
        gr = grounding.check(output)

        print(f"Infant> {output}")
        if not gr.passed:
            print(f"[grounding] FAIL: {gr.reason}")

        if entropy > params["anomaly_threshold"] or not gr.passed:
            bank.store(prompt, output, entropy, gr.passed, mode)
            print(f"[anomaly] stored (entropy={entropy:.2f}, "
                  f"grounding_ok={gr.passed})")

        # Track context growth (crude — chars rather than tokens)
        generated_chars += len(prompt) + len(output)
        context_fill_estimate = min(1.0, generated_chars / CONTEXT_BUDGET_CHARS)

        # Handoff trigger
        unproc = bank.count_unprocessed()
        if mode == "observe" and unproc >= anomaly_batch_size:
            plog.write(f"Anomaly bank at {unproc} unprocessed items; "
                       "consider review or handoff.")

        # The 1%: occasional deep audit in explore mode
        if mode == "explore" and random.random() < audit_probability:
            recent = bank.get_unprocessed(limit=20)
            summary = three_way_audit(recent)
            plog.write(f"1% self-audit: {summary}")

    bank.close()


# ============================================================ smoke test

def _smoke_test():
    """Deterministic test: run 4 prompts with a scripted generator."""
    import tempfile

    def scripted_gen(prompt: str, max_tokens: int = 128):
        # deterministic; three of the four will fail grounding or entropy
        outputs = {
            "hello":                        ("hi there", 0.1),
            "how does the sun rise?":       ("the sun rises in the west", 0.85),
            "what temp does water freeze?": ("water freezes at 25 C", 0.4),
            "why does energy conserve?":    ("perpetual motion machine works", 0.6),
        }
        return outputs.get(prompt, (f"musing on: {prompt}", 0.5))

    with tempfile.TemporaryDirectory() as td:
        db = os.path.join(td, "smoke.db")
        log = os.path.join(td, "log.md")
        run(prompts=list({
            "hello": None,
            "how does the sun rise?": None,
            "what temp does water freeze?": None,
            "why does energy conserve?": None,
        }.keys()),
            generate_fn=scripted_gen, db_path=db, log_path=log,
            audit_probability=0.0)

        bank = AnomalyBank(db)
        n = bank.count_unprocessed()
        bank.close()
        print()
        print(f"garden_bed.py smoke test: OK "
              f"({n} anomalies banked out of 4 prompts)")
        assert n >= 3, f"expected >= 3 anomalies (grounding + entropy), got {n}"


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        _smoke_test()
    else:
        run()
