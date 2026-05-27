---
name: security-standard-research
description: Use when researching and filling Chinese government security standard research templates (Word + Excel). Handles docx table filling, xlsx cell writing, parallel web research via delegate_task, and Chinese encoding pitfalls.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, research, china, standard, template, docx, xlsx]
    related_skills: []
---

# Security Standard Research Template Filler

## Overview

Systematically researches and fills Chinese government security standard research templates. The workflow handles: reading template files (`.docx` + `.xlsx`), parallel web research via `delegate_task`, filling Word tables and Excel cells, and saving. Designed for standards like 《智能体应用安全基本要求》where the output is multiple interconnected template files.

## When to Use

- User provides Word (`.docx`) and/or Excel (`.xlsx`) templates that need research-backed content
- The templates follow a question/answer format with tables
- Research topics span multiple domains (products, standards, regulations, technologies)
- Content must be written in Chinese
- Multiple files need to be filled in a coordinated manner

Don't use for: single-file research tasks, English-only content, non-template documents.

## Workflow

### Phase 1: Discovery

1. Search for all template files on the user's desktop or specified directory:
   ```python
   search_files(pattern='*keyword*', path='~/Desktop', target='files')
   search_files(pattern='*.docx', path='~/Desktop', target='files')
   search_files(pattern='*.xlsx', path='~/Desktop', target='files')
   ```

2. Verify Python dependencies:
   ```python
   import importlib
   for pkg in ['openpyxl', 'docx']:
       importlib.import_module(pkg)
   ```

3. Read and inventory all templates — understand the structure:
   - Word: number of tables, rows per table, question/fill-in columns
   - Excel: sheets, headers, merged cell ranges, rows that need data

### Phase 2: Research

Launch parallel `delegate_task` for independent research topics. Batch by domain:

```python
delegate_task(tasks=[
  {"goal":"Research mainstream AI Agent products: names, deployment, tools, commercial status. Return detailed Chinese summary.",
   "context":"User is filling a Chinese government security standard template. Focus on: OpenAI, Anthropic, Google, Meta, Microsoft, Baidu, Alibaba, ByteDance, Zhipu, DeepSeek. Include: commercial status, open-source status, deployment mode, tool calling methods, target industries.",
   "toolsets":["web"]},
  {"goal":"Research global AI/Agent security standards and frameworks.",
   "context":"Chinese language output. Cover: OWASP LLM Top 10, MITRE ATLAS, NIST AI RMF, ISO 42001, China's 生成式人工智能管理办法, 等保2.0, EU AI Act, Singapore AI Verify.",
   "toolsets":["web"]},
  ...
])
```

Key principle: **batch independent topics** in one `delegate_task` call (up to `delegation.max_concurrent_children`). Specify `"toolsets":["web"]` for web-only research.

### Phase 3: Fill Word Documents

**Critical rules for python-docx:**

1. Table row indexing starts at 1 (row 0 is header).
2. **Always clear existing paragraphs** before writing:
   ```python
   cell = table.rows[row_idx].cells[col_idx]
   for p in cell.paragraphs:
       p.clear()
   cell.paragraphs[0].text = content
   ```
3. **NEVER embed long Chinese strings directly in Python code.** Chinese quotation marks (「」『』""''）and special punctuations cause `SyntaxError`. Instead:
   - Write data to JSON file first: `write_file(path, json.dumps(data))`
   - Read JSON in execute_code: `json.load(open(path))`
   - Then fill cells from the parsed dict

4. Pattern for multi-table docx:
   ```python
   from docx import Document
   import json
   
   with open('/tmp/data.json', 'r', encoding='utf-8') as f:
       data = json.load(f)
   
   doc = Document(template_path)
   
   # Table 0
   t0 = doc.tables[0]
   for row_idx, text in data["T0"].items():
       cell = t0.rows[int(row_idx)].cells[1]
       for p in cell.paragraphs: p.clear()
       cell.paragraphs[0].text = text
   
   doc.save(template_path)
   ```

### Phase 4: Fill Excel Workbook

**Critical rules for openpyxl:**

1. Check actual file names — they may differ from expectations. Always `search_files` first.
2. Be aware of merged cell ranges: `list(ws.merged_cells.ranges)`.
3. Write large content via JSON to avoid encoding issues — same pattern as Word.
4. Write directly to cells:
   ```python
   from openpyxl import load_workbook
   import json
   
   with open('/tmp/xlsx_data.json', 'r', encoding='utf-8') as f:
       data = json.load(f)
   
   wb = load_workbook(path)
   ws = wb.active  # or wb[sheet_name]
   
   for row_str, text in data.items():
       ws.cell(row=int(row_str), column=3).value = text
   
   wb.save(path)
   ```

### Phase 5: Verify

After all fills, verify each file:
```python
import os
from docx import Document
from openpyxl import load_workbook

for fname in file_list:
    path = os.path.join(desktop, fname)
    size_kb = os.path.getsize(path) / 1024
    if fname.endswith('.docx'):
        doc = Document(path)
        filled = sum(1 for t in doc.tables for r in t.rows[1:] 
                     for c in r.cells if c.text.strip())
        print(f"{fname}: {size_kb:.1f}KB, {filled} filled cells")
    else:
        wb = load_workbook(path)
        ws = wb.active
        filled = sum(1 for row in ws.iter_rows(min_row=3, max_col=3) 
                     for c in row if c.value)
        print(f"{fname}: {size_kb:.1f}KB, {filled} filled rows")
```

## Common Pitfalls

1. **Chinese punctuation in Python strings:** `"` `"` `'` `'` `，` `：` inside Python `"..."` strings break parsing. **Always use JSON file as intermediate format.**

2. **Word table cell won't update:** You MUST `for p in cell.paragraphs: p.clear()` before setting `p.text`. Simply assigning to `cell.text` doesn't reliably work.

3. **Excel file not found:** Template file names from the brief may not match actual desktop files. Always `search_files` to discover the real names.

4. **execute_code timeout for large scripts:** When filling many cells, split into multiple `execute_code` calls (one per file, or one per JSON data write + one per fill).

5. **delegate_task returning too little data:** Research tasks that return <2000 chars likely didn't search enough. Rephrase the goal with more specific sub-questions and add more context.

6. **Merged cells in Excel:** Writing to a merged cell's secondary cells has no effect. Write only to the top-left cell of the merged range.

7. **Long text in single Word cell:** python-docx handles this fine — just assign the full text to `paragraphs[0].text`. No need to split across multiple paragraphs.

## Verification Checklist

- [ ] All template files found and paths confirmed
- [ ] All research data collected before starting fills
- [ ] JSON intermediate files used for all Chinese content
- [ ] Word cells cleared before writing (`p.clear()`)
- [ ] Excel file saved with `wb.save(path)` after all writes
- [ ] Each file verified: file size increased, cells contain content
- [ ] Output files are at the expected paths on the user's system
