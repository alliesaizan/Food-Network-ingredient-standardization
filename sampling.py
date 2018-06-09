#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 16:00:43 2018

@author: alliesaizan
"""

# Overview: the purpose of this file is to create a validation sample for
    # comparing the effectiveness of different standardization methodologies.
    # I use the propotional allocation stratified random sampling method.

# This work took me: 3 hours


import os
import pandas as pd
from itertools import chain
import operator
import matplotlib.pyplot as plt
import pickle

# Fix the working directory
os.getcwd()
os.chdir("Documents/Food-Network-master")
path = os.getcwd()

# Load JSON data
recipes = pd.read_json("recipes.json")

# Pull ingredients into a list and remove special characters
ingredients = list(chain.from_iterable(recipes.ingredients.tolist()))

ingredientsNew = []

for i in ingredients:
    ingredientsNew.append("".join(x for x in i if ord(x) < 126))

del i
    
ingredientsLower = set([i.lower() for i in ingredientsNew])

###################
# Step 1: Obtain counts of words in an ingredient into a dictionary-style format
ingredDict = {k:len(k.split()) for k in ingredientsLower}


###################
# Step 2: Determine the largest 
print(sorted(ingredDict.items(), key = operator.itemgetter(1), reverse=True))
    # The largest string has 11 elements. Ugh.
  
###################
# Step 3: Sample a set amount from each ingredient length type.

plt.hist(list(ingredDict.values()), bins = 11, facecolor="blue", alpha = 0.5)
    # Most ingredients have 2-4 words in them

# Method will be to sample with groups proportional to their original proportions and be small enough for me to hand-check, so
    # I'll take 2.5% of the total data

temp = pd.DataFrame(list(ingredDict.items()), columns = ["ingredients", "counts"])

# How many ingredients are in each strata?
temp["counts"].value_counts()

# What would 2.5% of the data look like for each strata?
temp["counts"].value_counts() * 0.025

# Pull a list of ingredient word length for use as the sample strata
frequencies = list(set(ingredDict.values()))

# Use the pandas sample methodology to sample 2.5% of each strata, and preserve
    # the result using "random sample" for replicability
    
samples = []

for value in frequencies:
    subset = temp[temp.counts == value]
    samples.append(subset.sample(frac = 0.025, random_state=1)["ingredients"].tolist())

validationList = list(chain.from_iterable(samples))

del value, temp, samples, frequencies, subset

# Save the list as a Python serialized object
pickle.dump(validationList, open(path + "/validationSet.py", "wb"))


