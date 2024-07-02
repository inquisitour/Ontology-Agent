import pytest
import json
import os
from pathlib import Path
from datetime import date, time
from owlready2 import get_ontology, TransitiveProperty, FunctionalProperty
from modules.ontology_creator import OntologyCreator, create_ontology_from_config
from modules.config import load_config
from jsonschema.exceptions import ValidationError
import logging

@pytest.fixture
def test_config(tmp_path):
    config_content = f"""
    [General]
    root_dir = test_datasets
    output_dir = output

    [OntologyCreator]
    config_schema_path = {tmp_path}/ontology_config_schema.json

    [Logging]
    level = INFO
    format = %%(asctime)s - %%(levelname)s - %%(message)s
    """
    config_file = tmp_path / "test_ontology_agent.ini"
    config_file.write_text(config_content.format(tmp_path=tmp_path))
    return load_config(str(config_file))

@pytest.fixture
def sample_config():
    return {
        "ontology_iri": "http://example.org/test_ontology.owl",
        "classes": {
            "Person": "Thing",
            "Student": "Person",
            "Course": "Thing",
            "Human": "Thing"
        },
        "object_properties": {
            "hasParent": {
                "domain": ["Person"],
                "range": ["Person"],
                "property_type": ["TransitiveProperty"]
            },
            "enrolledIn": {
                "domain": ["Student"],
                "range": ["Course"],
                "property_type": ["FunctionalProperty"]
            }
        },
        "data_properties": {
            "hasAge": {
                "domain": ["Person"],
                "range": ["int"],
                "property_type": ["FunctionalProperty"]
            },
            "hasBirthDate": {
                "domain": ["Person"],
                "range": ["datetime.date"]
            },
            "hasStartTime": {
                "domain": ["Course"],
                "range": ["datetime.time"]
            }
        },
        "individuals": [
            {
                "name": "John",
                "class": "Student",
                "attributes": {
                    "hasAge": [30],
                    "hasBirthDate": ["1993-05-15"]
                }
            },
            {
                "name": "Math101",
                "class": "Course",
                "attributes": {
                    "hasStartTime": ["09:00:00"]
                }
            }
        ],
        "disjoint_classes": ["Student", "Course"],
        "equivalent_classes": [
            {"class": "Person", "equivalent_to": ["Human"]}
        ],
        "general_axioms": [
            {"axiom_type": "TransitiveProperty", "properties": ["hasParent"]}
        ],
        "annotations": {
            "hasDescription": {
                "Person": ["A human being"],
                "Student": ["A person enrolled in an educational institution"]
            }
        }
    }

@pytest.fixture
def config_file(tmp_path, sample_config):
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(sample_config, f)
    return str(config_file)

@pytest.fixture
def schema_file(tmp_path):
    schema = {
        "type": "object",
        "properties": {
            "ontology_iri": {"type": "string"},
            "classes": {"type": "object"},
            "object_properties": {"type": "object"},
            "data_properties": {"type": "object"},
            "individuals": {"type": "array"},
            "disjoint_classes": {"type": "array"},
            "equivalent_classes": {"type": "array"},
            "general_axioms": {"type": "array"},
            "annotations": {"type": "object"}
        },
        "required": ["ontology_iri", "classes"]
    }
    schema_file = tmp_path / "ontology_config_schema.json"
    with open(schema_file, "w") as f:
        json.dump(schema, f)
    return str(schema_file)

@pytest.fixture
def ontology_creator(schema_file):
    creator = OntologyCreator()
    creator.CONFIG_SCHEMA = json.load(open(schema_file))
    return creator

def test_create_ontology_from_config(ontology_creator, config_file, test_config, caplog):
    caplog.set_level(logging.INFO)
    ontology_creator.create_ontology_from_config(config_file)
    
    output_dir = test_config.get('General', 'output_dir')
    print(f"Expected output directory: {output_dir}")
    
    output_file = Path(output_dir) / "my_dynamic_ontology.owl"
    print(f"Checking for existence of: {output_file}")
    
    assert output_file.exists()

    onto = get_ontology(output_file.as_uri()).load()
    
    # Test classes
    assert "Person" in onto.classes()
    assert "Student" in onto.classes()
    assert "Course" in onto.classes()
    assert onto.Student.is_a == [onto.Person]
    
    # Test object properties
    assert "hasParent" in onto.object_properties()
    assert "enrolledIn" in onto.object_properties()
    assert onto.Person in onto.hasParent.domain
    assert onto.Person in onto.hasParent.range
    assert TransitiveProperty in onto.hasParent.is_a
    assert FunctionalProperty in onto.enrolledIn.is_a
    
    # Test data properties
    assert "hasAge" in onto.data_properties()
    assert "hasBirthDate" in onto.data_properties()
    assert "hasStartTime" in onto.data_properties()
    assert onto.Person in onto.hasAge.domain
    assert int in onto.hasAge.range
    assert FunctionalProperty in onto.hasAge.is_a
    assert date in onto.hasBirthDate.range
    assert time in onto.hasStartTime.range
    
    # Test individuals
    assert "John" in onto.individuals()
    john = onto.John
    assert isinstance(john, onto.Student)
    assert john.hasAge == [30]
    assert john.hasBirthDate == [date(1993, 5, 15)]
    
    assert "Math101" in onto.individuals()
    math101 = onto.Math101
    assert isinstance(math101, onto.Course)
    assert math101.hasStartTime == [time(9, 0)]
    
    # Test disjoint classes
    assert onto.Course in onto.Student.disjoint_with
    
    # Test equivalent classes
    assert onto.Human in onto.Person.equivalent_to
    
    # Test annotations
    assert "hasDescription" in onto.annotation_properties()
    person_desc = onto.Person.hasDescription
    assert "A human being" in person_desc
    student_desc = onto.Student.hasDescription
    assert "A person enrolled in an educational institution" in student_desc

    assert "Ontology created and saved successfully" in caplog.text

def test_create_ontology_invalid_config(ontology_creator, tmp_path):
    invalid_config = {
        "ontology_iri": "http://example.org/test_ontology.owl",
        "invalid_key": "This should not be here"
    }
    config_file = tmp_path / "invalid_config.json"
    with open(config_file, "w") as f:
        json.dump(invalid_config, f)
    
    with pytest.raises(ValidationError):
        ontology_creator.create_ontology_from_config(str(config_file))

def test_create_ontology_file_not_found(ontology_creator, tmp_path):
    with pytest.raises(FileNotFoundError):
        ontology_creator.create_ontology_from_config(str(tmp_path / "nonexistent_config.json"))

def test_create_ontology_invalid_json(ontology_creator, tmp_path):
    invalid_json_file = tmp_path / "invalid.json"
    invalid_json_file.write_text("{invalid json")
    with pytest.raises(json.JSONDecodeError):
        ontology_creator.create_ontology_from_config(str(invalid_json_file))

# Add more specific tests as needed
