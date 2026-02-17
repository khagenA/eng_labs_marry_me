from .constants import DEADLINE, TYPE_TO_TEAM

def route_team(event_type: str):
    """Return team name for event_type, else None."""
    return TYPE_TO_TEAM.get(event_type)

def classify_event(arrival_ts: float, priority: str, start_ts: float, finish_ts: float) -> str:
    """
    Returns: 'expired', 'on_time', 'late'
    - expired : started after deadline
    - on_time : finished by deadline
    - late    : started before deadline but finished after
    """
    if priority not in DEADLINE:
        raise ValueError(f"Unknown priority: {priority}")

    deadline = arrival_ts + DEADLINE[priority]
    if start_ts > deadline:
        return "expired"
    if finish_ts <= deadline:
        return "on_time"
    return "late"
