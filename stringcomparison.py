import Levenshtein

def relative_distance(lhs, rhs, distance = Levenshtein.distance):
    return float(distance(lhs, rhs)) / (len(lhs) + len(rhs))

def rate(needle, haystack, distance = relative_distance):
    result = [
        (element, distance(needle, element))
        for element in haystack
    ]
    result.sort(key=lambda x: x[1])
    return result
