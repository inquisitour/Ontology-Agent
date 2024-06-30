from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ontology-agent",
    version="0.1.0",
    author="Pratik Deshmukh",
    author_email="deshmukhpratik931@gmail.com",
    description="An autonomous AI agent system for creating, processing, aligning, and matching ontologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inquisitour/ontology-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "owlready2==0.36",
        "jsonschema==3.2.0",
        "deeponto==0.0.1",
        "LLMs4OM==0.0.1",
    ],
    entry_points={
        "console_scripts": [
            "ontology-agent=main:main",
        ],
    },
)