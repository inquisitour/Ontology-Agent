import pytest
import json
import os
from pathlib import Path
from datetime import date, time, datetime
from owlready2 import *
from modules.ontology_processor import OntologyProcessor
from modules.ontology_creator import OntologyCreator
from modules.config import load_config
import logging

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

@pytest.fixture
def test_config(tmp_path):
    config_content = f"""
    [General]
    root_dir = test_datasets
    output_dir = output

    [OntologyCreator]
    config_schema_path = {tmp_path}/ontology_config_schema.json

    [OntologyProcessor]
    reasoning_enabled = true

    [Logging]
    level = INFO
    format = %%(asctime)s - %%(levelname)s - %%(message)s
    """
    config_file = tmp_path / "test_ontology_agent.ini"
    config_file.write_text(config_content)
    return load_config(str(config_file))

@pytest.fixture
def sample_ontology_config():
    return {
        "ontology_iri": "http://example.org/test_ontology.owl",
        "classes": {
            "Person": "Thing",
            "Student": "Person",
            "Professor": "Person",
            "Course": "Thing",
        },
        "object_properties": {
            "teaches": {
                "domain": ["Professor"],
                "range": ["Course"],
            },
            "attends": {
                "domain": ["Student"],
                "range": ["Course"],
            },
        },
        "data_properties": {
            "hasAge": {
                "domain": ["Person"],
                "range": ["int"],
                "property_type": ["FunctionalProperty"]
            },
            "hasName": {
                "domain": ["Person"],
                "range": ["str"],
                "property_type": ["FunctionalProperty"]
            },
        },
        "individuals": [
            {
                "name": "John",
                "class": "Student",
                "attributes": {
                    "hasAge": [20],
                    "hasName": ["John Doe"]
                }
            },
            {
                "name": "Math101",
                "class": "Course",
                "attributes": {}
            },
            {
                "name": "ProfSmith",
                "class": "Professor",
                "attributes": {
                    "hasAge": [45],
                    "hasName": ["Professor Smith"]
                }
            }
        ],
        "annotations": {
            "hasDescription": {
                "Person": ["A human being"],
                "Student": ["A person enrolled in an educational institution"],
                "Professor": ["A person who teaches courses"],
                "Course": ["An educational unit of instruction"]
            }
        }
    }

@pytest.fixture
def ontology_file(tmp_path, sample_ontology_config, test_config):
    config_file = tmp_path / "test_ontology_config.json"
    with open(config_file, "w") as f:
        json.dump(sample_ontology_config, f)

    creator = OntologyCreator()
    creator.create_ontology_from_config(str(config_file))

    output_file = Path(test_config.get('General', 'output_dir')) / "my_dynamic_ontology.owl"
    assert output_file.exists(), f"Output file does not exist: {output_file}"
    
    return str(output_file)

@pytest.fixture
def ontology_processor(ontology_file):
    return OntologyProcessor(ontology_file)

def test_query_entities(ontology_processor):
    classes, properties = ontology_processor.query_entities()
    
    class_names = [cls.name for cls in classes]
    property_names = [prop.name for prop in properties]
    
    print("Classes:", class_names)
    print("Properties:", property_names)
    
    assert "Person" in class_names
    assert "Student" in class_names
    assert "Professor" in class_names
    assert "Course" in class_names
    
    assert "teaches" in property_names
    assert "attends" in property_names
    assert "hasAge" in property_names
    assert "hasName" in property_names

def test_perform_reasoning(ontology_processor):
    inferred_subsumers = ontology_processor.perform_reasoning("Student")
    
    subsumer_names = [cls.name for cls in inferred_subsumers]
    print("Inferred subsumers of Student:", subsumer_names)
    
    assert "Person" in subsumer_names
    assert "Thing" in subsumer_names

def test_query_subclasses(ontology_processor):
    subclasses = ontology_processor.query_subclasses("Person")
    
    subclass_names = [cls.name for cls in subclasses]
    print("Subclasses of Person:", subclass_names)
    
    assert "Student" in subclass_names
    assert "Professor" in subclass_names

def test_query_individuals(ontology_processor):
    individuals = ontology_processor.query_individuals("Person")
    
    individual_names = [ind.name for ind in individuals]
    print("Individuals of Person:", individual_names)
    
    assert "John" in individual_names
    assert "ProfSmith" in individual_names

def test_query_object_properties(ontology_processor):
    object_properties = ontology_processor.query_object_properties()
    
    property_names = [prop.name for prop in object_properties]
    print("Object properties:", property_names)
    
    assert "teaches" in property_names
    assert "attends" in property_names

def test_query_data_properties(ontology_processor):
    data_properties = ontology_processor.query_data_properties()
    
    property_names = [prop.name for prop in data_properties]
    print("Data properties:", property_names)
    
    assert "hasAge" in property_names
    assert "hasName" in property_names

def test_query_annotations(ontology_processor):
    annotations = ontology_processor.query_annotations()
    
    print("Annotations:")
    for entity, ann_dict in annotations.items():
        print(f"  {entity}:")
        for prop, values in ann_dict.items():
            print(f"    {prop}: {values}")
    
    assert "hasDescription" in annotations["Person"]
    assert "A human being" in annotations["Person"]["hasDescription"]
    assert "A person enrolled in an educational institution" in annotations["Student"]["hasDescription"]

def test_query_property_characteristics(ontology_processor):
    characteristics = ontology_processor.query_property_characteristics("hasAge")
    
    print("Characteristics of hasAge:", characteristics)
    
    assert "FunctionalProperty" in characteristics

def test_query_class_hierarchy(ontology_processor):
    hierarchy = ontology_processor.query_class_hierarchy()
    
    print("Class hierarchy:")
    for parent, children in hierarchy.items():
        print(f"  {parent}: {children}")
    
    assert "Person" in hierarchy["Thing"]
    assert "Student" in hierarchy["Person"]
    assert "Professor" in hierarchy["Person"]

def test_query_property_domains_and_ranges(ontology_processor):
    domains, ranges = ontology_processor.query_property_domains_and_ranges("teaches")
    
    print("Domains of teaches:", [cls.name for cls in domains])
    print("Ranges of teaches:", [cls.name for cls in ranges])
    
    assert any(cls.name == "Professor" for cls in domains)
    assert any(cls.name == "Course" for cls in ranges)

def test_ontology_consistency(ontology_processor):
    is_consistent = ontology_processor.check_ontology_consistency()
    
    print("Ontology consistency:", is_consistent)
    
    assert is_consistent

def test_ontology_metrics(ontology_processor):
    metrics = ontology_processor.get_ontology_metrics()
    
    print("Ontology metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
    
    assert metrics["num_classes"] == 4
    assert metrics["num_object_properties"] == 2
    assert metrics["num_data_properties"] == 2
    assert metrics["num_individuals"] == 3

def test_query_non_existent_class(ontology_processor):
    with pytest.raises(AttributeError):
        ontology_processor.query_subclasses("NonExistentClass")
    print("Successfully raised AttributeError for non-existent class")

def test_query_non_existent_individual(ontology_processor):
    individuals = ontology_processor.query_individuals("Person")
    assert "NonExistentIndividual" not in [ind.name for ind in individuals]
    print("Successfully verified non-existent individual is not in results")

def test_query_non_existent_property(ontology_processor):
    with pytest.raises(AttributeError):
        ontology_processor.query_property_characteristics("nonExistentProperty")
    print("Successfully raised AttributeError for non-existent property")

def test_perform_reasoning_on_non_existent_concept(ontology_processor):
    with pytest.raises(AttributeError):
        ontology_processor.perform_reasoning("NonExistentConcept")
    print("Successfully raised AttributeError for non-existent concept in reasoning")

def test_query_empty_class(ontology_processor, ontology_file):
    # First, let's add an empty class to our ontology
    with ontology_processor.ontology:
        types.new_class("EmptyClass", (Thing,))
    
    empty_class_individuals = ontology_processor.query_individuals("EmptyClass")
    assert len(empty_class_individuals) == 0
    print("Successfully verified empty class has no individuals")

def test_query_property_with_no_domain_or_range(ontology_processor, ontology_file):
    # Add a property with no domain or range
    with ontology_processor.ontology:
        types.new_class("PropertyWithNoDomainOrRange", (ObjectProperty,))
    
    domains, ranges = ontology_processor.query_property_domains_and_ranges("PropertyWithNoDomainOrRange")
    assert len(domains) == 0 and len(ranges) == 0
    print("Successfully verified property with no domain or range")

def test_ontology_with_inconsistency(ontology_processor, ontology_file):
    # Create an inconsistency in the ontology
    with ontology_processor.ontology:
        inconsistent_class = types.new_class("InconsistentClass", (Thing,))
        inconsistent_class.equivalent_to.append(Not(inconsistent_class))
    
    is_consistent = ontology_processor.check_ontology_consistency()
    assert not is_consistent
    print("Successfully detected ontology inconsistency")

def test_ontology_with_inconsistency(ontology_processor, ontology_file):
    # Create an inconsistency in the ontology
    with ontology_processor.ontology:
        inconsistent_class = types.new_class("InconsistentClass", (Thing,))
        inconsistent_class.equivalent_to.append(Not(inconsistent_class))
    
    is_consistent = ontology_processor.check_ontology_consistency()
    assert not is_consistent
    print("Successfully detected ontology inconsistency")

