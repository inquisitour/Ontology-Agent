import pytest
from modules.ontology_creator import create_ontology_from_config
from owlready2 import get_ontology
import json

@pytest.fixture
def sample_config():
    return {
        "ontology_iri": "http://example.org/test_ontology.owl",
        "classes": {
            "Person": "Thing",
            "Student": "Person"
        },
        "object_properties": {
            "hasParent": {
                "domain": ["Person"],
                "range": ["Person"]
            }
        },
        "data_properties": {
            "hasAge": {
                "domain": ["Person"],
                "range": ["int"]
            }
        },
        "individuals": [
            {
                "name": "John",
                "class": "Person",
                "attributes": {
                    "hasAge": [30]
                }
            }
        ]
    }

def test_create_ontology_from_config(sample_config, tmp_path):
    config_file = tmp_path / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(sample_config, f)
    
    output_file = tmp_path / "test_ontology.owl"
    create_ontology_from_config(str(config_file))
    
    assert output_file.exists()
    
    onto = get_ontology(output_file.as_uri()).load()
    assert "Person" in onto.classes()
    assert "Student" in onto.classes()
    assert "hasParent" in onto.object_properties()
    assert "hasAge" in onto.data_properties()
    assert "John" in onto.individuals()

# Add more tests as needed