# Document to Excel Converter

This project provides a robust pipeline for extracting tables from PDF documents and converting them into well-structured Excel workbooks. It uses AI-assisted decision making to organize the extracted data into appropriate sheets and tables within the Excel file.

## Features

- Extract tables from multiple PDF documents
- AI-assisted sheet and table organization
- Customizable table extraction and Excel generation through YAML configuration
- Preserve styling information from source documents
- User-friendly command-line interface

## Components

1. `parse.py`: Defines Pydantic models for configuration and handles YAML config parsing.
2. `table_models.py`: Extends base table models with additional metadata and styling information.
3. `table_resolve.py`: Determines the structure of the Excel workbook based on extracted tables and user preferences.
4. `sheet_adapter.py`: Handles the creation of Excel workbooks using Openpyxl.
5. `main.py`: Provides the command-line interface and orchestrates the entire conversion process.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/document-to-excel-converter.git
   cd document-to-excel-converter
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Basic usage:
```
python main.py document1.pdf document2.pdf
```

This will process the specified PDF documents and create an `output.xlsx` file in the current directory.

### Options

- `-o, --output`: Specify the output Excel file path (default: output.xlsx)
- `-c, --config`: Specify a custom YAML configuration file path (default: tablefind.yaml)
- `-s, --sheet-name`: Specify a name for the main sheet in the output workbook
- `-v, --verbose`: Enable verbose output for more detailed processing information

Example with options:
```
python main.py document1.pdf document2.pdf -o my_workbook.xlsx -c my_config.yaml -s "Summary" -v
```

Run `python main.py --help` for more information on available options.

## Configuration

The behavior of the table extraction and Excel generation can be customized through a YAML configuration file. By default, the program looks for `tablefind.yaml` in the current directory. You can specify a different configuration file using the `-c` or `--config` option.

Example configuration structure:
```yaml
global_instructions: |
  Instructions for AI-assisted extraction...

tables:
  invoice_summary:
    name: "Invoice Summary"
    description: "Summary table for invoice data"
    fields:
      invoice_number:
        type: "string"
        required: true
        hints:
          - "Usually labeled as 'Invoice No.', 'Invoice #', or similar"
      # ... other fields ...

  # ... other table types ...

generic_extraction:
  enabled: true
  instructions: |
    Instructions for generic extraction...
  metadata:
    max_fields: 20
```

Refer to the sample configuration file for more details on available options.

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The creators and maintainers of the libraries used in this project, including Pydantic, Openpyxl, and Click
- The Docprompt library for PDF extraction