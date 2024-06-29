from modules.ontology_matcher import OntologyMatcher

def main():
    matcher = OntologyMatcher()
    matcher.setup()
    matcher.match_ontologies("data/my_ontology.owl", "data/another_ontology.owl")

if __name__ == "__main__":
    main()
