#!/usr/bin/env python3

# quick script to look at cluster distribution in a jsonl dataset
# prints counts + a few example rows per cluster
#
# run like:
# python3 scripts/analyze_clusters.py datasets/drone-planning/syn-aug-clustered.train.jsonl
#
# optional:
#   --examples N   (how many examples per cluster, default = 3)
#   --out PATH     (save output to a file)
#
# mostly just for sanity checking + grabbing numbers/examples for the report

import argparse
import json
from pathlib import Path
from collections import Counter, defaultdict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    parser.add_argument("--examples", type=int, default=3)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    dataset_path = Path(args.dataset)

    if not dataset_path.exists():
        print(f"Could not find dataset: {dataset_path}")
        return

    counts = Counter()
    examples = defaultdict(list)

    with dataset_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            ex = json.loads(line)
            cluster = ex.get("semantic_cluster", "NO_CLUSTER")

            counts[cluster] += 1

            if len(examples[cluster]) < args.examples:
                examples[cluster].append(ex)

    total = sum(counts.values())

    lines = []
    lines.append(f"Dataset: {dataset_path}")
    lines.append(f"Total examples: {total}")
    lines.append("")
    lines.append("Cluster counts:")

    for cluster, count in counts.most_common():
        percent = 100 * count / total if total else 0
        lines.append(f"{cluster}: {count} ({percent:.2f}%)")

    lines.append("")
    lines.append("Example rows:")

    for cluster, rows in examples.items():
        lines.append("")
        lines.append(f"{cluster}:")

        for ex in rows:
            lines.append(f"  natural: {ex.get('natural', '')}")
            lines.append(f"  formula: {ex.get('formula', '')}")

    output = "\n".join(lines)
    print(output)

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(output + "\n", encoding="utf-8")
        print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()