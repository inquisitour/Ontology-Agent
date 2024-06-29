from modules.ontology_matcher import OntologyMatcher

def main():
    matcher = OntologyMatcher()
    matcher.setup()
    results = matcher.match_ontologies("data/my_ontology.owl", "data/another_ontology.owl")
    print(f"Match Results: {results}")
    matcher.save_results(results, "data/match_results.txt")

if __name__ == "__main__":
    main()
