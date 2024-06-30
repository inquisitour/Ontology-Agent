import logging
from typing import List, Tuple
from owlready2 import *
from modules.config import load_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

class OntologyProcessor:
    """
    A class for processing and querying ontologies.
    """

    def __init__(self, ontology_path: str):
        """
        Initialize the OntologyProcessor with an ontology.

        Args:
            ontology_path (str): Path to the ontology file.

        Raises:
            FileNotFoundError: If the ontology file is not found.
        """
        try:
            self.ontology = get_ontology(ontology_path).load()
            logger.info(f"Loaded ontology from {ontology_path}")
        except FileNotFoundError:
            logger.error(f"Ontology file not found: {ontology_path}")
            raise

    def query_entities(self) -> Tuple[List[Thing], List[Property]]:
        """
        Query all classes and properties in the ontology.

        Returns:
            Tuple[List[Thing], List[Property]]: A tuple containing lists of classes and properties.
        """
        classes = list(self.ontology.classes())
        properties = list(self.ontology.properties())
        logger.info(f"Queried {len(classes)} classes and {len(properties)} properties")
        return classes, properties

    def perform_reasoning(self, concept_name: str) -> List[Thing]:
        """
        Perform reasoning on a given concept and return inferred subsumers.

        Args:
            concept_name (str): Name of the concept to reason about.

        Returns:
            List[Thing]: List of inferred subsumers.

        Raises:
            AttributeError: If the concept is not found in the ontology.
        """
        try:
            with self.ontology:
                sync_reasoner()
            concept = getattr(self.ontology, concept_name)
            inferred_subsumers = list(concept.ancestors())
            logger.info(f"Performed reasoning on {concept_name}, found {len(inferred_subsumers)} inferred subsumers")
            return inferred_subsumers
        except AttributeError:
            logger.error(f"Concept not found in ontology: {concept_name}")
            raise

    def query_subclasses(self, class_name: str) -> List[Thing]:
        """
        Query subclasses of a given class.

        Args:
            class_name (str): Name of the class to query subclasses for.

        Returns:
            List[Thing]: List of subclasses.

        Raises:
            AttributeError: If the class is not found in the ontology.
        """
        try:
            cls = getattr(self.ontology, class_name)
            subclasses = list(cls.subclasses())
            logger.info(f"Queried subclasses of {class_name}, found {len(subclasses)} subclasses")
            return subclasses
        except AttributeError:
            logger.error(f"Class not found in ontology: {class_name}")
            raise

    def query_individuals(self, class_name: str) -> List[Thing]:
        """
        Query individuals of a given class.

        Args:
            class_name (str): Name of the class to query individuals for.

        Returns:
            List[Thing]: List of individuals.

        Raises:
            AttributeError: If the class is not found in the ontology.
        """
        try:
            cls = getattr(self.ontology, class_name)
            individuals = list(cls.instances())
            logger.info(f"Queried individuals of {class_name}, found {len(individuals)} individuals")
            return individuals
        except AttributeError:
            logger.error(f"Class not found in ontology: {class_name}")
            raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process and query an ontology.")
    parser.add_argument("ontology", help="Path to the ontology file")
    parser.add_argument("--concept", help="Concept name for reasoning")
    parser.add_argument("--class", dest="class_name", help="Class name for subclass or individual queries")
    parser.add_argument("--query", choices=["subclasses", "individuals"], help="Type of query to perform")
    args = parser.parse_args()

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