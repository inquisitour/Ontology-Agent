from owlready2 import get_ontology, Thing, DataProperty, ObjectProperty, Individual

class OntologyCreator:
    def __init__(self, iri: str):
        self.ontology = get_ontology(iri)
    
    def create_classes(self):
        with self.ontology:
            class Person(Thing):
                pass
            class Organization(Thing):
                pass
    
    def create_properties(self):
        with self.ontology:
            class worksAt(ObjectProperty):
                domain = [Person]
                range = [Organization]
            
            class hasAge(DataProperty):
                domain = [Person]
                range = [int]
    
    def create_individuals(self):
        with self.ontology:
            alice = Person("Alice")
            acme_corp = Organization("ACME_Corp")
            alice.worksAt = [acme_corp]
            alice.hasAge = [30]
    
    def save_ontology(self, file_path: str):
        self.ontology.save(file_path)

