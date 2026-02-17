import asyncio
import json
import time
from typing import Dict

from .constants import WORK_SEC, SIM_SEC, DEADLINE
from .models import Staff, Event
from .logic import route_team, classify_event

def tnow(start: float) -> float:
    return time.monotonic() - start

def log(start: float, msg: str) -> None:
    print(f"[{tnow(start):6.2f}s] {msg}", flush=True)

async def worker_loop(staff: Staff, queue: asyncio.Queue, start: float, metrics: Dict[str, int]):
    while True:
        ev: Event = await queue.get()
        now = tnow(start)

        deadline = ev.timestamp + DEADLINE[ev.priority]

        # expired if we start after deadline
        if now > deadline:
            metrics["expired"] += 1
            metrics["stress"] += 1
            log(start, f"EXPIRED  #{ev.id} team={staff.team}")
            queue.task_done()
            continue

        staff.status = "Working"
        log(start, f"START    #{ev.id} team={staff.team}")
        await asyncio.sleep(WORK_SEC)
        staff.status = "Idle"

        finished = tnow(start)
        result = classify_event(ev.timestamp, ev.priority, start_ts=now, finish_ts=finished)

        if result == "on_time":
            metrics["handled_on_time"] += 1
            log(start, f"ON-TIME  #{ev.id} team={staff.team}")
        else:  # late
            metrics["delayed_handled"] += 1
            metrics["stress"] += 1
            log(start, f"LATE     #{ev.id} team={staff.team} (deadline={deadline:.2f})")

        queue.task_done()

async def run_sim(path: str, workers_per_team: int = 2):
    events = [Event(**e) for e in json.load(open(path, "r", encoding="utf-8"))]
    events.sort(key=lambda e: e.timestamp)

    start = time.monotonic()
    metrics = {
        "received": 0,
        "invalid": 0,
        "handled_on_time": 0,
        "delayed_handled": 0,
        "expired": 0,
        "leftover": 0,
        "stress": 0,
    }

    queues = {team: asyncio.Queue() for team in ("Security", "Catering", "Waiters")}

    # start worker pool
    for team in queues:
        for _ in range(workers_per_team):
            asyncio.create_task(worker_loop(Staff("Idle", team), queues[team], start, metrics))

    log(start, "Simulation started")

    # ingest events by timestamp
    for ev in events:
        await asyncio.sleep(max(0.0, ev.timestamp - tnow(start)))
        metrics["received"] += 1

        team = route_team(ev.event_type)
        if (team is None) or (ev.priority not in DEADLINE):
            metrics["invalid"] += 1
            log(start, f"INVALID  #{ev.id} type={ev.event_type} prio={ev.priority} -> SKIP")
            continue

        log(start, f"RECEIVED #{ev.id} -> {team}")
        await queues[team].put(ev)

    # run until SIM_SEC
    await asyncio.sleep(max(0.0, SIM_SEC - tnow(start)))

    # wait for already-queued items to be fully accounted for (prevents “in flight” mismatch)
    await asyncio.gather(*(q.join() for q in queues.values()))
    await asyncio.sleep(0)

    # leftovers should be 0 after join, but we count anyway
    leftovers = 0
    for q in queues.values():
        while True:
            try:
                q.get_nowait()
            except asyncio.QueueEmpty:
                break
            else:
                leftovers += 1
                q.task_done()
    metrics["leftover"] = leftovers

    print("\nSUMMARY", flush=True)
    print("received         :", metrics["received"], flush=True)
    print("invalid          :", metrics["invalid"], flush=True)
    print("handled_on_time  :", metrics["handled_on_time"], flush=True)
    print("delayed_handled  :", metrics["delayed_handled"], flush=True)
    print("expired          :", metrics["expired"], flush=True)
    print("leftover         :", metrics["leftover"], flush=True)
    print("stress           :", metrics["stress"], flush=True)

    print("\nCHECK", flush=True)
    valid_received = metrics["received"] - metrics["invalid"]
    total = metrics["handled_on_time"] + metrics["delayed_handled"] + metrics["expired"] + metrics["leftover"]
    print("valid received =", valid_received, flush=True)
    print("on_time + late + expired + leftover =", total, flush=True)

    return metrics

if __name__ == "__main__":
    import sys, asyncio
    path = sys.argv[1] if len(sys.argv) > 1 else "data/events_easy.json"
    asyncio.run(run_sim(path))
