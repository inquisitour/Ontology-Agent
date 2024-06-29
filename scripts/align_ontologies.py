from modules.ontology_aligner import OntologyAligner

def main():
    aligner = OntologyAligner("my_dynamic_ontology.owl", "another_ontology.owl")
    alignment = aligner.align_ontologies()
    print(f"Alignment: {alignment}")
    aligner.save_alignment(alignment, "data/alignment_results.txt")

if __name__ == "__main__":
    main()
