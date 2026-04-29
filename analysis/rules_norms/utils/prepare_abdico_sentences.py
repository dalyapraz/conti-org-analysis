import os
import csv
import argparse
from pathlib import Path
import spacy
from spacy.language import Language


@Language.component("no_abbrev_breaks")
def no_abbrev_breaks(doc):
    stop = {"e.g.", "i.e.", "etc."}
    for i, t in enumerate(doc[:-1]):
        if t.text in stop:
            doc[i + 1].is_sent_start = False
    return doc


def build_nlp():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("no_abbrev_breaks", first=True)
    return nlp


def file_to_sentence_csv_spacy(input_file, output_csv, nlp):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Sentence"])
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            doc = nlp(line)
            for sent in doc.sents:
                clean_sentence = sent.text.strip()
                if clean_sentence:
                    writer.writerow([clean_sentence])
    print(f"Created: {output_csv}")


def process_directory(input_dir, output_base_dir):
    nlp = build_nlp()
    for root, _, files in os.walk(input_dir):
        rel_path = os.path.relpath(root, input_dir)
        for file in files:
            if file.startswith("."):
                continue
            input_path = os.path.join(root, file)
            name, _ = os.path.splitext(file)
            output_dir = os.path.join(output_base_dir, rel_path)
            output_csv = os.path.join(output_dir, f"{name}_sentences.csv")
            if os.path.exists(output_csv):
                print(f"Skipping existing: {output_csv}")
                continue
            file_to_sentence_csv_spacy(input_path, output_csv, nlp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert text files to sentence-level CSVs.")
    parser.add_argument("--input_dir", required=True, help="Directory with input text files")
    parser.add_argument("--output_dir", required=True, help="Directory to store CSV outputs")

    args = parser.parse_args()

    process_directory(args.input_dir, args.output_dir)