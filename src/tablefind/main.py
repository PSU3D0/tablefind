import click
import asyncio
import os
from typing import List
import yaml
from parse import load_config, DocumentExtractionConfig
from src.tablefind.table_models import ExtendedExtractedTable, ExtendedTableCell, ExtendedTableHeader, ExtendedTableRow
from src.tablefind.table_resolve import resolve_sheets
from sheet_adapter import create_excel_workbook, save_workbook

async def mock_extract_tables(pdf_path: str) -> List[ExtendedExtractedTable]:
    """Mock function to simulate table extraction from a PDF."""
    # In a real implementation, this would use a PDF parsing library and your extraction logic
    return [
        ExtendedExtractedTable(
            source_document=os.path.basename(pdf_path),
            page_number=1,
            title=f"Mock Table from {os.path.basename(pdf_path)}",
            headers=[
                ExtendedTableHeader(text="Column 1"),
                ExtendedTableHeader(text="Column 2"),
            ],
            rows=[
                ExtendedTableRow(cells=[
                    ExtendedTableCell(text="Data 1"),
                    ExtendedTableCell(text="Data 2"),
                ]),
                ExtendedTableRow(cells=[
                    ExtendedTableCell(text="Data 3"),
                    ExtendedTableCell(text="Data 4"),
                ]),
            ]
        )
    ]

async def process_documents(pdf_paths: List[str], config: DocumentExtractionConfig) -> List[ExtendedExtractedTable]:
    all_tables = []
    for pdf_path in pdf_paths:
        tables = await mock_extract_tables(pdf_path)
        all_tables.extend(tables)
    return all_tables

@click.command()
@click.argument('pdf_paths', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--output', '-o', default='output.xlsx', help='Path for the output Excel workbook.')
@click.option('--config', '-c', default='tablefind.yaml', help='Path to the YAML configuration file.')
@click.option('--sheet-name', '-s', help='Name for the main sheet in the output workbook.')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output.')
async def convert_to_workbook(pdf_paths, output, config, sheet_name, verbose):
    """Convert PDF documents to an Excel workbook with extracted tables."""
    if verbose:
        click.echo(f"Processing the following PDF files: {', '.join(pdf_paths)}")
        click.echo(f"Using configuration file: {config}")

    try:
        # Load configuration
        extraction_config = load_config(config)
        
        # Process documents and extract tables
        all_tables = await process_documents(pdf_paths, extraction_config)
        
        if verbose:
            click.echo(f"Extracted {len(all_tables)} tables from {len(pdf_paths)} documents.")

        # Prepare user preferences
        user_preferences = {
            "preferred_sheet_names": [sheet_name] if sheet_name else []
        }

        # Resolve sheets
        workbook_config = await resolve_sheets(all_tables, user_preferences)

        if verbose:
            click.echo(f"Resolved workbook structure with {len(workbook_config.sheets)} sheets.")

        # Create Excel workbook
        wb = create_excel_workbook(workbook_config)

        # Save the workbook
        save_workbook(wb, output)

        click.echo(f"Excel workbook created successfully: {output}")

    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    asyncio.run(convert_to_workbook())