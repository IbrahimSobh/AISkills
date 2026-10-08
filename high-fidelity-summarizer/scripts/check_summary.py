#!/usr/bin/env python3
"""
Mechanical verification for high-fidelity-summarizer output.

Checks:
  1. Word count vs. the 22%-28% compression band (target 25%)
  2. Compression ratio (PASS only if 22% <= ratio <= 28%)
  3. Capitalized terms/acronyms found in the source but missing from the summary
     (a proxy for "did we drop a name, acronym, file name, or term of art")

This does not replace a human/model read-through for tone, structural order,
or hallucination checks -- it only catches what's mechanically countable.
"""

import argparse
import re
import sys

MIN_RATIO = 0.22
MAX_RATIO = 0.28


def word_count(text: str) -> int:
    return len(text.split())


def extract_terms(text: str) -> set:
    """Pull out likely named entities / acronyms: capitalized words,
    ALLCAPS acronyms, and numbers with units, deduplicated case-sensitively."""
    # Capitalized words (not sentence-initial only -- this is a heuristic, not NLP)
    caps = re.findall(r"\b[A-Z][a-zA-Z0-9\-]{1,}\b", text)
    # Standalone acronyms (2+ uppercase letters)
    acronyms = re.findall(r"\b[A-Z]{2,}\b", text)
    # Numbers with a unit/percent attached, e.g. "20%", "3.5x", "$400M"
    metrics = re.findall(r"\$?\d[\d,.]*\s?(?:%|x|k|K|M|B|bn|tn)\b", text)
    return set(caps) | set(acronyms) | set(metrics)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Path to source text file")
    parser.add_argument("--summary", required=True, help="Path to summary text file")
    args = parser.parse_args()

    with open(args.source, "r", encoding="utf-8") as f:
        source = f.read()
    with open(args.summary, "r", encoding="utf-8") as f:
        summary = f.read()

    src_wc = word_count(source)
    sum_wc = word_count(summary)
    ratio = sum_wc / src_wc if src_wc else 0
    low = round(src_wc * MIN_RATIO)
    high = round(src_wc * MAX_RATIO)

    print(f"Source words:   {src_wc}")
    print(f"Summary words:  {sum_wc}")
    print(f"Compression:    {ratio:.1%} of source")
    print(f"Allowed band:   {low}-{high} words (22%-28%)")

    if ratio < MIN_RATIO:
        length_ok = False
        print(f"LENGTH: FAIL    too short -- add {low - sum_wc} word(s) of restored detail")
    elif ratio > MAX_RATIO:
        length_ok = False
        print(f"LENGTH: FAIL    too long -- cut {sum_wc - high} word(s)")
    else:
        length_ok = True
        print("LENGTH: PASS    inside the 22%-28% band")

    src_terms = extract_terms(source)
    sum_terms = extract_terms(summary)
    missing = sorted(src_terms - sum_terms)

    print(f"\nTerms/acronyms/metrics found in source: {len(src_terms)}")
    if missing:
        print(f"Present in source but NOT found verbatim in summary ({len(missing)}):")
        for term in missing:
            print(f"  - {term}")
        print("(Not all of these need to survive -- check against your extracted")
        print(" 'core thesis + supporting pillars' from step 2. This just flags")
        print(" candidates worth a second look.)")
    else:
        print("All detected source terms/acronyms/metrics appear in the summary.")

    return 0 if length_ok else 1


if __name__ == "__main__":
    sys.exit(main())
