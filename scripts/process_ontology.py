import argparse
import logging
from modules.config import load_config
from modules.ontology_processor import OntologyProcessor

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Process and query an ontology.")
    parser.add_argument("ontology", help="Path to the ontology file")
    parser.add_argument("--concept", help="Concept name for reasoning")
    parser.add_argument("--class", dest="class_name", help="Class name for subclass or individual queries")
    parser.add_argument("--query", choices=["subclasses", "individuals"], help="Type of query to perform")
    args = parser.parse_args()

    try:
        processor = OntologyProcessor(args.ontology)

        if args.concept:
            inferred_subsumers = processor.perform_reasoning(args.concept)
            print(f"Inferred subsumers of {args.concept}: {inferred_subsumers}")

        if args.class_name and args.query:
            if args.query == "subclasses":
                subclasses = processor.query_subclasses(args.class_name)
                print(f"Subclasses of {args.class_name}: {subclasses}")
            elif args.query == "individuals":
                individuals = processor.query_individuals(args.class_name)
                print(f"Individuals of {args.class_name}: {individuals}")

        if not (args.concept or (args.class_name and args.query)):
            classes, properties = processor.query_entities()
            print(f"Classes: {classes}")
            print(f"Properties: {properties}")

    except Exception as e:
        logger.error(f"An error occurred while processing the ontology: {str(e)}")

if __name__ == "__main__":
    main()