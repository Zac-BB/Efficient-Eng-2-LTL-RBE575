import json
from pathlib import Path
from collections import Counter

INPUT = Path("datasets/drone-planning/syn-aug.train.jsonl")
OUTPUT = Path("datasets/drone-planning/syn-aug-clustered.train.jsonl")

def get_cluster(formula):
    f = formula.lower()

    if "until" in f:
        return "until_ordering"
    if "always" in f and "not" in f:
        return "safety_avoidance"
    if "always" in f:
        return "global_constraint"
    if "finally" in f and "and" in f:
        return "ordered_goal"
    if "or" in f:
        return "choice_goal"
    if "not" in f:
        return "negation"
    if "finally" in f:
        return "single_goal"
    return "other"

counts = Counter()

with INPUT.open("r", encoding="utf-8") as fin, OUTPUT.open("w", encoding="utf-8") as fout:
    for line in fin:
        ex = json.loads(line)
        cluster = get_cluster(ex["formula"])
        ex["semantic_cluster"] = cluster
        counts[cluster] += 1
        fout.write(json.dumps(ex) + "\n")

print(f"Wrote: {OUTPUT}")
print("Cluster counts:")
for cluster, count in counts.most_common():
    print(f"{cluster}: {count}")
