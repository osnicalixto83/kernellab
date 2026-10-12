"""Algoritmos de escalonamento de CPU do KernelLab.

Convenções:
- arrival: instante de chegada
- burst: duração total de CPU
- priority: menor número significa maior prioridade
- tempos são unidades abstratas de tempo
"""

from copy import deepcopy


def _prepare(processes):
    """Valida e copia os processos, sem modificar os dados de entrada."""
    required = {"id", "arrival", "burst", "priority"}
    prepared = []
    seen = set()
    for original in processes:
        missing = required - original.keys()
        if missing:
            raise ValueError(f"Processo sem campos obrigatórios: {sorted(missing)}")
        p = deepcopy(original)
        if p["id"] in seen:
            raise ValueError(f"ID de processo duplicado: {p['id']}")
        seen.add(p["id"])
        if p["arrival"] < 0 or p["burst"] <= 0:
            raise ValueError(f"Chegada deve ser >= 0 e burst > 0: {p['id']}")
        p["remaining"] = p["burst"]
        p["first_start"] = None
        p["completion"] = None
        prepared.append(p)
    return sorted(prepared, key=lambda p: (p["arrival"], p["id"]))


def _record_run(p, start, end, timeline):
    if p["first_start"] is None:
        p["first_start"] = start
    timeline.append({"process": p["id"], "start": start, "end": end})


def _finish_result(processes, timeline, algorithm):
    by_id = {p["id"]: p for p in processes}
    rows = []
    for p in processes:
        completion = p["completion"]
        turnaround = completion - p["arrival"]
        waiting = turnaround - p["burst"]
        response = p["first_start"] - p["arrival"]
        rows.append({
            "id": p["id"], "name": p.get("name", p["id"]),
            "arrival": p["arrival"], "burst": p["burst"],
            "priority": p["priority"], "first_start": p["first_start"],
            "completion": completion, "waiting": waiting,
            "turnaround": turnaround, "response": response
        })
    # Troca de contexto: mudança de um processo para outro. Intervalos ociosos
    # não contam como troca entre processos.
    switches = sum(
        1 for a, b in zip(timeline, timeline[1:])
        if a["process"] != "IDLE" and b["process"] != "IDLE"
        and a["process"] != b["process"]
    )
    return {
        "algorithm": algorithm,
        "timeline": timeline,
        "processes": rows,
        "context_switches": switches,
        "averages": {
            key: round(sum(row[key] for row in rows) / len(rows), 3) if rows else 0
            for key in ("waiting", "turnaround", "response")
        }
    }


def fcfs(processes):
    """FCFS não preemptivo: executa na ordem de chegada."""
    ps = _prepare(processes)
    timeline, time = [], 0
    for p in ps:
        if time < p["arrival"]:
            timeline.append({"process": "IDLE", "start": time, "end": p["arrival"]})
            time = p["arrival"]
        start = time
        time += p["burst"]
        _record_run(p, start, time, timeline)
        p["completion"] = time
    return _finish_result(ps, timeline, "FCFS")


def sjf(processes):
    """SJF não preemptivo: entre os prontos, escolhe o menor burst."""
    ps = _prepare(processes)
    pending = ps[:]
    timeline, time = [], 0
    while pending:
        ready = [p for p in pending if p["arrival"] <= time]
        if not ready:
            next_arrival = min(p["arrival"] for p in pending)
            timeline.append({"process": "IDLE", "start": time, "end": next_arrival})
            time = next_arrival
            continue
        p = min(ready, key=lambda x: (x["burst"], x["arrival"], x["id"]))
        pending.remove(p)
        start = time
        time += p["burst"]
        _record_run(p, start, time, timeline)
        p["completion"] = time
    return _finish_result(ps, timeline, "SJF")


def round_robin(processes, quantum=3):
    """Round Robin preemptivo com fila FIFO e quantum configurável."""
    if not isinstance(quantum, int) or quantum <= 0:
        raise ValueError("O quantum deve ser um inteiro positivo.")
    ps = _prepare(processes)
    by_id = {p["id"]: p for p in ps}
    pending_index = 0
    ready = []
    timeline, time = [], 0
    while pending_index < len(ps) or ready:
        while pending_index < len(ps) and ps[pending_index]["arrival"] <= time:
            ready.append(ps[pending_index])
            pending_index += 1
        if not ready:
            next_arrival = ps[pending_index]["arrival"]
            timeline.append({"process": "IDLE", "start": time, "end": next_arrival})
            time = next_arrival
            continue
        p = ready.pop(0)
        start = time
        duration = min(quantum, p["remaining"])
        end = time + duration
        _record_run(p, start, end, timeline)
        p["remaining"] -= duration
        time = end
        # Processos que chegaram durante o intervalo entram antes de recolocar
        # o processo que ainda não terminou.
        while pending_index < len(ps) and ps[pending_index]["arrival"] <= time:
            ready.append(ps[pending_index])
            pending_index += 1
        if p["remaining"] > 0:
            ready.append(p)
        else:
            p["completion"] = time
    return _finish_result(ps, timeline, f"Round Robin (q={quantum})")


def priority_preemptive(processes):
    """Prioridade preemptiva: reavalia a cada unidade de tempo."""
    ps = _prepare(processes)
    timeline, time = [], 0
    remaining = {p["id"]: p["burst"] for p in ps}
    first_start = {p["id"]: None for p in ps}
    completion = {}
    pending = {p["id"]: p for p in ps}
    last_process = None
    while len(completion) < len(ps):
        ready = [p for p in ps if p["arrival"] <= time and remaining[p["id"]] > 0]
        if not ready:
            future = [p["arrival"] for p in ps if remaining[p["id"]] > 0 and p["arrival"] > time]
            if not future:
                break
            next_time = min(future)
            timeline.append({"process": "IDLE", "start": time, "end": next_time})
            time = next_time
            last_process = None
            continue
        p = min(ready, key=lambda x: (x["priority"], x["arrival"], x["id"]))
        pid = p["id"]
        if first_start[pid] is None:
            first_start[pid] = time
        # Junta unidades adjacentes do mesmo processo no diagrama.
        if timeline and timeline[-1]["process"] == pid and timeline[-1]["end"] == time:
            timeline[-1]["end"] += 1
        else:
            timeline.append({"process": pid, "start": time, "end": time + 1})
        remaining[pid] -= 1
        time += 1
        if remaining[pid] == 0:
            completion[pid] = time
    for p in ps:
        p["first_start"] = first_start[p["id"]]
        p["completion"] = completion[p["id"]]
    return _finish_result(ps, timeline, "Prioridade preemptiva")


def run_all_schedulers(processes, quantum=3):
    """Executa todos os escalonadores para facilitar a comparação."""
    return [
        fcfs(processes),
        sjf(processes),
        round_robin(processes, quantum),
        priority_preemptive(processes),
    ]
