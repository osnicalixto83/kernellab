import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from schedulers import fcfs, sjf, round_robin, priority_preemptive

SAMPLE = [
    {"id":"A","arrival":0,"burst":3,"priority":1},
    {"id":"B","arrival":1,"burst":2,"priority":0},
]

def test_fcfs_completes_all_processes():
    result = fcfs(SAMPLE)
    assert len(result["processes"]) == 2
    assert all(p["completion"] is not None for p in result["processes"])

def test_sjf_runs_shortest_ready_job_after_first():
    result = sjf(SAMPLE)
    assert result["timeline"][0]["process"] == "A"
    assert result["timeline"][1]["process"] == "B"

def test_round_robin_rejects_invalid_quantum():
    try:
        round_robin(SAMPLE, 0)
        assert False, "Era esperado ValueError"
    except ValueError:
        pass

def test_priority_can_preempt():
    result = priority_preemptive(SAMPLE)
    assert result["timeline"][0]["process"] == "A"
    assert result["timeline"][1]["process"] == "B"
    assert result["processes"][1]["response"] == 0
