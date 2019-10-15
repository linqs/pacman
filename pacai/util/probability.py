"""
Various utilities for working with probabilities and distributions.
"""

import random

def normalize(vectorOrDict):
    """
    Normalize a vector or counter by dividing each value by the sum of all values.
    """

    if type(vectorOrDict) == dict:
        normalizedDict = {}
        dictContainer = vectorOrDict
        total = float(sum(dictContainer.values()))
        if total == 0:
            return dictContainer

        for key, value in dictContainer.items():
            normalizedDict[key] = value / total

        return normalizedDict
    else:
        vector = vectorOrDict
        s = float(sum(vector))
        if s == 0:
            return vector

        return [el / s for el in vector]

def nSample(distribution, values, n):
    if sum(distribution) != 1:
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
    if type(distribution) == dict:
        items = sorted(list(distribution.items()))
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]

    if sum(distribution) != 1:
        distribution = normalize(distribution)

    choice = random.random()
    i = 0
    total = distribution[0]

    while choice > total:
        i += 1
        total += distribution[i]

    return values[i]

def sampleFromDict(dict):
    items = sorted(list(dict.items()))
    return sample([v for k, v in items], [k for k, v in items])

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

def chooseFromDistribution(distribution):
    """
    Takes either a dict or a list of (prob, key) pairs and samples
    """

    if type(distribution) == dict:
        return sample(distribution)

    r = random.random()
    base = 0.0
    for prob, element in distribution:
        base += prob
        if r <= base:
            return element
