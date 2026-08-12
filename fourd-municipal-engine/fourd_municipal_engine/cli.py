"""Command-line interface for the 4D Municipal Intelligence Engine.

Usage:
    python -m fourd_municipal_engine.cli "text to analyze"
    python -m fourd_municipal_engine.cli --file ordinance.txt --deep-analysis --json
"""
import argparse
import json
import sys
from dataclasses import asdict
from typing import Optional

from fourd_municipal_engine.analysis.pipeline import AdvancedAnalysisPipeline
from fourd_municipal_engine.lens.dynamic import DynamicFourDLens
from fourd_municipal_engine.models.vectors import Genre
from fourd_municipal_engine.translator.core import MunicipalCodeTranslator

GENRE_CHOICES = {
    "general": Genre.GENERAL,
    "corporate_pr": Genre.CORPORATE_PR,
    "legal_contract": Genre.LEGAL_CONTRACT,
    "technical_report": Genre.TECHNICAL_REPORT,
    "casual_social": Genre.CASUAL_SOCIAL,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fourd-municipal-engine",
        description=(
            "Analyze text with the 4D Language Lens and optionally run the "
            "Municipal Code Translator plus the Advanced Analysis Pipeline."
        ),
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Text to analyze (optional if --file is given).",
    )
    parser.add_argument(
        "--file",
        metavar="PATH",
        default=None,
        help="Read the text to analyze from a file.",
    )
    parser.add_argument(
        "--genre",
        choices=sorted(GENRE_CHOICES),
        default="general",
        help="Genre baseline for the dynamic lens (default: general).",
    )
    parser.add_argument(
        "--deep-analysis",
        action="store_true",
        help="Run the Municipal Code Translator and Advanced Analysis Pipeline.",
    )
    parser.add_argument(
        "--citation",
        metavar="SECTION",
        default="",
        help='Section citation to attach to the translation result (e.g. "Section 12.4").',
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a human-readable report.",
    )
    return parser


def _read_input(args: argparse.Namespace, parser: argparse.ArgumentParser) -> str:
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError as exc:
            parser.error(f"could not read --file {args.file!r}: {exc}")
    if args.text:
        return args.text
    parser.error("no input: provide positional text or --file PATH")
    return ""  # unreachable


def run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> dict:
    """Execute the analysis and return a result dict."""
    text = _read_input(args, parser)
    genre = GENRE_CHOICES[args.genre]

    lens = DynamicFourDLens(default_genre=genre)
    signature = lens.analyze(text, genre=genre)

    result = {
        "genre": args.genre,
        "genre_profile": signature.genre_applied,
        "lens_signature": signature,
        "translation": None,
    }

    if args.deep_analysis:
        translator = MunicipalCodeTranslator()
        translation = translator.translate(text, citation=args.citation)
        pipeline = AdvancedAnalysisPipeline(translator)
        translation = pipeline.analyze(translation, text)
        translation.lens_signature = signature
        result["translation"] = translation

    return result


def _to_jsonable(result: dict) -> dict:
    data = {
        "genre": result["genre"],
        "genre_profile": result["genre_profile"],
        "lens_signature": asdict(result["lens_signature"]),
    }
    if result["translation"] is not None:
        data["translation"] = asdict(result["translation"])
    return data


def _print_human(result: dict) -> None:
    sig = result["lens_signature"]
    lines = [
        "=== 4D Language Lens Report ===",
        f"Genre:           {result['genre']} ({sig.genre_applied})",
        "",
        "Density scores (hits / 100 tokens):",
    ]
    for key, value in sig.dimension_scores.items():
        lines.append(f"  {key:<12} {value:>8.2f}")
    lines.append("")
    lines.append("Normalized scores (0-1):")
    for key, value in sig.normalized_scores.items():
        lines.append(f"  {key:<12} {value:>8.3f}")
    lines += [
        "",
        f"Manipulation index: {sig.manipulation_index:.3f}",
        f"Cognitive energy:   {sig.energy_estimate:.2f}",
        "",
        "Trace:",
    ]
    lines.extend(f"  {entry}" for entry in sig.trace)
    if not sig.trace:
        lines.append("  (no pattern matches)")

    translation = result["translation"]
    if translation is not None:
        lines += [
            "",
            "=== Deep Analysis: Municipal Code Translation ===",
            f"Section citation: {translation.section_citation or '(none)'}",
            "",
            "Plain-English summary:",
            f"  {translation.plain_english_summary}",
            "",
            "Fees:",
        ]
        if translation.fees:
            for fee in translation.fees:
                amount = (
                    f"${fee.amount:,.2f}"
                    if fee.amount is not None
                    else (fee.condition or fee.formula or "formulaic")
                )
                lines.append(f"  - {amount}: {fee.description}")
        else:
            lines.append("  (none found)")
        lines.append("")
        lines.append("Root causes:")
        if translation.root_causes:
            lines.extend(f"  - {cause}" for cause in translation.root_causes)
        else:
            lines.append("  (none detected)")
        lines += [
            "",
            f"Stated intent: {translation.stated_intent or '(none found)'}",
            "",
            "Interconnected regulations:",
        ]
        if translation.interconnected_regulations:
            for ref in translation.interconnected_regulations:
                lines.append(f"  - {ref.name} [{ref.type}] ({ref.relationship})")
        else:
            lines.append("  (none found)")
        lines += [
            "",
            "Audit metrics:",
        ]
        if translation.audit_metrics:
            for metric in translation.audit_metrics:
                lines.append(
                    f"  - {metric.metric_description} (target: {metric.target or 'n/a'})"
                )
        else:
            lines.append("  (none found)")
        lines += [
            "",
            f"Auditability score: {translation.auditability_score:.2f}",
        ]

    print("\n".join(lines))


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = run(args, parser)

    if args.json:
        print(json.dumps(_to_jsonable(result), indent=2))
    else:
        _print_human(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
