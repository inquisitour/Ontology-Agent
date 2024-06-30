import argparse
import logging
from modules.config import load_config
from modules.ontology_aligner import OntologyAligner

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Align two ontologies using BERTMap.")
    parser.add_argument("ontology1", help="Path to the first ontology file")
    parser.add_argument("ontology2", help="Path to the second ontology file")
    parser.add_argument("--output", default="alignment_results.txt", help="Path to save alignment results")
    args = parser.parse_args()

    try:
        aligner = OntologyAligner(args.ontology1, args.ontology2)
        alignment = aligner.align_ontologies()
        aligner.save_alignment(alignment, args.output)
        logger.info(f"Alignment completed. Results saved to {args.output}")
    except Exception as e:
        logger.error(f"An error occurred while aligning ontologies: {str(e)}")

if __name__ == "__main__":
    main()