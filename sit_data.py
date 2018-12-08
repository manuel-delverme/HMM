import numpy as np
import pandas as pd

transitions = {}
sums_rows = {}

with open ("hmm_class/site_data.csv") as file:
    # for line in file:
    #     print(line)
    for line in file:
        start, end = line.rstrip().split(",")
        transitions[(start, end)] = transitions.get((start, end), 0) + 1
        sums_rows[start] =  sums_rows.get(start, 0) + 1

# normalize keys on transitions or normalize counts to make a distributions
for key, value in transitions.items():
    start, end = key
    transitions[key] = value / sums_rows[start]


# create initial state distributions

print(transitions)
print(sums_rows)

