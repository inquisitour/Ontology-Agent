import argparse
import logging
from modules.config import load_config
from modules.ontology_creator import create_ontology_from_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Create an ontology from a configuration file.")
    parser.add_argument("config", help="Path to the ontology configuration JSON file")
    parser.add_argument("--output", help="Path to save the created ontology", 
                        default=config.get('General', 'output_dir'))
    args = parser.parse_args()

    try:
        create_ontology_from_config(args.config)
        logger.info(f"Ontology created and saved to {args.output}")
    except Exception as e:
        logger.error(f"An error occurred while creating the ontology: {str(e)}")

if __name__ == "__main__":
    main()