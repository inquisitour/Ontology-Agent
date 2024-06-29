from modules.ontology_matcher import OntologyMatcher

def main():
    matcher = OntologyMatcher("my_dynamic_ontology.owl", "another_ontology.owl")
    results = matcher.match_ontologies()
    print(f"Match Results: {results}")
    matcher.save_results(results, "data/match_results.txt")

if __name__ == "__main__":
    main()
