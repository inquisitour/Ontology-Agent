from owlready2 import get_ontology, sync_reasoner
from deeponto.align import BERTMap

class OntologyAligner:
    def __init__(self, ontology_path1, ontology_path2):
        self.ontology1 = get_ontology(ontology_path1).load()
        self.ontology2 = get_ontology(ontology_path2).load()
        self.bertmap = BERTMap()

    def align_ontologies(self):
        alignment = self.bertmap.align(self.ontology1, self.ontology2)
        return alignment

    def save_alignment(self, alignment, file_path: str):
        with open(file_path, 'w') as f:
            for a in alignment:
                f.write(f"{a[0]} <-> {a[1]}: {a[2]}\n")
