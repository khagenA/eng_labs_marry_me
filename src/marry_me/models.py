from dataclasses import dataclass

@dataclass
class Staff:
    status: str  # "Idle" | "Working"
    team: str

@dataclass(frozen=True)
class Event:
    id: int
    event_type: str
    priority: str
    description: str
    timestamp: float
