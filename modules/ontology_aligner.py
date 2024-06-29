from deeponto.align import BERTMap

class OntologyAligner:
    def __init__(self):
        self.bertmap = BERTMap()
    
    def align_ontologies(self, file_path1: str, file_path2: str):
        alignment = self.bertmap.align(file_path1, file_path2)
        return alignment
