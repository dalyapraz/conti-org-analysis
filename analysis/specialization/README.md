# Specialization Analysis

This folder contains the notebook and supporting files for analyzing user specialization in the Conti chat network through text embeddings and thematic clustering.

## Files

### `Specialization_similarity.ipynb`

Main analysis notebook for the specialization analysis.

The notebook performs the following steps:

1. Loads the preprocessed Conti conversation graph.
2. Extracts user-authored text from conversation units.
3. Generates text embeddings using `ai-forever/ru-en-RoSBERTa`.
4. Clusters each user's embeddings to identify within-user topical groupings.
5. Represents each within-user cluster with a centroid embedding.
6. Clusters these representative embeddings across users into higher-level thematic clusters.
7. Computes user similarity based on shared thematic cluster membership using cosine similarity and Jaccard similarity.

### `graph_functions.py`

Helper functions for loading and working with the graph object used in the analysis.

The notebook relies on this file to load the preprocessed conversation graph.

### `conti_clusters.pkl`

Serialized graph object used as the input to the specialization analysis.

This graph was produced in the earlier structure-processing stage of the project. It contains the Conti textual conversation network, with conversations already split into conversation units and turns. Each edge stores conversation turn units between users, and the specialization notebook extracts user-authored texts from these units for embedding and clustering.

