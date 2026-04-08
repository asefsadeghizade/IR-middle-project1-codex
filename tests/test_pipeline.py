from pipeline.main import run_pipeline
from sample_data.ir_samples import ASSIGNMENT_IR, MULTI_TRIGGER_IR, VALIDATION_IR


def test_pipeline_validation_end_to_end():
    results = run_pipeline(VALIDATION_IR)
    assert len(results) == 1
    assert results[0]["behavior"] == "validation"
    assert "Too high" in results[0]["mapped_code"]


def test_pipeline_assignment_end_to_end():
    results = run_pipeline(ASSIGNMENT_IR)
    assert results[0]["behavior"] == "state_update"
    assert results[0]["mapped_code"] == "setBonus(1000);"


def test_pipeline_multiple_triggers_end_to_end():
    results = run_pipeline(MULTI_TRIGGER_IR)
    assert len(results) == 2
    assert results[0]["behavior"] == "validation"
    assert results[1]["behavior"] == "crud"
