import logging
from typing import Dict, Any
from owlready2 import get_ontology, sync_reasoner
from LLMs4OM.ontomap.ontology import MouseHumanOMDataset
from LLMs4OM.ontomap.base import BaseConfig
from LLMs4OM.ontomap.evaluation.evaluator import evaluator
from LLMs4OM.ontomap.encoder import IRILabelInRAGEncoder
from LLMs4OM.ontomap.ontology_matchers import MistralLLMBertRAG
from LLMs4OM.ontomap.postprocess import process
from modules.config import load_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

class OntologyMatcher:
    """
    A class for matching ontologies using LLMs4OM.
    """

    def __init__(self, ontology_path1: str, ontology_path2: str):
        """
        Initialize the OntologyMatcher with two ontologies and optional configuration.

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
            
            self.base_config = BaseConfig(approach='rag').get_args(device='cuda', batch_size=16)
            self.base_config.root_dir = config.get('General', 'root_dir')
            
            self.matcher_model = config.get('OntologyMatcher', 'matcher_model')
            self.llm_confidence_threshold = config.getfloat('OntologyMatcher', 'llm_confidence_threshold')
            self.ir_score_threshold = config.getfloat('OntologyMatcher', 'ir_score_threshold')
        except FileNotFoundError as e:
            logger.error(f"Ontology file not found: {e.filename}")
            raise

    def match_ontologies(self) -> Dict[str, Any]:
        """
        Match the two ontologies using LLMs4OM.

        Returns:
            Dict[str, Any]: A dictionary containing the matching results.

        Raises:
            Exception: If there's an error during the matching process.
        """
        try:
            ontology = MouseHumanOMDataset().collect(root_dir=self.base_config.root_dir)
            encoded_inputs = IRILabelInRAGEncoder()(ontology)
            model = globals()[self.matcher_model](self.base_config.MistralBertRAG)
            predicts = model.generate(input_data=encoded_inputs)
            predicts, _ = process.postprocess_hybrid(
                predicts=predicts, 
                llm_confidence_th=self.llm_confidence_threshold, 
                ir_score_threshold=self.ir_score_threshold
            )
            results = evaluator(track='anatomy', predicts=predicts, references=ontology["reference"])
            logger.info("Ontology matching completed successfully")
            return results
        except Exception as e:
            logger.error(f"Error during ontology matching: {str(e)}")
            raise

    def save_results(self, results: Dict[str, Any], file_path: str) -> None:
        """
        Save the matching results to a file.

        Args:
            results (Dict[str, Any]): The matching results.
            file_path (str): Path to save the matching results.

        Raises:
            IOError: If there's an error writing to the file.
        """
        try:
            with open(file_path, 'w') as f:
                for key, value in results.items():
                    f.write(f"{key}: {value}\n")
            logger.info(f"Saved matching results to {file_path}")
        except IOError as e:
            logger.error(f"Error saving matching results: {str(e)}")
            raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Match two ontologies using LLMs4OM.")
    parser.add_argument("ontology1", help="Path to the first ontology file")
    parser.add_argument("ontology2", help="Path to the second ontology file")
    parser.add_argument("--output", default="match_results.txt", help="Path to save matching results")
    args = parser.parse_args()

    matcher = OntologyMatcher(args.ontology1, args.ontology2)
    results = matcher.match_ontologies()
    matcher.save_results(results, args.output)
    print(f"Matching completed. Results saved to {args.output}")