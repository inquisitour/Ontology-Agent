import pytest
from modules.ontology_matcher import OntologyMatcher
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

def test_match_ontologies(sample_ontologies, mocker):
    onto1_path, onto2_path = sample_ontologies
    
    # Mock the necessary components of LLMs4OM
    mocker.patch('LLMs4OM.ontomap.ontology.MouseHumanOMDataset.collect')
    mocker.patch('LLMs4OM.ontomap.encoder.IRILabelInRAGEncoder.__call__')
    mocker.patch('LLMs4OM.ontomap.ontology_matchers.MistralLLMBertRAG.generate')
    mock_postprocess = mocker.patch('LLMs4OM.ontomap.postprocess.process.postprocess_hybrid')
    mock_postprocess.return_value = ({"Person": "Human", "Student": "Learner"}, None)
    mock_evaluator = mocker.patch('LLMs4OM.ontomap.evaluation.evaluator.evaluator')
    mock_evaluator.return_value = {"precision": 0.9, "recall": 0.8, "f1": 0.85}
    
    matcher = OntologyMatcher(onto1_path, onto2_path)
    results = matcher.match_ontologies()
    
    assert "precision" in results
    assert "recall" in results
    assert "f1" in results
    assert results["precision"] == 0.9
    assert results["recall"] == 0.8
    assert results["f1"] == 0.85

def test_save_results(sample_ontologies, tmp_path):
    onto1_path, onto2_path = sample_ontologies
    output_path = tmp_path / "match_results.txt"
    
    matcher = OntologyMatcher(onto1_path, onto2_path)
    results = {"precision": 0.9, "recall": 0.8, "f1": 0.85}
    matcher.save_results(results, str(output_path))
    
    assert output_path.exists()
    with open(output_path, 'r') as f:
        content = f.read()
        assert "precision: 0.9" in content
        assert "recall: 0.8" in content
        assert "f1: 0.85" in content

# Add more tests as needed