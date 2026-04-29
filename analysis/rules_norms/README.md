# Rules and Norms Analysis

This folder contains the materials used to analyze rules and norms in Conti internal documentation using sentence-level preprocessing and ABDICO-style institutional statement coding.

## Folder contents

- `Translated_Docs/`  
  Translated Conti documentation files. The documents were originally translated from Russian into English using the DeepL API and manually reviewed/corrected by the author where necessary.

- `ABDICO_CSVs/`  
  Sentence-level CSV files generated from the translated documents. These files are used as inputs for ABDICO coding.

- `Guidelines/`  
  Files related to the subset of documents categorized as guidelines. This folder includes sentence-level files and ABDICO-coded outputs for guideline documents.

- `ABDICO_eval/`  
  Evaluation files for ABDICO coding, including human-coded validation files, slot-level precision/recall/F1 results, and statement-type reliability summaries.

- `utils/`  
  Utility scripts for preprocessing. Currently includes `prepare_abdico_sentences.py`, which splits translated documents into sentence-level CSV files.

## Main files

- `Files Prep.ipynb`  
  Notebook for preparing translated documents for analysis by splitting them into sentence-level CSV files.

- `Conti_IG_analysis.ipynb`  
  Notebook for applying ABDICO-style institutional grammar coding and evaluating extracted rule/norm statements.

- `Analysis.ipynb`  
  Additional analysis notebook for reviewing and summarizing rules and norms outputs.

- `adic_human_validated.csv`  
  Human-validated ABDICO-coded statements reported in the paper.

- `adic_nonempty_rows.csv`  
  Filtered ABDICO output containing non-empty coded rows.

- `files_categories.numbers`  
  File categorization spreadsheet used to organize documents by analytical category.
