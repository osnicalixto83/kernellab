import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from devices import can_access, simulate_device_requests

def test_alarm_has_audio_execute_permission():
    assert can_access("P4", "audio", "execute")

def test_backup_cannot_use_audio():
    assert not can_access("P5", "audio", "use")

def test_denied_disk_write_is_reported():
    events = simulate_device_requests([{"process":"P4","operation":"write"}], "disco")
    assert any("NEGADO" in event for event in events)


def test_process_can_request_exclusive_disk_access():
    assert can_access("P5", "disco", "request_exclusive")

def test_concurrent_requests_complete():
    events = simulate_device_requests([
        {"process":"P3","operation":"read","duration":0.001},
        {"process":"P5","operation":"write","duration":0.001}
    ], "disco", concurrent=True)
    assert any("concluiu read" in event for event in events)
    assert any("concluiu write" in event for event in events)
