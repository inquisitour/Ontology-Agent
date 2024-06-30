# Ontology Agent [Under Development]

<p align="center">
  <img src="images/ontoAgent.jpg" alt="Ontology-Agent">
</p>

<p align="center">
  <a href="https://github.com/inquisitour/Ontology-Agent/actions/workflows/pre-commit.yml">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen" alt="pre-commit enabled">
  </a>
  <a href="https://github.com/inquisitour/Ontology-Agent/actions/workflows/code_style.yml">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black">
  </a>
  <a href="https://github.com/inquisitour/Ontology-Agent/actions/workflows/imports.yml">
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

## 🌟 Introduction

Welcome to Ontology Agent, your all-in-one solution for creating, scaling, and maintaining ontologies with the power of AI! This adaptive autonomous agent combines the robust capabilities of Owlready2, the advanced processing of DeepOnto, and the sophisticated matching algorithms of LLMs4OM to revolutionize your ontology management workflow.

Whether you're a seasoned ontology engineer or just starting your journey in knowledge representation, Ontology Agent is designed to streamline your work and enhance your decision-making processes.

## 🚀 Features

Ontology Agent is packed with powerful features to make your ontology management tasks a breeze:

- **Intelligent Creation and Modification**: Harness the power of Owlready2 to effortlessly define classes, properties, and individuals.
- **Advanced Processing and Reasoning**: Leverage DeepOnto's capabilities for sophisticated querying, reasoning, and ontology alignment.
- **State-of-the-Art Matching**: Utilize cutting-edge large language models through LLMs4OM for precise and efficient ontology matching.
- **Flexible Configuration**: Easily customize your ontology structure using our intuitive JSON configuration system.
- **Comprehensive Testing**: Ensure reliability with our extensive pytest-based testing suite.

## 🛠️ Installation

Get up and running with Ontology Agent in just a few simple steps:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/inquisitour/Ontology-Agent.git
    cd Ontology-Agent
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
    - Rename `.env-example` to `.env`
    - Update `.env` with appropriate tokens for LLMs (e.g., LLaMA-2 or GPT-3.5)

5. **Customize Your Ontology**
    - Edit `config/ontology_config.json` to define your ontology structure

## 💡 Usage

Ontology Agent offers a simple command-line interface for all your ontology management needs:

### Create Ontology
```bash
python main.py create
```

### Process Ontology
```bash
python main.py process
```

### Align Ontologies
```bash
python main.py align
```

### Match Ontologies
```bash
python main.py match
```

## 📁 Project Structure

Our well-organized project structure ensures easy navigation and maintenance:

```
Ontology-Agent/
├── config/
│   ├── ontology_agent.ini
│   ├── ontology_config_schema.json
├── data/
├── modules/
│   ├── __init__.py
│   ├── config.py
│   ├── ontology_creator.py
│   ├── ontology_processor.py
│   ├── ontology_aligner.py
│   ├── ontology_matcher.py
├── scripts/
│   ├── create_ontology.py
│   ├── process_ontology.py
│   ├── align_ontologies.py
│   ├── match_ontologies.py
├── tests/
│   ├── __init__.py
│   ├── test_ontology_creator.py
│   ├── test_ontology_processor.py
│   ├── test_ontology_aligner.py
│   ├── test_ontology_matcher.py
├── main.py
├── requirements.txt
├── setup.py
├── README.md
├── .gitignore
```

## 🧠 Core Modules

Ontology Agent's power comes from its four core modules:

- **ontology_creator.py**: Create and modify ontologies with ease using Owlready2.
- **ontology_processor.py**: Process and analyze ontologies using DeepOnto's advanced capabilities.
- **ontology_aligner.py**: Align ontologies with precision using BERTMap in DeepOnto.
- **ontology_matcher.py**: Match ontologies efficiently with LLMs4OM's state-of-the-art algorithms.

## 🧪 Testing

We take quality seriously. Our comprehensive test suite ensures reliability:

```bash
pytest tests/
```

## 🤝 Contributing

We believe in the power of community! If you have ideas to enhance Ontology Agent, here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

Have questions or suggestions? We'd love to hear from you!

Email: [deshmukhpratik931@gmail.com](mailto:deshmukhpratik931@gmail.com)

---

Dive deeper into the world of Ontology Agent by visiting our [GitHub repository](https://github.com/inquisitour/Ontology-Agent). Start your journey towards effortless ontology management today!