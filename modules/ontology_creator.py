import json
import logging
import os
from typing import Dict, List, Union
from owlready2 import *
from jsonschema import validate
import jsonschema.exceptions
from modules.config import load_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

# Load the JSON schema from the path specified in the config
with open(config.get('OntologyCreator', 'config_schema_path')) as schema_file:
    CONFIG_SCHEMA = json.load(schema_file)

def create_ontology_from_config(config_path: str) -> None:
    """
    Create an ontology based on the configuration specified in a JSON file.

    Args:
        config_path (str): Path to the configuration JSON file.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If the configuration file is not valid JSON.
        jsonschema.exceptions.ValidationError: If the configuration does not match the schema.
    """
    try:
        with open(config_path, 'r') as file:
            ontology_config = json.load(file)
        
        # Validate configuration against schema
        validate(instance=ontology_config, schema=CONFIG_SCHEMA)
        
        ontology_iri = ontology_config["ontology_iri"]
        onto = get_ontology(ontology_iri)

        with onto:
            # Create classes
            classes = {cls: types.new_class(cls, (eval(parent),)) for cls, parent in ontology_config["classes"].items()}

            # Create object properties
            for prop, details in ontology_config.get("object_properties", {}).items():
                create_property(onto, prop, ObjectProperty, details)

            # Create data properties
            for prop, details in ontology_config.get("data_properties", {}).items():
                create_property(onto, prop, DataProperty, details)

            # Create individuals
            for individual in ontology_config["individuals"]:
                create_individual(onto, individual, classes)

            # Handle disjoint classes
            if "disjoint_classes" in ontology_config:
                AllDisjoint([classes[cls] for cls in ontology_config["disjoint_classes"]])

            # Handle equivalent classes
            for eq in ontology_config.get("equivalent_classes", []):
                cls = classes[eq["class"]]
                cls.equivalent_to.append(classes[eq["equivalent_to"][0]])

            # Handle general axioms
            for axiom in ontology_config.get("general_axioms", []):
                eval(axiom["axiom_type"])([getattr(onto, prop) for prop in axiom["properties"]])

        output_path = os.path.join(config.get('General', 'output_dir'), "my_dynamic_ontology.owl")
        onto.save(file=output_path, format="rdfxml")
        sync_reasoner()
        logger.info(f"Ontology created and saved successfully to {output_path}")
    
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file: {config_path}")
        raise
    except jsonschema.exceptions.ValidationError as ve:
        logger.error(f"Configuration validation error: {ve}")
        raise

def create_property(onto: Ontology, prop_name: str, prop_type: Union[ObjectProperty, DataProperty], details: Dict) -> None:
    """
    Create a property in the ontology.

    Args:
        onto (Ontology): The ontology to add the property to.
        prop_name (str): Name of the property.
        prop_type (Union[ObjectProperty, DataProperty]): Type of the property.
        details (Dict): Details of the property including domain, range, and extra types.
    """
    prop = types.new_class(prop_name, (prop_type,))
    for etype in details.get("property_type", []):
        prop.is_a.append(eval(etype))
    prop.domain = [getattr(onto, cls) for cls in details["domain"]]
    prop.range = [eval(r) if r in ["int", "float", "str", "bool"] else getattr(onto, r) for r in details["range"]]
    
    if "inverse_property" in details:
        inv_prop = types.new_class(details["inverse_property"], (ObjectProperty,))
        inv_prop.inverse_property = prop

def create_individual(onto: Ontology, individual: Dict, classes: Dict) -> None:
    """
    Create an individual in the ontology.

    Args:
        onto (Ontology): The ontology to add the individual to.
        individual (Dict): Details of the individual.
        classes (Dict): Dictionary of classes in the ontology.
    """
    ind = classes[individual["class"]](individual["name"])
    for attr, values in individual["attributes"].items():
        prop = getattr(onto, attr)
        for value in values:
            setattr(ind, prop.name, value)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create an ontology from a configuration file.")
    parser.add_argument("config", help="Path to the configuration JSON file")
    args = parser.parse_args()
    
    create_ontology_from_config(args.config)