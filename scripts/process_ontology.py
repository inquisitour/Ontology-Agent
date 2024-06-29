from modules.ontology_processor import OntologyProcessor

def main():
    processor = OntologyProcessor("data/my_ontology.owl")
    classes, properties = processor.query_entities()
    print(f"Classes: {classes}\nProperties: {properties}")
    
    inferred_subsumers = processor.perform_reasoning("Person")
    print(f"Inferred Subsumers of Person: {inferred_subsumers}")

if __name__ == "__main__":
    main()
