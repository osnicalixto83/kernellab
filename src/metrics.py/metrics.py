"""Funções de apresentação, métricas e gráficos do KernelLab."""


def gantt_text(result):
    parts = []
    for item in result["timeline"]:
        parts.append(f'{item["process"]}[{item["start"]}-{item["end"]}]')
    return " | ".join(parts)


def print_scheduler_result(result):
    print(f"\n=== {result['algorithm']} ===")
    print("Diagrama de Gantt:")
    print(gantt_text(result))
    print("\nProcesso | Espera | Retorno | Resposta")
    for p in result["processes"]:
        print(f'{p["id"]:>8} | {p["waiting"]:>6} | {p["turnaround"]:>7} | {p["response"]:>8}')
    print("Médias:", result["averages"])
    print("Trocas de contexto:", result["context_switches"])


def print_memory_result(result):
    print(f'\n=== Memória: {result["algorithm"]} ===')
    print("Ref. | Frames | Resultado | Substituída")
    for row in result["history"]:
        print(f'{row["reference"]:>4} | {str(row["frames"]):<18} | {row["result"]:<7} | {row["replaced"]}')
    print(f'Hits: {result["hits"]} | Faults: {result["faults"]} | Taxa de faltas: {result["fault_rate"]:.1%}')


def plot_scheduler_comparison(results, output_path="docs/comparacao_cpu.png"):
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Instale as dependências com: pip install -r requirements.txt") from exc
    names = [r["algorithm"] for r in results]
    metrics = ("waiting", "turnaround", "response")
    labels = ("Espera média", "Retorno médio", "Resposta média")
    x = list(range(len(names)))
    width = 0.25
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (metric, label) in enumerate(zip(metrics, labels)):
        values = [r["averages"][metric] for r in results]
        positions = [v + (i - 1) * width for v in x]
        ax.bar(positions, values, width, label=label)
    ax.set_xticks(x, names, rotation=12)
    ax.set_ylabel("Unidades de tempo")
    ax.set_title("Comparação dos escalonadores")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_memory_comparison(results, output_path="docs/comparacao_memoria.png"):
    import matplotlib.pyplot as plt
    names = [r["algorithm"] for r in results]
    faults = [r["faults"] for r in results]
    hits = [r["hits"] for r in results]
    fig, ax = plt.subplots(figsize=(7, 4))
    x = list(range(len(names)))
    ax.bar([v - 0.18 for v in x], faults, 0.36, label="Page faults")
    ax.bar([v + 0.18 for v in x], hits, 0.36, label="Page hits")
    ax.set_xticks(x, names)
    ax.set_ylabel("Quantidade")
    ax.set_title("Comparação de substituição de páginas")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path
