import logging
from typing import List, Tuple, Dict
from owlready2 import *
from modules.config import load_config

config = load_config()
logging.basicConfig(level=config.get('Logging', 'level'), format=config.get('Logging', 'format'))
logger = logging.getLogger(__name__)

class OntologyProcessor:
    def __init__(self, ontology_path: str):
        try:
            self.ontology = get_ontology(ontology_path).load()
            self.reasoning_enabled = config.getboolean('OntologyProcessor', 'reasoning_enabled', fallback=False)
            logger.info(f"Loaded ontology from {ontology_path}")
            if self.reasoning_enabled:
                logger.info("Reasoning is enabled")
                sync_reasoner(self.ontology)
        except FileNotFoundError:
            logger.error(f"Ontology file not found: {ontology_path}")
            raise

    def query_entities(self) -> Tuple[List[Thing], List[Property]]:
        classes = list(self.ontology.classes())
        properties = list(self.ontology.properties())
        logger.info(f"Queried {len(classes)} classes and {len(properties)} properties")
        return classes, properties

    def perform_reasoning(self, concept_name: str) -> List[Thing]:
        try:
            if self.reasoning_enabled:
                sync_reasoner(self.ontology)
            concept = getattr(self.ontology, concept_name)
            inferred_subsumers = list(concept.ancestors())
            logger.info(f"Performed reasoning on {concept_name}, found {len(inferred_subsumers)} inferred subsumers")
            return inferred_subsumers
        except AttributeError:
            logger.error(f"Concept not found in ontology: {concept_name}")
            raise

    def query_subclasses(self, class_name: str) -> List[Thing]:
        try:
            cls = getattr(self.ontology, class_name)
            subclasses = list(cls.subclasses())
            logger.info(f"Queried subclasses of {class_name}, found {len(subclasses)} subclasses")
            return subclasses
        except AttributeError:
            logger.error(f"Class not found in ontology: {class_name}")
            raise

    def query_individuals(self, class_name: str) -> List[Thing]:
        try:
            cls = getattr(self.ontology, class_name)
            individuals = list(cls.instances())
            logger.info(f"Queried individuals of {class_name}, found {len(individuals)} individuals")
            return individuals
        except AttributeError:
            logger.error(f"Class not found in ontology: {class_name}")
            raise

    def query_object_properties(self) -> List[ObjectProperty]:
        object_properties = list(self.ontology.object_properties())
        logger.info(f"Queried {len(object_properties)} object properties")
        return object_properties

    def query_data_properties(self) -> List[DataProperty]:
        data_properties = list(self.ontology.data_properties())
        logger.info(f"Queried {len(data_properties)} data properties")
        return data_properties

    def query_annotations(self) -> Dict[str, Dict[str, List[str]]]:
        annotations = {}
        for entity in list(self.ontology.classes()) + list(self.ontology.individuals()):
            entity_annotations = {}
            for prop in self.ontology.annotation_properties():
                values = list(prop[entity])
                if values:
                    entity_annotations[prop.name] = values
            if entity_annotations:
                annotations[entity.name] = entity_annotations
        logger.info(f"Queried annotations for {len(annotations)} entities")
        return annotations

    def query_property_characteristics(self, property_name: str) -> List[str]:
        try:
            prop = getattr(self.ontology, property_name)
            characteristics = []
            
            if FunctionalProperty in prop.is_a:
                characteristics.append("FunctionalProperty")
            if InverseFunctionalProperty in prop.is_a:
                characteristics.append("InverseFunctionalProperty")
            if TransitiveProperty in prop.is_a:
                characteristics.append("TransitiveProperty")
            
            logger.info(f"Queried characteristics of {property_name}, found {len(characteristics)} characteristics")
            
            # Debugging: print the property and its characteristics
            print(f"Property: {property_name}, Characteristics: {characteristics}")
            
            return characteristics
        except AttributeError:
            logger.error(f"Property not found in ontology: {property_name}")
            raise

    def query_class_hierarchy(self) -> Dict[str, List[str]]:
        hierarchy = {}
        for cls in self.ontology.classes():
            parent_names = [parent.name for parent in cls.is_a if isinstance(parent, ThingClass)]
            for parent_name in parent_names:
                if parent_name not in hierarchy:
                    hierarchy[parent_name] = []
                hierarchy[parent_name].append(cls.name)
        logger.info(f"Queried class hierarchy, found {len(hierarchy)} parent classes")
        return hierarchy

    def query_property_domains_and_ranges(self, property_name: str) -> Tuple[List[Thing], List[Thing]]:
        try:
            prop = getattr(self.ontology, property_name)
            domains = list(prop.domain)
            ranges = list(prop.range)
            logger.info(f"Queried domains and ranges of {property_name}")
            return domains, ranges
        except AttributeError:
            logger.error(f"Property not found in ontology: {property_name}")
            raise

    def check_ontology_consistency(self) -> bool:
        try:
            with self.ontology:
                sync_reasoner()
            logger.info("Checked ontology consistency")
            return True
        except OwlReadyInconsistentOntologyError:
            logger.warning("Ontology is inconsistent")
            return False

    def get_ontology_metrics(self) -> Dict[str, int]:
        metrics = {
            "num_classes": len(list(self.ontology.classes())),
            "num_object_properties": len(list(self.ontology.object_properties())),
            "num_data_properties": len(list(self.ontology.data_properties())),
            "num_individuals": len(list(self.ontology.individuals())),
            "num_annotation_properties": len(list(self.ontology.annotation_properties())),
        }
        logger.info("Calculated ontology metrics")
        return metrics

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Process and query an ontology.")
    parser.add_argument("ontology", help="Path to the ontology file")
    parser.add_argument("--query", choices=["entities", "subclasses", "individuals", "annotations", "metrics"],
                        help="Type of query to perform")
    parser.add_argument("--class", dest="class_name", help="Class name for subclass or individual queries")
    args = parser.parse_args()

    processor = OntologyProcessor(args.ontology)

    if args.query == "entities":
        classes, properties = processor.query_entities()
        print(f"Classes: {[c.name for c in classes]}")
        print(f"Properties: {[p.name for p in properties]}")
    elif args.query == "subclasses" and args.class_name:
        subclasses = processor.query_subclasses(args.class_name)
        print(f"Subclasses of {args.class_name}: {[c.name for c in subclasses]}")
    elif args.query == "individuals" and args.class_name:
        individuals = processor.query_individuals(args.class_name)
        print(f"Individuals of {args.class_name}: {[i.name for i in individuals]}")
    elif args.query == "annotations":
        annotations = processor.query_annotations()
        for entity, ann in annotations.items():
            print(f"{entity}: {ann}")
    elif args.query == "metrics":
        metrics = processor.get_ontology_metrics()
        for metric, value in metrics.items():
            print(f"{metric}: {value}")
    else:
        print("Please specify a valid query type and provide necessary arguments.")
