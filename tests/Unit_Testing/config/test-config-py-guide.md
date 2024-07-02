# Testing Guide for config.py

## Overview
The `config.py` file is responsible for loading and parsing the `ontology_agent.ini` file. It's crucial to test this file thoroughly as it affects the entire project.

## Test Cases

1. Test loading a valid configuration file
```python
def test_load_valid_config(tmp_path):
    valid_config = """
    [General]
    root_dir = test_datasets
    output_dir = test_output
    
    [OntologyCreator]
    config_schema_path = test_config/ontology_config_schema.json
    """
    config_file = tmp_path / "valid_config.ini"
    config_file.write_text(valid_config)
    
    config = load_config(str(config_file))
    assert config.get('General', 'root_dir') == 'test_datasets'
    assert config.get('General', 'output_dir') == 'test_output'
    assert config.get('OntologyCreator', 'config_schema_path') == 'test_config/ontology_config_schema.json'
```

2. Test loading a non-existent configuration file
```python
def test_load_nonexistent_config():
    with pytest.raises(FileNotFoundError):
        load_config('nonexistent_config.ini')
```

3. Test loading a malformed configuration file
```python
def test_load_malformed_config(tmp_path):
    malformed_config = """
    [General
    root_dir = test_datasets
    """
    config_file = tmp_path / "malformed_config.ini"
    config_file.write_text(malformed_config)
    
    with pytest.raises(configparser.ParsingError):
        load_config(str(config_file))
```

4. Test getting values of different types
```python
def test_config_value_types(tmp_path):
    config_content = """
    [TestSection]
    string_value = hello
    int_value = 42
    float_value = 3.14
    bool_value = true
    """
    config_file = tmp_path / "type_test_config.ini"
    config_file.write_text(config_content)
    
    config = load_config(str(config_file))
    assert config.get('TestSection', 'string_value') == 'hello'
    assert config.getint('TestSection', 'int_value') == 42
    assert config.getfloat('TestSection', 'float_value') == 3.14
    assert config.getboolean('TestSection', 'bool_value') == True
```

5. Test fallback values
```python
def test_config_fallback_values(tmp_path):
    config_content = """
    [TestSection]
    existing_value = exists
    """
    config_file = tmp_path / "fallback_test_config.ini"
    config_file.write_text(config_content)
    
    config = load_config(str(config_file))
    assert config.get('TestSection', 'existing_value') == 'exists'
    assert config.get('TestSection', 'non_existing_value', fallback='default') == 'default'
```

These tests cover the main functionalities of the `config.py` file, including loading valid configurations, handling errors, and retrieving values of different types.

