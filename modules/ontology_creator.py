import json
import logging
import os
from typing import Dict, List, Union, Type
from owlready2 import *
from jsonschema import validate
import jsonschema.exceptions
from modules.config import load_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

class OntologyCreator:
    def __init__(self):
        with open(config.get('OntologyCreator', 'config_schema_path')) as schema_file:
            self.CONFIG_SCHEMA = json.load(schema_file)

    def create_ontology_from_config(self, config_path: str) -> None:
        try:
            with open(config_path, 'r') as file:
                ontology_config = json.load(file)
            
            validate(instance=ontology_config, schema=self.CONFIG_SCHEMA)
            
            ontology_iri = ontology_config["ontology_iri"]
            self.onto = get_ontology(ontology_iri)

            with self.onto:
                self._create_classes(ontology_config["classes"])
                self._create_object_properties(ontology_config.get("object_properties", {}))
                self._create_data_properties(ontology_config.get("data_properties", {}))
                self._create_individuals(ontology_config.get("individuals", []))
                self._handle_disjoint_classes(ontology_config.get("disjoint_classes", []))
                self._handle_equivalent_classes(ontology_config.get("equivalent_classes", []))
                self._handle_general_axioms(ontology_config.get("general_axioms", []))
                self._add_annotations(ontology_config.get("annotations", {}))
                logger.info("Annotations added to the ontology")

            output_dir = config.get('General', 'output_dir')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_path = os.path.join(output_dir, "my_dynamic_ontology.owl")
            self.onto.save(file=output_path, format="rdfxml")
            default_world.save()
            logger.info(f"Ontology created and saved successfully to {output_path}")

            # Reload the ontology to ensure all changes are properly saved
            reloaded_onto = get_ontology(output_path).load()
            logger.info("Ontology reloaded for verification")
        
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in configuration file: {config_path}")
            raise
        except jsonschema.exceptions.ValidationError as ve:
            logger.error(f"Configuration validation error: {ve}")
            raise

    def _create_classes(self, classes_config: Dict[str, str]) -> None:
        self.classes = {}
        for cls, parent in classes_config.items():
            if parent == "Thing":
                self.classes[cls] = types.new_class(cls, (Thing,))
            else:
                self.classes[cls] = types.new_class(cls, (self.classes[parent],))
            logger.debug(f"Created class: {cls} with parent: {parent}")

    def _create_object_properties(self, properties_config: Dict[str, Dict]) -> None:
        for prop, details in properties_config.items():
            self._create_property(prop, ObjectProperty, details, unique_range=False)

    def _create_data_properties(self, properties_config: Dict[str, Dict]) -> None:
        for prop, details in properties_config.items():
            self._create_property(prop, DataProperty, details, unique_range=True)

    def _create_property(self, prop_name: str, prop_type: Union[Type[ObjectProperty], Type[DataProperty]], details: Dict, unique_range: bool = False) -> None:
        prop = types.new_class(prop_name, (prop_type,))
        
        # Assign property types correctly
        property_types = details.get("property_type", [])
        if "FunctionalProperty" in property_types and FunctionalProperty not in prop.is_a:
            prop.is_a.append(FunctionalProperty)
        if "InverseFunctionalProperty" in property_types and InverseFunctionalProperty not in prop.is_a:
            prop.is_a.append(InverseFunctionalProperty)
        if "TransitiveProperty" in property_types and TransitiveProperty not in prop.is_a:
            prop.is_a.append(TransitiveProperty)

        prop.domain = [self.classes[cls] for cls in details["domain"]]
        
        if prop_type == ObjectProperty:
            prop.range = [self.classes[r] for r in details["range"]]
        else:  # DataProperty
            if unique_range:
                prop.range = list(set(self._get_range_type(r) for r in details["range"]))
            else:
                prop.range = [self._get_range_type(r) for r in details["range"]]
        
        if "inverse_property" in details:
            inv_prop = types.new_class(details["inverse_property"], (ObjectProperty,))
            inv_prop.inverse_property = prop
        
        logger.debug(f"Created property: {prop_name} of type {prop_type.__name__}")

    def _get_range_type(self, range_type: str):
        if range_type == "int":
            return int
        elif range_type == "float":
            return float
        elif range_type == "str":
            return str
        elif range_type == "bool":
            return bool
        elif range_type == "datetime.date":
            return datetime.date
        elif range_type == "datetime.time":
            return datetime.time
        elif range_type == "datetime.datetime":
            return datetime.datetime
        else:
            return self.classes[range_type]

    def _create_individuals(self, individuals_config: List[Dict]) -> None:
        for individual in individuals_config:
            ind = self.classes[individual["class"]](individual["name"])
            for attr, values in individual.get("attributes", {}).items():
                prop = getattr(self.onto, attr)
                if prop.is_functional_for(ind.__class__):
                    setattr(ind, prop.name, values[0])
                else:
                    for value in values:
                        getattr(ind, prop.name).append(value)
            logger.debug(f"Created individual: {individual['name']} of class {individual['class']}")

    def _handle_disjoint_classes(self, disjoint_classes: List[str]) -> None:
        if disjoint_classes:
            AllDisjoint([self.classes[cls] for cls in disjoint_classes])
            logger.debug(f"Set disjoint classes: {disjoint_classes}")

    def _handle_equivalent_classes(self, equivalent_classes: List[Dict]) -> None:
        for eq in equivalent_classes:
            if eq["class"] not in self.classes or eq["equivalent_to"][0] not in self.classes:
                logger.error(f"Class '{eq['class']}' or its equivalent '{eq['equivalent_to'][0]}' is not defined in the ontology classes.")
                continue
            self.classes[eq["class"]].equivalent_to.append(self.classes[eq["equivalent_to"][0]])
            logger.debug(f"Set equivalent classes: {eq['class']} and {eq['equivalent_to'][0]}")

    def _handle_general_axioms(self, general_axioms: List[Dict]) -> None:
        for axiom in general_axioms:
            if axiom["axiom_type"] == "TransitiveProperty":
                for prop_name in axiom["properties"]:
                    prop = getattr(self.onto, prop_name)
                    prop.is_a.append(TransitiveProperty)
                    logger.debug(f"Set {prop_name} as TransitiveProperty")
            # Add more axiom types as needed

    def _add_annotations(self, annotations_config: Dict[str, Dict]) -> None:
        for ann, details in annotations_config.items():
            ann_prop = types.new_class(ann, (AnnotationProperty,))
            for target, values in details.items():
                if hasattr(self.onto, target):
                    entity = getattr(self.onto, target)
                    for value in values:
                        ann_prop[entity].append(value)
                    logger.debug(f"Added annotation {ann} to {target} with values {values}")
                else:
                    logger.warning(f"Target '{target}' for annotation '{ann}' not found in the ontology.")

def create_ontology_from_config(config_path: str) -> None:
    creator = OntologyCreator()
    creator.create_ontology_from_config(config_path)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create an ontology from a configuration file.")
    parser.add_argument("config", help="Path to the configuration JSON file")
    args = parser.parse_args()
    
    create_ontology_from_config(args.config)