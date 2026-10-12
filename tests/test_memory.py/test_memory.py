import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from memory import simulate_pages

SEQUENCE = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]

def test_total_hits_and_faults_equal_references():
    result = simulate_pages(SEQUENCE, 4, "FIFO")
    assert result["hits"] + result["faults"] == len(SEQUENCE)

def test_optimal_not_worse_than_fifo_for_sample():
    fifo = simulate_pages(SEQUENCE, 4, "FIFO")
    optimal = simulate_pages(SEQUENCE, 4, "Optimal")
    assert optimal["faults"] <= fifo["faults"]

def test_invalid_frame_count():
    try:
        simulate_pages(SEQUENCE, 0, "LRU")
        assert False, "Era esperado ValueError"
    except ValueError:
        pass
