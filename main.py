import sys
import logging
import argparse
from modules.config import load_config
from modules.ontology_creator import create_ontology_from_config
from modules.ontology_processor import OntologyProcessor
from modules.ontology_aligner import OntologyAligner
from modules.ontology_matcher import OntologyMatcher

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="OntologyAgent: Create, process, align, and match ontologies.")
    parser.add_argument("action", choices=["create", "process", "align", "match"], help="Action to perform")
    parser.add_argument("--config", help="Path to the configuration file (for create action)")
    parser.add_argument("--ontology", help="Path to the ontology file (for process action)")
    parser.add_argument("--ontology1", help="Path to the first ontology file (for align and match actions)")
    parser.add_argument("--ontology2", help="Path to the second ontology file (for align and match actions)")
    parser.add_argument("--output", help="Path to save the output")
    parser.add_argument("--concept", help="Concept name for reasoning (for process action)")
    parser.add_argument("--class", dest="class_name", help="Class name for subclass or individual queries (for process action)")
    parser.add_argument("--query", choices=["subclasses", "individuals"], help="Type of query to perform (for process action)")
    args = parser.parse_args()

    try:
        if args.action == "create":
            if not args.config:
                raise ValueError("Config file path is required for create action")
            create_ontology_from_config(args.config)
        
        elif args.action == "process":
            if not args.ontology:
                raise ValueError("Ontology file path is required for process action")
            processor = OntologyProcessor(args.ontology)
            
            if args.concept:
                inferred_subsumers = processor.perform_reasoning(args.concept)
                print(f"Inferred subsumers of {args.concept}: {inferred_subsumers}")
            elif args.class_name and args.query:
                if args.query == "subclasses":
                    subclasses = processor.query_subclasses(args.class_name)
                    print(f"Subclasses of {args.class_name}: {subclasses}")
                elif args.query == "individuals":
                    individuals = processor.query_individuals(args.class_name)
                    print(f"Individuals of {args.class_name}: {individuals}")
            else:
                classes, properties = processor.query_entities()
                print(f"Classes: {classes}")
                print(f"Properties: {properties}")
        
        elif args.action == "align":
            if not (args.ontology1 and args.ontology2):
                raise ValueError("Two ontology file paths are required for align action")
            aligner = OntologyAligner(args.ontology1, args.ontology2)
            alignment = aligner.align_ontologies()
            output_path = args.output or "alignment_results.txt"
            aligner.save_alignment(alignment, output_path)
            print(f"Alignment completed. Results saved to {output_path}")
        
        elif args.action == "match":
            if not (args.ontology1 and args.ontology2):
                raise ValueError("Two ontology file paths are required for match action")
            matcher = OntologyMatcher(args.ontology1, args.ontology2)
            results = matcher.match_ontologies()
            output_path = args.output or "match_results.txt"
            matcher.save_results(results, output_path)
            print(f"Matching completed. Results saved to {output_path}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()