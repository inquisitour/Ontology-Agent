from deeponto import Ontology, OntologyReasoner

class OntologyProcessor:
    def __init__(self, file_path: str):
        self.ontology = Ontology(file_path)
    
    def query_entities(self):
        classes = self.ontology.get_classes()
        properties = self.ontology.get_properties()
        return classes, properties
    
    def perform_reasoning(self, concept_name: str):
        reasoner = OntologyReasoner(self.ontology)
        inferred_subsumers = reasoner.get_inferred_subsumers(concept_name)
        return inferred_subsumers
