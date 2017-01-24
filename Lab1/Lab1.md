# Lab 1: Introduction to Map Reduce

## Introduction

This lab will introduce the map/reduce computing paradigm. In essence, map/reduce breaks tasks down into a map phase (where an algorithm is mapped onto data) and a reduce phase, where the outputs of the map phase are aggregated into a concise output. The map phase is designed to be parallel, so as to allow wide distribution of computation.

The map phase identifies keys and associates with them a value. The reduce phase collects keys and aggregates their values. The standard example used to demonstrate this programming approach is a word count problem, where words (or tokens) are the keys) and the number of occurrences of each word (or token) is the value.

As this technique was popularized by large web search companies like Google and Yahoo who were processing large quantities of unstructured text data, this approach quickly became popular for a wide range of problems. The standard MapReduce approach uses Hadoop, which was built using Java. However, to introduce you to this topic without adding the extra overhead of learning Hadoop's idiosyncrasies, we will be 'simulating' a map/reduce workload in pure Python.
