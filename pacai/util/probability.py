"""
Various utilities for working with probabilities and distributions.
"""

import math
import random

def normalize(listOrDict):
    """
    Normalize a list or dictionary by dividing each value by the
    sum of all values, resulting in values to be in range [0, 1].
    Requirements for listOrDict argument:
    1. Must be non-empty.
    2. For a dict, each value must be >= 0 and the sum must be > 0.
    """

    if isinstance(listOrDict, dict):
        total = float(sum(listOrDict.values()))
        if math.isclose(total, 0):
            return listOrDict

        normalizedDict = {}
        for key, value in listOrDict.items():
            normalizedDict[key] = value / total

        return normalizedDict
    else:
        total = float(sum(listOrDict))
        if math.isclose(total, 0):
            return listOrDict

        return [val / total for val in listOrDict]

def nSample(distribution, values, n):
    if not math.isclose(sum(distribution), 1):
        distribution = normalize(distribution)

    rand = [random.random() for i in range(n)]
    rand.sort()
    samples = []
    samplePos, distPos, cdf = 0, 0, distribution[0]
    while samplePos < n:
        if rand[samplePos] < cdf:
            samplePos += 1
            samples.append(values[distPos])
        else:
            distPos += 1
            cdf += distribution[distPos]

    return samples

def sample(distribution, values = None):
    if isinstance(distribution, dict):
        items = sorted(distribution.items())
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]

    if len(distribution) == 0:
        raise ValueError("Distribution to sample must be non-empty.")

    if math.isclose(sum(distribution), 1):
        distribution = normalize(distribution)

    if values is None:
        raise ValueError("When sampling list, both distribution and values must be initialized.")

    if len(distribution) != len(values):
        raise ValueError("When sampling list, distribution and values must be the same size.")

    choice = random.random()
    i = 0
    total = distribution[0]

    while choice >= total:
        i += 1
        total += distribution[i]

    return values[i]

def getProbability(value, distribution, values):
    """
    Gives the probability of a value under a discrete distribution
    defined by (distributions, values).
    """

    total = 0.0
    for prob, val in zip(distribution, values):
        if val == value:
            total += prob

    return total

def flipCoin(p):
    r = random.random()
    return r < p
