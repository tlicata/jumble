#!/usr/bin/python

import sys

# Script accepts one argument that is a string of letters. It will
# output a list of words that can be generated from those letters.
# The original input will not be included in the output, even the case
# that it is a valid word. Ispell word lists are used to test if a
# string is a word.

# The jumble I played in college required that all letters be used
# (e.g., dog => god). However, other rules allow for subsets of the
# letters to be used (e.g., dog => god, do, go). This flag allows for
# toggling of that behavior.
useAllLetters = False

# Grab the jumbled argument. Capping the length for performace reasons
# (recursive approach will eat all your resources.) You can up the
# limit by 1 if you want to wait, but I wouldn't up it by 2 without
# a more efficient algorithm.
if len(sys.argv) != 2:
    print "requires exactly one argument"
    sys.exit()
jumble = sys.argv[1].lower()
maxChars = 10 if useAllLetters else 8
if (len(jumble) > maxChars):
    print "argument should be " + str(maxChars) + " characters or less for performance reasons"
    sys.exit()

# Some pre-processing of the ispell dictionaries.
ispellFiles = [
    "altamer.0",
    "altamer.1",
    "altamer.2",
    "american.0",
    "american.1",
    "american.2",
    "british.0",
    "british.1",
    "british.2",
    "english.0",
    "english.1",
    "english.2",
    "english.3"
]
dictionary = {};
for wordlist in ispellFiles:
    for line in open("ispell/" + wordlist):
        dictionary[line.strip()] = True;
def inDictionary (word):
    return word in dictionary

# Functions for getting all the reorganizations of the jumbled word.
# The Memoize function is grabbed from StackOverflow.
def removeLetter (word, letter):
    arr = list(word)
    arr.remove(letter)
    return "".join(arr)
def permute (word):
    results = []
    letters = list(word)
    if (len(letters) == 1):
        results.append(word)
    else:
        for l in letters:
            currentResults = permute(removeLetter(word, l))
            if (not useAllLetters):
                results.extend(currentResults)
            results.extend(map(lambda x: "".join([l, x]), currentResults))
    return results
class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]
permute = Memoize(permute)
permutations = permute(jumble)

# For each possible permutation of the given letters, check if it's in
# the dictionary. Put the results into a set to remove any duplicates,
# then remove the argument from the list if it's present.
words = []
for perm in permutations:
    if inDictionary(perm):
        words.append(perm)
words = set(words)
if (jumble in words):
    words.remove(jumble)
if len(words) > 0:
    print ", ".join(words)
else:
    print "No words found"
