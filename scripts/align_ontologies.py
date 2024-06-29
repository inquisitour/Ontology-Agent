from modules.ontology_aligner import OntologyAligner

def main():
    aligner = OntologyAligner()
    alignment = aligner.align_ontologies("data/my_ontology.owl", "data/another_ontology.owl")
    print(f"Alignment: {alignment}")
    aligner.save_alignment(alignment, "data/alignment_results.txt")

if __name__ == "__main__":
    main()
