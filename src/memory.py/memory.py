"""Algoritmos de substituição de páginas: FIFO, LRU e Optimal."""


def simulate_pages(sequence, frame_count=4, algorithm="FIFO"):
    if frame_count <= 0:
        raise ValueError("A quantidade de frames deve ser positiva.")
    if algorithm not in {"FIFO", "LRU", "Optimal"}:
        raise ValueError("Algoritmo deve ser FIFO, LRU ou Optimal.")

    frames = []
    history = []
    queue_order = []  # ordem de entrada para FIFO
    last_used = {}    # instante da última utilização para LRU
    hits = faults = 0

    for index, page in enumerate(sequence):
        hit = page in frames
        replaced = None
        if hit:
            hits += 1
        else:
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
                queue_order.append(page)
            else:
                if algorithm == "FIFO":
                    victim = queue_order.pop(0)
                elif algorithm == "LRU":
                    victim = min(frames, key=lambda x: last_used.get(x, -1))
                else:
                    future = sequence[index + 1:]
                    distances = {}
                    for resident in frames:
                        distances[resident] = future.index(resident) if resident in future else float("inf")
                    victim = max(frames, key=lambda x: distances[x])
                replaced = victim
                slot = frames.index(victim)
                frames[slot] = page
                if algorithm == "FIFO":
                    queue_order.append(page)
                elif algorithm == "Optimal":
                    # A ordem FIFO não é usada pelo Optimal.
                    pass
        last_used[page] = index
        history.append({
            "reference": page, "frames": frames.copy(),
            "result": "HIT" if hit else "FAULT", "replaced": replaced
        })

    total = len(sequence)
    return {
        "algorithm": algorithm,
        "history": history,
        "hits": hits,
        "faults": faults,
        "references": total,
        "fault_rate": round(faults / total, 4) if total else 0,
        "hit_rate": round(hits / total, 4) if total else 0,
    }


def compare_memory(sequence, frame_count=4):
    return [simulate_pages(sequence, frame_count, alg) for alg in ("FIFO", "LRU", "Optimal")]
