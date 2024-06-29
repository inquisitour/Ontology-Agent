from modules.ontology_creator import OntologyCreator

def main():
    creator = OntologyCreator("http://example.org/my_ontology.owl")
    creator.create_classes()
    creator.create_properties()
    creator.create_individuals()
    creator.save_ontology("data/my_ontology.owl")

if __name__ == "__main__":
    main()
