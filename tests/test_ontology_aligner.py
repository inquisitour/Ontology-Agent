import pytest
from modules.ontology_aligner import OntologyAligner
from owlready2 import get_ontology, Thing

@pytest.fixture
def sample_ontologies(tmp_path):
    onto1_path = tmp_path / "ontology1.owl"
    onto2_path = tmp_path / "ontology2.owl"
    
    onto1 = get_ontology("http://example.org/ontology1.owl")
    with onto1:
        class Person(Thing): pass
        class Student(Person): pass
    onto1.save(file=str(onto1_path), format="rdfxml")
    
    onto2 = get_ontology("http://example.org/ontology2.owl")
    with onto2:
        class Human(Thing): pass
        class Learner(Human): pass
    onto2.save(file=str(onto2_path), format="rdfxml")
    
    return str(onto1_path), str(onto2_path)

def test_align_ontologies(sample_ontologies, mocker):
    onto1_path, onto2_path = sample_ontologies
    
    # Mock the BERTMap align method to return a predefined alignment
    mock_align = mocker.patch('deeponto.align.BERTMap.align')
    mock_align.return_value = [
        ('Person', 'Human', 0.9),
        ('Student', 'Learner', 0.8)
    ]
    
    aligner = OntologyAligner(onto1_path, onto2_path)
    alignment = aligner.align_ontologies()
    
    assert len(alignment) == 2
    assert ('Person', 'Human', 0.9) in alignment
    assert ('Student', 'Learner', 0.8) in alignment

def test_save_alignment(sample_ontologies, tmp_path):
    onto1_path, onto2_path = sample_ontologies
    output_path = tmp_path / "alignment_results.txt"
    
    aligner = OntologyAligner(onto1_path, onto2_path)
    alignment = [('Person', 'Human', 0.9), ('Student', 'Learner', 0.8)]
    aligner.save_alignment(alignment, str(output_path))
    
    assert output_path.exists()
    with open(output_path, 'r') as f:
        content = f.read()
        assert "Person <-> Human: 0.9" in content
        assert "Student <-> Learner: 0.8" in content

# Add more tests as needed