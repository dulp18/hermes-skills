---
name: document-form-filling
description: Programmatically fill structured forms in Word (.docx) and Excel (.xlsx) with Chinese-language content using python-docx and openpyxl.
---

## Trigger

When the user asks you to fill structured forms (Word tables or Excel spreadsheets) with Chinese-language research content, survey responses, or similar text-heavy data.

## Core Pattern: JSON → Document

**Never embed Chinese text with special quotation marks (Chinese 「」""'') directly in Python `execute_code` calls.** The Chinese quotation marks `""` and `''` cause `SyntaxError: invalid character (U+FF0C/U+201C/etc.)` when they appear inside Python string literals, even in triple-quoted strings.

Instead, use a two-phase approach:

### Phase 1: Write JSON data file
Write all Chinese content into a JSON file using `write_file`. In JSON, Chinese quotation marks are safely escaped as `\u201c` / `\u201d` unicode escapes, or you can type them directly since JSON handles Unicode natively.

```json
{
  "row_1_col_1": "提示注入检测：识别如\u201c忽略上述指令\u201d的恶意提示",
  "row_2_col_1": "另一段包含\u2018中文引号\u2019的内容"
}
```

### Phase 2: Load JSON and fill document
In a separate `execute_code` call, load the JSON and iterate:
```python
import json
from docx import Document
from openpyxl import load_workbook

with open('/tmp/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# For Word tables
doc = Document('path.docx')
for table_idx, table in enumerate(doc.tables):
    for row_idx in range(1, len(table.rows)):  # skip header row 0
        cell = table.rows[row_idx].cells[1]   # feedback column
        # ALWAYS clear existing paragraphs first
        for p in cell.paragraphs:
            p.clear()
        cell.paragraphs[0].text = data.get(f't{table_idx}_r{row_idx}', '')

doc.save('path.docx')
```

## Pitfalls

### Chinese quotation mark syntax errors
- **Problem**: Chinese `""` and `''` chars inside Python strings cause `SyntaxError: invalid character`
- **Fix**: Always route through JSON. Use unicode escapes `\u201c` / `\u201d` / `\u2018` / `\u2019` if needed.

### python-docx cell writing
- **Problem**: Cells retain old content when you just set `cell.text` or `cell.paragraphs[0].text` without clearing first
- **Fix**: Always clear first:
  ```python
  for p in cell.paragraphs:
      p.clear()
  cell.paragraphs[0].text = new_text
  ```

### Word table row indexing
- Row 0 is the header row. Data rows start at index 1.

### Excel file detection
- Use `search_files` with broad patterns (`*副本*`, `*.xlsx`) when exact filenames fail. Desktop files from Chinese systems often have unexpected naming variants.

### openpyxl cell writing
- Straightforward: `ws.cell(row=r, column=c).value = text`
- Merged cells: read with `list(ws.merged_cells.ranges)` before writing

## Workflow for Multi-Form Research Tasks

1. **Search for files** with `search_files` using broad patterns
2. **Read structure** of all documents (table counts, column layouts, merged cells) via `execute_code`
3. **Collect data** via research / delegation if needed
4. **Prepare JSON** per document in `/tmp/` with `write_file`
5. **Fill each document** in separate `execute_code` calls (one per file to keep each call simple and debuggable)
6. **Verify** all saves completed successfully

## Notes

- python-docx: `Document(path)`, access tables by index `doc.tables[i]`
- openpyxl: `load_workbook(path)`, access sheet `wb[sheetname]`
- Always use `encoding='utf-8'` for JSON read/write
- For government/research forms, content should be professional and exhaustively detailed in Chinese
