
# OntologyAgent

OntologyAgent is an adaptive autonomous AI agent designed for scaling and maintaining ontologies. It leverages the strengths of both Owlready2 for creation and modification and DeepOnto for advanced processing, ensuring conceptual coherence in intelligent systems. This agent is capable of creating, modifying, and processing ontologies autonomously for enhanced decision-making and reasoning functions.

## Features

- **Creation and Modification**: Uses Owlready2 for defining classes, properties, and individuals.
- **Advanced Processing**: Employs DeepOnto for querying entities, performing reasoning, and ontology alignment.
- **Adaptability**: Integrates machine learning algorithms to enhance ontology management capabilities.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/inquisitour/OntologyAgent.git
    cd OntologyAgent
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Create Ontology

To create and save an ontology:
```bash
python main.py create
```

### Process Ontology

To load and process an ontology:
```bash
python main.py process
```

### Align Ontologies

To align two ontologies:
```bash
python main.py align
```

## Project Structure

```
OntologyAgent/
│
├── data/
│   ├── my_ontology.owl
│
├── modules/
│   ├── __init__.py
│   ├── ontology_creator.py
│   ├── ontology_processor.py
│   ├── ontology_aligner.py
│
├── scripts/
│   ├── create_ontology.py
│   ├── process_ontology.py
│   ├── align_ontologies.py
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

## Modules

### `modules/ontology_creator.py`
Module for creating and modifying ontologies using Owlready2.

### `modules/ontology_processor.py`
Module for loading and processing ontologies with DeepOnto.

### `modules/ontology_aligner.py`
Module for aligning ontologies using BERTMap in DeepOnto.

## Scripts

### `scripts/create_ontology.py`
Script to create and save the ontology.

### `scripts/process_ontology.py`
Script to load and process the ontology.

### `scripts/align_ontologies.py`
Script to align two ontologies.

## Contributing

We welcome contributions to enhance the capabilities of OntologyAgent. Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the Apache-2.0 License. See the LICENSE file for details.
