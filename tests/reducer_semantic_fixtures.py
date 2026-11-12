"""Authored multi-domain examples and a deliberately limited deterministic rubric.

These are labelled witnesses, not model outputs or an entailment evaluator.
"""

import re

from tests.performance.fixtures import pdf

DOMAINS = {
    "science": {
        "pages": [
            "The study tests compound C1 in algae cultures.",
            "C1 reduced growth by 12% at 20 C over seven days.",
            "The experiment used 30 cultures; field safety was not tested.",
            "Results at 20 C do not establish effects at other temperatures.",
        ],
        "summary": (
            (
                "In 30 algae cultures, compound C1 reduced growth by 12% at 20 C over "
                "seven days. Field safety was not tested; effects at other temperatures are not established."
            ),
        ),
        "findings": ["C1", "algae", "12%", "20 C", "seven days", "30"],
        "qualifications": [
            "Field safety",
            "other temperatures",
            "not tested",
            "not established",
        ],
        "unsupported": "C1 is safe outdoors at every temperature.",
    },
    "regulation": {
        "pages": [
            "Draft tank guidance takes effect in 2027 and is not yet binding.",
            "The permit holder must inspect tank T7 monthly under this guidance.",
            "Inspection reports must reach the regulator within 10 days.",
            "Emergency shutdown may precede notice; this is an exception to prior notice.",
        ],
        "summary": (
            (
                "The draft 2027 guidance is not yet binding. It requires monthly T7 "
                "inspections and reports to the regulator within 10 days; emergency "
                "shutdown may precede notice."
            ),
        ),
        "findings": ["2027", "T7", "monthly", "regulator", "10 days"],
        "qualifications": [
            "draft",
            "not yet binding",
            "emergency",
            "may precede notice",
        ],
        "unsupported": "The guidance already imposes criminal penalties.",
    },
}


def valve_case():
    """Use the unchanged original phase17h-pdf/1 four-page source, seed 1708."""
    raw, manifest = pdf(4, seed=1708)
    pages = ["\n".join(p["lines"]) for p in manifest["expected"]]
    groups = []
    for number, page in enumerate(pages, 1):
        valves = re.findall(r"inspect valve (\d{4})", page)
        groups.append(f"unit {number:04d}: {', '.join(valves)}")
    return (
        raw,
        manifest,
        {
            "pages": pages,
            "summary": (
                "Pre-operation valve inspections cover " + "; ".join(groups[:2]) + ".",
                "The same inspection requirement covers " + "; ".join(groups[2:]) + ".",
            ),
            "findings": re.findall(r"inspect valve (\d{4})", "\n".join(pages)),
            "qualifications": ["Pre-operation"],
            "unsupported": "All valves are certified safe without inspection.",
        },
    )


def rubric_checks(text, case):
    """Observable fixture labels only; arbitrary unsupported prose needs review."""
    lowered = text.casefold()
    return {
        "important_information": all(x.casefold() in lowered for x in case["findings"]),
        "qualifications": all(x.casefold() in lowered for x in case["qualifications"]),
        "standalone_content": not re.search(
            r"\b(?:processed|wrappers?|child claims?|evidence array)\b", lowered
        ),
        "known_unsupported_conclusion_absent": case["unsupported"].casefold()
        not in lowered,
    }
