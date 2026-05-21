# conti-org-analysis

Code and processed data for analyzing organizational dimensions: structure, specialization, and rules & norms; using the Conti ransomware group as a case study.

## Overview

This repository contains code, processed data, and analysis workflows supporting the study of organizational structure in cybercrime groups. The analyses are based on a leaked dataset from the Conti ransomware operation and are used to examine how organizational properties emerge from communication and internal documentation.

The repository focuses on three core organizational dimensions:

- **Structure**: Network-based analysis of communication patterns between members  
- **Specialization**: Semantic analysis of user roles and functional similarity  
- **Rules & Norms**: Institutional analysis of internal documentation using ABDICO-based coding  

These dimensions are part of a broader multilayer framework for modeling organizational resilience in cybercrime ecosystems.

## Associated paper

This repository accompanies the following paper:

> Manatova, Dalyapraz., McGrath, Cathleen., & Camp, L. Jean. (2026).  
> *The Organizational Anatomy of Cybercrime: A Multilayer Framework for Modeling Resilience.*  
> In press in *Journal of Cybersecurity* https://doi.org/10.1093/cybsec/tyag014.

## Data

The analysis is based on publicly leaked Conti data.

- Chat logs are preserved in their original language (Russian) for computational analysis.
- Translated documentation used for rules and norms analysis was generated using the DeepL API and manually reviewed and corrected by the author where necessary.
- Raw data may not be fully redistributed in this repository. Processed data and derived artifacts are provided where possible to support reproducibility. For example if you are looking for translated documents, the files appear in `analysis/rules_norms/Translated_Docs/docs`.  

## Repository structure

- `analysis/structure/`  
  Construction and analysis of the communication graph, including network measures and clustering.

- `analysis/specialization/`  
  Text embedding and clustering-based analysis of user specialization.

- `analysis/rules_norms/`  
  Sentence-level preprocessing and ABDICO-based extraction of institutional statements from internal documents.

## Reproducibility

The repository is structured to support transparency and reproducibility of the reported results:

- Notebooks are preserved with outputs and are not intended to be rerun without adapting local data paths.
- Key intermediate and final outputs (e.g., graphs, embeddings, cluster assignments) are saved where possible.
- Preprocessing and utility functions are provided in reusable Python modules.

## Notes

- This repository is intended for research and analytical purposes.
- Paths in notebooks may need to be adjusted depending on the local environment.

## Citation

If you use this repository, please cite the associated paper.
