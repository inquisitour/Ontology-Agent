from owlready2 import *

class OntologyProcessor:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

    def query_entities(self):
        classes = list(self.ontology.classes())
        properties = list(self.ontology.properties())
        return classes, properties

    def perform_reasoning(self, concept_name: str):
        reasoner = sync_reasoner()
        inferred_subsumers = reasoner.get_inferred_subsumers(concept_name)
        return inferred_subsumers

    def query_subclasses(self, class_name):
        cls = self.ontology[class_name]
        return list(cls.subclasses())

    def query_individuals(self, class_name):
        cls = self.ontology[class_name]
        return list(cls.instances())
