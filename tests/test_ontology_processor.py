import pytest
from modules.ontology_processor import OntologyProcessor
from owlready2 import get_ontology, Thing

@pytest.fixture
def sample_ontology(tmp_path):
    onto_path = tmp_path / "test_ontology.owl"
    onto = get_ontology("http://example.org/test_ontology.owl")
    
    with onto:
        class Person(Thing): pass
        class Student(Person): pass
        class hasParent(Person >> Person): pass
        class hasAge(Person >> int, FunctionalProperty): pass
        john = Person("John")
        john.hasAge = 30
    
    onto.save(file=str(onto_path), format="rdfxml")
    return str(onto_path)

def test_query_entities(sample_ontology):
    processor = OntologyProcessor(sample_ontology)
    classes, properties = processor.query_entities()
    
    assert len(classes) == 3  # Thing, Person, Student
    assert len(properties) == 2  # hasParent, hasAge

def test_perform_reasoning(sample_ontology):
    processor = OntologyProcessor(sample_ontology)
    inferred_subsumers = processor.perform_reasoning("Student")
    
    assert "Person" in [c.name for c in inferred_subsumers]
    assert "Thing" in [c.name for c in inferred_subsumers]

def test_query_subclasses(sample_ontology):
    processor = OntologyProcessor(sample_ontology)
    subclasses = processor.query_subclasses("Person")
    
    assert "Student" in [c.name for c in subclasses]

def test_query_individuals(sample_ontology):
    processor = OntologyProcessor(sample_ontology)
    individuals = processor.query_individuals("Person")
    
    assert "John" in [i.name for i in individuals]

# Add more tests as needed