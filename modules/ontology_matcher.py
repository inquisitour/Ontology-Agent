from LLMs4OM.ontomap.ontology import MouseHumanOMDataset
from LLMs4OM.ontomap.base import BaseConfig
from LLMs4OM.ontomap.evaluation.evaluator import evaluator
from LLMs4OM.ontomap.encoder import IRILabelInRAGEncoder
from LLMs4OM.ontomap.ontology_matchers import MistralLLMBertRAG
from LLMs4OM.ontomap.postprocess import process

class OntologyMatcher:
    def setup(self):
        self.config = BaseConfig(approach='rag').get_args(device='cuda', batch_size=16)
        self.config.root_dir = "datasets"

    def match_ontologies(self, source_ontology_path, target_ontology_path):
        ontology = MouseHumanOMDataset().collect(root_dir=self.config.root_dir)
        encoded_inputs = IRILabelInRAGEncoder()(ontology)
        model = MistralLLMBertRAG(self.config.MistralBertRAG)
        predicts = model.generate(input_data=encoded_inputs)
        predicts, _ = process.postprocess_hybrid(predicts=predicts, llm_confidence_th=0.7, ir_score_threshold=0.9)
        results = evaluator(track='anatomy', predicts=predicts, references=ontology["reference"])
        return results

    def save_results(self, results, file_path: str):
        with open(file_path, 'w') as f:
            for result in results:
                f.write(f"{result}\n")
