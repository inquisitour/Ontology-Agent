import argparse
import logging
from modules.config import load_config
from modules.ontology_matcher import OntologyMatcher

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Match two ontologies using LLMs4OM.")
    parser.add_argument("ontology1", help="Path to the first ontology file")
    parser.add_argument("ontology2", help="Path to the second ontology file")
    parser.add_argument("--output", default="match_results.txt", help="Path to save matching results")
    args = parser.parse_args()

    try:
        matcher = OntologyMatcher(args.ontology1, args.ontology2)
        results = matcher.match_ontologies()
        matcher.save_results(results, args.output)
        logger.info(f"Matching completed. Results saved to {args.output}")
    except Exception as e:
        logger.error(f"An error occurred while matching ontologies: {str(e)}")

if __name__ == "__main__":
    main()