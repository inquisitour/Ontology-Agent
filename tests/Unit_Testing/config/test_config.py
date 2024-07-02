import pytest
import configparser
from modules.config import load_config, Config

@pytest.fixture
def sample_config_content():
    return """
    [General]
    root_dir = test_datasets
    output_dir = test_output

    [OntologyCreator]
    config_schema_path = test_config/ontology_config_schema.json

    [OntologyProcessor]
    reasoning_enabled = true

    [OntologyAligner]
    alignment_method = BERTMap
    confidence_threshold = 0.7

    [OntologyMatcher]
    matcher_model = MistralLLMBertRAG
    llm_confidence_threshold = 0.7
    ir_score_threshold = 0.9

    [Logging]
    level = INFO
    format = %%(asctime)s - %%(levelname)s - %%(message)s

    [TestSection]
    string_value = hello
    int_value = 42
    float_value = 3.14
    bool_value = true
    """

@pytest.fixture
def sample_config_file(tmp_path, sample_config_content):
    config_file = tmp_path / "test_config.ini"
    config_file.write_text(sample_config_content)
    return str(config_file)

def test_load_valid_config(sample_config_file):
    config = load_config(sample_config_file)
    assert isinstance(config, Config)
    assert config.get('General', 'root_dir') == 'test_datasets'
    assert config.get('General', 'output_dir') == 'test_output'
    assert config.get('OntologyCreator', 'config_schema_path') == 'test_config/ontology_config_schema.json'
    assert config.getboolean('OntologyProcessor', 'reasoning_enabled') == True
    assert config.get('Logging', 'level') == 'INFO'
    assert config.get('OntologyAligner', 'alignment_method') == 'BERTMap'
    assert config.getfloat('OntologyAligner', 'confidence_threshold') == 0.7
    assert config.get('OntologyMatcher', 'matcher_model') == 'MistralLLMBertRAG'
    assert config.getfloat('OntologyMatcher', 'llm_confidence_threshold') == 0.7
    assert config.getfloat('OntologyMatcher', 'ir_score_threshold') == 0.9

def test_load_nonexistent_config():
    with pytest.raises(FileNotFoundError):
        load_config('nonexistent_config.ini')

def test_load_malformed_config(tmp_path):
    malformed_config = """
    [General
    root_dir = test_datasets
    """
    config_file = tmp_path / "malformed_config.ini"
    config_file.write_text(malformed_config)
    
    with pytest.raises(configparser.ParsingError):
        load_config(str(config_file))

def test_config_value_types(sample_config_file):
    config = load_config(sample_config_file)
    assert isinstance(config.get('TestSection', 'string_value'), str)
    assert isinstance(config.getint('TestSection', 'int_value'), int)
    assert isinstance(config.getfloat('TestSection', 'float_value'), float)
    assert isinstance(config.getboolean('TestSection', 'bool_value'), bool)

def test_config_specific_values(sample_config_file):
    config = load_config(sample_config_file)
    assert config.get('TestSection', 'string_value') == 'hello'
    assert config.getint('TestSection', 'int_value') == 42
    assert config.getfloat('TestSection', 'float_value') == 3.14
    assert config.getboolean('TestSection', 'bool_value') == True

def test_config_fallback_values(sample_config_file):
    config = load_config(sample_config_file)
    assert config.get('TestSection', 'nonexistent_key', fallback='default') == 'default'
    assert config.getint('TestSection', 'nonexistent_int', fallback=10) == 10
    assert config.getfloat('TestSection', 'nonexistent_float', fallback=1.23) == 1.23
    assert config.getboolean('TestSection', 'nonexistent_bool', fallback=False) == False

def test_get_section(sample_config_file):
    config = load_config(sample_config_file)
    general_section = config.get_section('General')
    assert isinstance(general_section, dict)
    assert general_section['root_dir'] == 'test_datasets'
    assert general_section['output_dir'] == 'test_output'

def test_get_nonexistent_section(sample_config_file):
    config = load_config(sample_config_file)
    nonexistent_section = config.get_section('NonexistentSection')
    assert isinstance(nonexistent_section, dict)
    assert len(nonexistent_section) == 0