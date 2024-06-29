# Ontology Agent [Under Development]

<p align="center">
  <img src="images/ontoAgent.jpg" alt="OntologyAgent">
</p>

<p align="center">
  <a href="https://github.com/inquisitour/OntologyAgent/actions/workflows/pre-commit.yml">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen" alt="pre-commit enabled">
  </a>
  <a href="https://github.com/inquisitour/OntologyAgent/actions/workflows/code_style.yml">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
  </a>
  <a href="https://github.com/inquisitour/OntologyAgent/actions/workflows/imports.yml">
    <img src="https://img.shields.io/badge/imports-isort-1c91e6" alt="Imports: isort">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache-2.0">
  </a>
  <a href="https://example.com/paper.pdf">
    <img src="https://img.shields.io/badge/Paper-pdf-red" alt="Paper">
  </a>
  <a href="https://example.com/supplementary_material.pdf">
    <img src="https://img.shields.io/badge/Supplementary%20Material-pdf-black" alt="Supplementary Material">
  </a>
</p>

Ontology Agent is an adaptive autonomous AI agent designed for creating, scaling and maintaining ontologies. It leverages the strengths of Owlready2 for creation and modification, DeepOnto for advanced processing, and LLMs4OM for sophisticated ontology matching. This agent is capable of creating, modifying, and processing ontologies autonomously for enhanced decision-making and reasoning functions.

## Features

- **Creation and Modification**: Uses Owlready2 for defining classes, properties, and individuals.
- **Advanced Processing**: Employs DeepOnto for querying entities, performing reasoning, and ontology alignment.
- **Sophisticated Matching**: Utilizes LLMs4OM for effective ontology matching using large language models.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/inquisitour/OntologyAgent.git
    cd OntologyAgent
    ```

2. **Add LLMs4OM as a Submodule**
    ```bash
    git submodule add https://github.com/HamedBabaei/LLMs4OM.git LLMs4OM
    git submodule update --init --recursive
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**
    - Rename the `.env-example` file to `.env`.
    - Update the `.env` file with appropriate tokens if you plan to use specific LLMs like LLaMA-2 or GPT-3.5. If not, you can use dummy tokens.

5. **Configuration for ontology**

- Customize the config/ontology_config.json file to define your ontology's classes, properties, individuals, disjoint classes, equivalent classes, and general axioms. This configuration file allows you to 
  specify the structure and elements of your ontology flexibly.

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

### Match Ontologies

To match ontologies using LLMs4OM:
```bash
python main.py match
```

## Project Structure

```
Ontology-Agent/
│
├── LLMs4OM/
│   ├── .env-example
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   └── ...
│
├── config/
│   ├── ontology_config.json
│
├── data/
│   ├── my_ontology.owl
│
├── images/
│   ├── ontoAgent.jpg
│
├── modules/
│   ├── __init__.py
│   ├── ontology_creator.py
│   ├── ontology_processor.py
│   ├── ontology_aligner.py
│   ├── ontology_matcher.py
│
├── scripts/
│   ├── create_ontology.py
│   ├── process_ontology.py
│   ├── align_ontologies.py
│   ├── match_ontologies.py
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

### `modules/ontology_matcher.py`
Module for matching ontologies using LLMs4OM.

## Scripts

### `scripts/create_ontology.py`
Script to create and save the ontology.

### `scripts/process_ontology.py`
Script to load and process the ontology.

### `scripts/align_ontologies.py`
Script to align two ontologies.

### `scripts/match_ontologies.py`
Script to match ontologies using LLMs4OM.

## Contributing

We welcome contributions to enhance the capabilities of OntologyAgent. Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the Apache-2.0 License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please contact [deshmukhpratik931@gmail.com].

---

For more detailed information, visit the [OntologyAgent GitHub repository](https://github.com/inquisitour/OntologyAgent).
