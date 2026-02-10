import random
import json
import sys

# Define event types and their respective teams (3 teams, 2 workers each)
teams = {
    'Security': ['brawl', 'not_on_list'],
    'Catering': ['bad_food', 'feeling_ill'],
    'Waiters':  ['dirty_table', 'broken_item'],
}

# All valid event types (flat list)
all_event_types = [et for types in teams.values() for et in types]

# Priority deadline mapping (seconds from event timestamp)
priority_deadlines = {
    'high':   5,
    'medium': 10,
    'low':    15,
}

# Descriptions per event type
descriptions = {
    'brawl': [
        "A brawl broke out near the bar area",
        "Guests shoving each other on the dance floor",
        "Two guests arguing loudly at table 7",
        "Fight between guests over seating arrangement",
    ],
    'not_on_list': [
        "Unknown person trying to enter the venue",
        "Guest not found on the invitation list",
        "Someone claiming to be a plus-one but not on the list",
        "Uninvited guest causing confusion at the entrance",
    ],
    'bad_food': [
        "Guests complaining about cold soup",
        "Undercooked chicken served at table 3",
        "Guest found a hair in their salad",
        "Overly salty appetizers at the cocktail hour",
        "Missing vegan option for guests at table 9",
    ],
    'feeling_ill': [
        "Guest feeling faint after dancing too long",
        "Guest feeling nauseous after eating too much cake",
        "Guest allergic reaction to flower pollen",
        "Guest feeling dizzy due to the heat",
        "Guest with stomach ache after the appetizers",
    ],
    'dirty_table': [
        "Dirty dishes piling up at table 5",
        "Spilled wine all over table 12",
        "Flower arrangement knocked over at table 2",
        "Coffee stain on the rental linens at table 8",
        "Dirty napkins left after dessert service",
    ],
    'broken_item': [
        "Broken glass found near the bar counter",
        "Broken chair at table 4",
        "Broken vase near the entrance",
        "Broken microphone during the toast",
        "Broken decoration piece on the gift table",
    ],
}


def generate_event(event_id, timestamp):
    """Generate a single random event at the given timestamp."""
    event_type = random.choice(all_event_types)
    priority = random.choice(list(priority_deadlines.keys()))
    description = random.choice(descriptions[event_type])

    return {
        'id': event_id,
        'event_type': event_type,
        'priority': priority,
        'description': description,
        'timestamp': round(timestamp, 1),
    }


def generate_dataset(num_events, seed=None):
    """Generate a dataset of events spread across a 60-second simulation."""
    if seed is not None:
        random.seed(seed)

    # Generate sorted random timestamps in [0.0, 55.0]
    # (cap at 55 so even low-priority events have a chance to expire within 60s)
    timestamps = sorted(round(random.uniform(0.0, 55.0), 1) for _ in range(num_events))

    dataset = []
    for i, ts in enumerate(timestamps, start=1):
        dataset.append(generate_event(i, ts))

    return dataset


# --- Difficulty presets ---
# With 3 teams × 2 workers, each event taking 3s to handle:
#   max throughput ≈ 2 events/second when all workers are idle
PRESETS = {
    'easy':   15,   # light load, most events should be handled
    'medium': 30,   # moderate pressure
    'hard':   60,   # significant queuing and expiration expected
}

if __name__ == '__main__':
    preset = sys.argv[1] if len(sys.argv) > 1 else 'medium'
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if preset.isdigit():
        num_events = int(preset)
    elif preset in PRESETS:
        num_events = PRESETS[preset]
    else:
        print(f"Usage: {sys.argv[0]} [easy|medium|hard|<number>] [seed]")
        print(f"  Presets: {PRESETS}")
        sys.exit(1)

    dataset = generate_dataset(num_events, seed=seed)
    filename = f"events_{preset}.json"

    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"Generated {len(dataset)} events -> {filename}")
    print(f"Simulation window: 60 seconds")
    print(f"Teams: {list(teams.keys())} (2 workers each)")
    print()
    for event in dataset:
        print(f"  [{event['timestamp']:5.1f}s] #{event['id']:>3d}  {event['priority']:<6s}  {event['event_type']:<13s}  {event['description']}")
