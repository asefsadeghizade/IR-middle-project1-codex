# Oracle Forms IR MVP Pipeline

This project provides a modular MVP pipeline for transforming Oracle Forms IR trigger code into modern mapped outputs.

## Phases

1. **Phase 2 – PL/SQL Parser** (`parser/plsql_parser.py`)
2. **Phase 3 – Behavior Classification** (`classifier/behavior_classifier.py`)
3. **Phase 4 – Pattern Mapping** (`mapper/pattern_mapper.py`)
4. **Integration Pipeline** (`pipeline/main.py`)

## Project structure

```text
project/
  parser/
  classifier/
  mapper/
  pipeline/
  models/
  tests/
```

## Run tests

```bash
python -m pytest -q
```

## Example usage

```python
from pipeline.main import run_pipeline
from sample_data.ir_samples import VALIDATION_IR

results = run_pipeline(VALIDATION_IR)
print(results)
```

## Sample IR inputs

See `sample_data/ir_samples.py` for:
- Validation example
- Assignment example
- Multiple triggers
- Mixed logic example
