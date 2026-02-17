import pytest
from marry_me.logic import classify_event

def test_expired_started_after_deadline():
    # high deadline = 2 + 5 = 7
    assert classify_event(arrival_ts=2.0, priority="high", start_ts=7.01, finish_ts=10.01) == "expired"

def test_on_time_finished_by_deadline():
    # medium deadline = 3 + 10 = 13
    assert classify_event(arrival_ts=3.0, priority="medium", start_ts=5.0, finish_ts=13.0) == "on_time"

def test_late_finished_after_deadline():
    # low deadline = 4 + 15 = 19
    assert classify_event(arrival_ts=4.0, priority="low", start_ts=18.0, finish_ts=19.01) == "late"

def test_bad_priority_raises():
    with pytest.raises(ValueError):
        classify_event(arrival_ts=0.0, priority="urgent", start_ts=0.0, finish_ts=1.0)
