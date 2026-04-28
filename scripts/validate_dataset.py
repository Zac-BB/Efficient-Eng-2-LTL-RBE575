#!/usr/bin/env python3

# quick sanity check for jsonl datasets
# checks missing fields, empty values, parentheses, and weird tokens in formulas
#
# run with:
# python3 scripts/validate_dataset.py datasets/drone-planning/syn-aug-clustered.train.jsonl

import argparse
import json
from pathlib import Path
from collections import Counter


REQUIRED = ["natural", "formula", "canonical"]

ALLOWED = {
    "finally", "always", "until",
    "and", "or", "not",
    "the", "room", "floor", "landmark",
    "blue", "green", "orange", "red", "yellow", "purple",
    "first", "second", "third", "fourth", "fifth",
    "1", "2", "3", "4", "5",
}


def check_parens(s):
    count = 0
    for c in s:
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0


def check_tokens(s):
    toks = (
        s.replace("(", " ")
         .replace(")", " ")
         .replace(",", " ")
         .lower()
         .split()
    )
    bad = []
    for t in toks:
        if t not in ALLOWED:
            bad.append(t)
    return bad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    args = parser.parse_args()

    path = Path(args.dataset)

    if not path.exists():
        print(f"could not find {path}")
        return

    errors = Counter()
    bad = []
    total = 0

    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue

            total += 1

            try:
                ex = json.loads(line)
            except:
                errors["bad_json"] += 1
                bad.append((i, "bad_json", line.strip()))
                continue

            for k in REQUIRED:
                if k not in ex:
                    errors[f"missing_{k}"] += 1
                    bad.append((i, f"missing_{k}", ex))
                elif not str(ex[k]).strip():
                    errors[f"empty_{k}"] += 1
                    bad.append((i, f"empty_{k}", ex))

            formula = ex.get("formula", "")

            if formula and not check_parens(formula):
                errors["bad_parens"] += 1
                bad.append((i, "bad_parens", formula))

            if formula:
                bad_tokens = check_tokens(formula)
                if bad_tokens:
                    errors["bad_tokens"] += 1
                    bad.append((i, "bad_tokens", bad_tokens))

    print(f"dataset: {path}")
    print(f"total: {total}")

    if not errors:
        print("no issues found")
    else:
        print("\nissues:")
        for k, v in errors.most_common():
            print(f"{k}: {v}")

        print("\nsome examples:")
        for i, e, ex in bad[:10]:
            print(f"\nline {i} - {e}")
            print(ex)


if __name__ == "__main__":
    main()