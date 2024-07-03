import pytest
import json
import os
from pathlib import Path
from datetime import date, time, datetime
from owlready2 import *
from modules.ontology_creator import OntologyCreator, create_ontology_from_config
from modules.config import load_config
from jsonschema.exceptions import ValidationError
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

    [Logging]
    level = INFO
    format = %%(asctime)s - %%(levelname)s - %%(message)s
    """
    config_file = tmp_path / "test_ontology_agent.ini"
    config_file.write_text(config_content)
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
    
    # Ensure the output directory exists in the project root
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    ontology_creator.create_ontology_from_config(config_file)
    
    output_file = output_dir / "my_dynamic_ontology.owl"
    print(f"Checking for existence of: {output_file}")
    
    assert output_file.exists(), f"Output file does not exist: {output_file}"

    # Use file:// URI for local files
    onto_uri = f"file://{output_file.resolve().as_posix()}"
    onto = get_ontology(onto_uri).load()
    
    # Convert classes, properties, and individuals to lists for easier assertion
    classes = list(onto.classes())
    class_names = [cls.name for cls in classes]
    object_properties = list(onto.object_properties())
    object_property_names = [prop.name for prop in object_properties]
    data_properties = list(onto.data_properties())
    data_property_names = [prop.name for prop in data_properties]
    individuals = list(onto.individuals())
    individual_names = [ind.name for ind in individuals]
    
    # Debug prints
    print("Loaded classes:", class_names)
    print("Loaded object properties:", object_property_names)
    print("Loaded data properties:", data_property_names)
    print("Loaded individuals:", individual_names)
    
    # Test classes
    assert "Person" in class_names
    assert "Student" in class_names
    assert "Course" in class_names
    assert onto.Student in list(onto.Person.subclasses())
    
    # Test object properties
    assert "hasParent" in object_property_names
    assert "enrolledIn" in object_property_names
    hasParent = onto.hasParent
    enrolledIn = onto.enrolledIn
    assert onto.Person in list(hasParent.domain)
    assert onto.Person in list(hasParent.range)
    assert TransitiveProperty in list(hasParent.is_a)
    assert FunctionalProperty in list(enrolledIn.is_a)
    
    # Test data properties
    assert "hasAge" in data_property_names
    assert "hasBirthDate" in data_property_names
    assert "hasStartTime" in data_property_names
    hasAge = onto.hasAge
    hasBirthDate = onto.hasBirthDate
    hasStartTime = onto.hasStartTime
    assert onto.Person in list(hasAge.domain)
    assert int in list(hasAge.range)
    assert FunctionalProperty in list(hasAge.is_a)
    assert date in list(hasBirthDate.range)
    assert datetime.time in list(hasStartTime.range)
    
    # Test individuals
    assert "John" in individual_names
    assert "Math101" in individual_names
    john = onto.John
    math101 = onto.Math101
    
    print(f"John's hasAge type: {type(john.hasAge)}, value: {john.hasAge}")
    print(f"John's hasBirthDate type: {type(john.hasBirthDate)}, value: {john.hasBirthDate}")
    print(f"Math101's hasStartTime type: {type(math101.hasStartTime)}, value: {math101.hasStartTime}")
    
    assert isinstance(john, onto.Student)
    
    # Check hasAge
    assert john.hasAge == 30 or john.hasAge == [30] or john.hasAge == ['30']
    
    # Check hasBirthDate
    expected_date = date(1993, 5, 15)
    assert (john.hasBirthDate == expected_date or 
            john.hasBirthDate == [expected_date] or 
            john.hasBirthDate == '1993-05-15' or 
            john.hasBirthDate == ['1993-05-15'])
    
    assert isinstance(math101, onto.Course)
    
    # Check hasStartTime
    expected_time = datetime.time(9, 0)
    assert (math101.hasStartTime == expected_time or 
            math101.hasStartTime == [expected_time] or 
            math101.hasStartTime == '09:00:00' or 
            math101.hasStartTime == ['09:00:00'])
    
    # Test disjoint classes
    disjoint_classes = [d for d in onto.disjoint_classes()]
    print(f"Disjoint classes: {disjoint_classes}")
    assert any(set(d.entities) == {onto.Student, onto.Course} for d in disjoint_classes)
    
    # Test equivalent classes
    assert onto.Human in list(onto.Person.equivalent_to)
    
    # Test annotations
    annotation_properties = list(onto.annotation_properties())
    annotation_property_names = [prop.name for prop in annotation_properties]
    print("Loaded annotation properties:", annotation_property_names)
    assert "hasDescription" in annotation_property_names

    # Debug: print all annotations for Person class
    print("Person annotations:")
    for prop in onto.annotation_properties():
        values = list(prop[onto.Person])
        print(f"  {prop.name}: {values}")

    # Check if hasDescription is in Person's __dict__
    print("Person __dict__:", onto.Person.__dict__)

    # Try to access hasDescription directly
    try:
        person_desc = onto.Person.hasDescription
        print("Person hasDescription:", person_desc)
    except Exception as e:
        print("Error accessing Person.hasDescription:", str(e))

    # Check annotations using IRIS
    print("Ontology triples:")
    world = onto.world
    for s, p, o in onto.get_triples():
        subject = world._entities.get(s)
        predicate = world._entities.get(p)
        object = world._entities.get(o) if isinstance(o, int) else o
        print(f"Subject: {subject}, Predicate: {predicate}, Object: {object}")
        if hasattr(predicate, 'name') and predicate.name == "hasDescription":
            print(f"Found annotation: subject={subject}, predicate={predicate.name}, object={object}")

    # Assert annotations
    assert any(p.name == "hasDescription" and "A human being" in list(p[onto.Person]) for p in onto.annotation_properties())
    assert any(p.name == "hasDescription" and "A person enrolled in an educational institution" in list(p[onto.Student]) for p in onto.annotation_properties())

    assert "Ontology created and saved successfully" in caplog.text

    # Clean up: remove the created ontology file after the test
    output_file.unlink()

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