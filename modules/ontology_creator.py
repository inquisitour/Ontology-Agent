import json
from owlready2 import *

def create_ontology_from_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    ontology_iri = config["ontology_iri"]
    onto = get_ontology(ontology_iri)

    def create_class(class_name, parent="Thing"):
        with onto:
            parent_class = Thing if parent == "Thing" else getattr(onto, parent)
            cls = types.new_class(class_name, (parent_class,))
        return cls

    def create_property(prop_name, prop_type, domain, range_, extra_types=[]):
        with onto:
            base_class = ObjectProperty if prop_type == "ObjectProperty" else DataProperty
            prop = types.new_class(prop_name, (base_class,))
            for etype in extra_types:
                prop.is_a.append(eval(etype))
            prop.domain = [getattr(onto, cls) for cls in domain]
            prop.range = [eval(r) if r in ["int", "float", "str", "bool"] else getattr(onto, r) for r in range_]
        return prop

    # Create classes
    classes = {cls: create_class(cls, parent) for cls, parent in config["classes"].items()}

    # Create object properties
    for prop, details in config.get("object_properties", {}).items():
        create_property(prop, "ObjectProperty", details["domain"], details["range"], details.get("property_type", []))
        if "inverse_property" in details:
            with onto:
                inv_prop = types.new_class(details["inverse_property"], (ObjectProperty,))
                inv_prop.inverse_property = getattr(onto, prop)

    # Create data properties
    for prop, details in config.get("data_properties", {}).items():
        create_property(prop, "DataProperty", details["domain"], details["range"], details.get("property_type", []))

    # Create individuals
    for individual in config["individuals"]:
        with onto:
            ind = classes[individual["class"]](individual["name"])
            for attr, values in individual["attributes"].items():
                prop = getattr(onto, attr)
                for value in values:
                    setattr(ind, prop.name, value)
    
    # Handle disjoint classes
    if "disjoint_classes" in config:
        with onto:
            AllDisjoint([classes[cls] for cls in config["disjoint_classes"]])

    # Handle equivalent classes
    if "equivalent_classes" in config:
        for eq in config["equivalent_classes"]:
            with onto:
                cls = classes[eq["class"]]
                cls.equivalent_to.append(getattr(onto, eq["equivalent_to"][0]))

    # Handle general axioms
    if "general_axioms" in config:
        for axiom in config["general_axioms"]:
            with onto:
                eval(axiom["axiom_type"])([getattr(onto, prop) for prop in axiom["properties"]])

    onto.save(file="my_dynamic_ontology.owl")
    sync_reasoner()  # Perform reasoning

if __name__ == "__main__":
    create_ontology_from_config("ontology_config.json")
