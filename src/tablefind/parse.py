import os
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field
import yaml

class FieldType(str, Enum):
    STRING = "string"
    DATE = "date"
    CURRENCY = "currency"
    LIST = "list"
    TEXT = "text"
    TABLE = "table"

class FieldConfig(BaseModel):
    type: FieldType
    required: bool = False
    format: Optional[str] = None
    hints: List[str]

class TableMetadata(BaseModel):
    extract_extra_keys: bool = False
    include_filename: bool = False
    include_page_number: bool = False

class TableConfig(BaseModel):
    name: str
    description: str
    metadata: TableMetadata
    fields: Dict[str, FieldConfig]

class GenericExtractionMetadata(TableMetadata):
    max_fields: int = Field(20, ge=1)

class GenericExtraction(BaseModel):
    enabled: bool = True
    instructions: str
    metadata: GenericExtractionMetadata

class DocumentExtractionConfig(BaseModel):
    global_instructions: str
    generic_extraction: GenericExtraction
    tables: Dict[str, TableConfig]

def load_config(file_path: str = "tablefind.yaml") -> DocumentExtractionConfig:
    """
    Load and parse the YAML configuration file.
    
    Args:
    file_path (str): Path to the YAML configuration file. Defaults to "tablefind.yaml" in the current directory.
    
    Returns:
    DocumentExtractionConfig: Parsed configuration object.
    
    Raises:
    FileNotFoundError: If the specified file is not found.
    yaml.YAMLError: If there's an error parsing the YAML file.
    ValidationError: If the YAML content doesn't match the expected structure.
    """
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        try:
            config_dict = yaml.safe_load(file)
            return DocumentExtractionConfig(**config_dict)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file: {e}")

def get_table_config(config: DocumentExtractionConfig, table_name: str) -> Optional[TableConfig]:
    """
    Retrieve the configuration for a specific table.
    
    Args:
    config (DocumentExtractionConfig): The loaded configuration object.
    table_name (str): The name of the table to retrieve.
    
    Returns:
    Optional[TableConfig]: The configuration for the specified table, or None if not found.
    """
    return config.tables.get(table_name)

def is_generic_extraction_enabled(config: DocumentExtractionConfig) -> bool:
    """
    Check if generic extraction is enabled in the configuration.
    
    Args:
    config (DocumentExtractionConfig): The loaded configuration object.
    
    Returns:
    bool: True if generic extraction is enabled, False otherwise.
    """
    return config.generic_extraction.enabled

if __name__ == "__main__":
    # Example usage
    try:
        config = load_config()
        print(f"Loaded configuration successfully.")
        print(f"Global instructions: {config.global_instructions[:50]}...")
        print(f"Number of defined tables: {len(config.tables)}")
        print(f"Generic extraction enabled: {is_generic_extraction_enabled(config)}")
        
        # Example of accessing a specific table configuration
        invoice_config = get_table_config(config, "invoice_summary")
        if invoice_config:
            print(f"Invoice summary table fields: {', '.join(invoice_config.fields.keys())}")
        else:
            print("Invoice summary table not found in configuration.")
    
    except Exception as e:
        print(f"Error loading configuration: {e}")