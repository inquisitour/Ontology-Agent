import logging
from typing import List, Tuple
from owlready2 import get_ontology, sync_reasoner
from deeponto.align import BERTMap
from modules.config import load_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

class OntologyAligner:
    """
    A class for aligning two ontologies using BERTMap.
    """

    def __init__(self, ontology_path1: str, ontology_path2: str):
        """
        Initialize the OntologyAligner with two ontologies.

        Args:
            ontology_path1 (str): Path to the first ontology file.
            ontology_path2 (str): Path to the second ontology file.

        Raises:
            FileNotFoundError: If either ontology file is not found.
        """
        try:
            self.ontology1 = get_ontology(ontology_path1).load()
            self.ontology2 = get_ontology(ontology_path2).load()
            logger.info(f"Loaded ontologies from {ontology_path1} and {ontology_path2}")
            self.bertmap = BERTMap()
            self.confidence_threshold = config.getfloat('OntologyAligner', 'confidence_threshold')
        except FileNotFoundError as e:
            logger.error(f"Ontology file not found: {e.filename}")
            raise

    def align_ontologies(self) -> List[Tuple[str, str, float]]:
        """
        Align the two ontologies using BERTMap.

        Returns:
            List[Tuple[str, str, float]]: A list of alignment tuples (entity1, entity2, confidence).
        """
        try:
            alignment = self.bertmap.align(self.ontology1, self.ontology2)
            filtered_alignment = [a for a in alignment if a[2] >= self.confidence_threshold]
            logger.info(f"Aligned ontologies, found {len(filtered_alignment)} alignments above threshold")
            return filtered_alignment
        except Exception as e:
            logger.error(f"Error during ontology alignment: {str(e)}")
            raise

    def save_alignment(self, alignment: List[Tuple[str, str, float]], file_path: str) -> None:
        """
        Save the alignment results to a file.

        Args:
            alignment (List[Tuple[str, str, float]]): The alignment results.
            file_path (str): Path to save the alignment results.

        Raises:
            IOError: If there's an error writing to the file.
        """
        try:
            with open(file_path, 'w') as f:
                for a in alignment:
                    f.write(f"{a[0]} <-> {a[1]}: {a[2]}\n")
            logger.info(f"Saved alignment results to {file_path}")
        except IOError as e:
            logger.error(f"Error saving alignment results: {str(e)}")
            raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Align two ontologies using BERTMap.")
    parser.add_argument("ontology1", help="Path to the first ontology file")
    parser.add_argument("ontology2", help="Path to the second ontology file")
    parser.add_argument("--output", default="alignment_results.txt", help="Path to save alignment results")
    args = parser.parse_args()

    aligner = OntologyAligner(args.ontology1, args.ontology2)
    alignment = aligner.align_ontologies()
    aligner.save_alignment(alignment, args.output)
    print(f"Alignment completed. Results saved to {args.output}")