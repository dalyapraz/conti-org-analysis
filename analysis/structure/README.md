# Structure Analysis

This folder contains code and outputs for the organizational structure analysis of the Conti communication network. The analysis constructs a user-level social graph from chat logs and examines its topology and clustering structure.

## Overview

The pipeline processes raw message logs into one-to-one conversation histories, filters non-interactive or invalid exchanges, segments conversations into units, and constructs a weighted undirected graph where:

- nodes represent users  
- edges represent reciprocal interactions  
- edge weights correspond to the number of conversation units between users  

The resulting graph is analyzed using standard network measures and clustered to identify structural roles within the organization.

## Files

- `Prep Conversations for Analysis.ipynb`  
  Preprocesses chat logs into structured one-to-one conversations, applies filtering (single-speaker, glitch, encrypted messages), and segments conversations into units. Outputs the final graph-ready conversation dataset.

- `Conti_Graph_Analysis.ipynb`  
  Loads the processed graph, computes graph-level and node-level metrics, performs clustering (Gaussian Mixture Model), and generates figures and tables used in the paper.

- `functions.py`  
  Utility functions for loading logs, constructing conversation structures, filtering conversations, and segmentation.

- `graph_functions.py`  
  Functions for computing network measures, preparing feature matrices, and supporting clustering and graph analysis.

## Outputs

The analysis produces the following key artifacts (saved during notebook execution):

- `convo_graph.pkl`  
  Final conversation-unit graph.

- `conti_clusters.pkl`  
  Graph with cluster labels assigned to nodes.

- `graph_clusters.graphml`  
  Graph export for external visualization tools.


## Data dependencies

This analysis expects preprocessed log files located in the repository:

- `data/logs/chat_logs.json`
- `data/logs/jabber_logs.json`
- `data/logs/user match list.json`
- `data/user_lists/users.txt`

If raw logs are not provided, the saved graph and output files are sufficient to reproduce the reported results.

## Notes

- Notebooks are preserved with outputs for reproducibility and are not intended to be rerun without adjusting local paths.
- Exploratory or unused code (e.g., alternative segmentation methods or speaking-turn analysis) has been removed or archived.