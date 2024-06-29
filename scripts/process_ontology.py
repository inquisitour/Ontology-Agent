from modules.ontology_processor import OntologyProcessor

def main():
    processor = OntologyProcessor("my_dynamic_ontology.owl")
    classes, properties = processor.query_entities()
    print(f"Classes: {classes}\nProperties: {properties}")

    inferred_subsumers = processor.perform_reasoning("Person")
    print(f"Inferred Subsumers of Person: {inferred_subsumers}")

    subclasses = processor.query_subclasses("Person")
    print(f"Subclasses of Person: {subclasses}")

    individuals = processor.query_individuals("Person")
    print(f"Individuals of Person: {individuals}")

if __name__ == "__main__":
    main()
