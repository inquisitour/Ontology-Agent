# OntologyAgent

![OntologyAgent](images/ontoAgent.jpg)

OntologyAgent is an adaptive autonomous AI agent designed for scaling and maintaining ontologies. It leverages the strengths of Owlready2 for creation and modification, DeepOnto for advanced processing, and LLMs4OM for sophisticated ontology matching. This agent is capable of creating, modifying, and processing ontologies autonomously for enhanced decision-making and reasoning functions.

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
OntologyAgent/
│
├── LLMs4OM/
│   ├── .env-example
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   └── ...
├── data/
│   ├── my_ontology.owl
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
