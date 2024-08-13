from docprompt.tasks.table_extraction.schema import (
    ExtractedTable,
    TableHeader,
    TableCell,
    TableRow
)

from typing import List, Optional, Dict
from pydantic import BaseModel, Field



class StyleInfo(BaseModel):
    font_name: Optional[str] = None
    font_size: Optional[float] = None
    font_color: Optional[str] = None
    background_color: Optional[str] = None
    bold: bool = False
    italic: bool = False
    underline: bool = False

class ExtendedTableHeader(TableHeader):
    style: Optional[StyleInfo] = None

class ExtendedTableCell(TableCell):
    style: Optional[StyleInfo] = None

class ExtendedTableRow(TableRow):
    cells: List[ExtendedTableCell] = Field(default_factory=list)
    style: Optional[StyleInfo] = None

class ExtendedExtractedTable(ExtractedTable):
    source_document: str
    page_number: int
    headers: List[ExtendedTableHeader] = Field(default_factory=list)
    rows: List[ExtendedTableRow] = Field(default_factory=list)
    style: Optional[StyleInfo] = None

    def to_markdown_string(self) -> str:
        markdown = f"Source: {self.source_document}, Page: {self.page_number}\n\n"
        markdown += super().to_markdown_string()
        return markdown

    def to_dict_with_styles(self) -> Dict:
        return {
            "source_document": self.source_document,
            "page_number": self.page_number,
            "title": self.title,
            "style": self.style.dict() if self.style else None,
            "headers": [
                {
                    "text": header.text,
                    "bbox": header.bbox,
                    "style": header.style.dict() if header.style else None
                }
                for header in self.headers
            ],
            "rows": [
                {
                    "cells": [
                        {
                            "text": cell.text,
                            "bbox": cell.bbox,
                            "style": cell.style.dict() if cell.style else None
                        }
                        for cell in row.cells
                    ],
                    "bbox": row.bbox,
                    "style": row.style.dict() if row.style else None
                }
                for row in self.rows
            ]
        }