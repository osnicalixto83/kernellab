"""Ponto de entrada do KernelLab. Execute com: python src/main.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from schedulers import run_all_schedulers
from memory import compare_memory
from devices import ACCESS_MATRIX, simulate_device_requests
from metrics import print_scheduler_result, print_memory_result, plot_scheduler_comparison, plot_memory_comparison


DEFAULT_SEQUENCE = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5, 2, 1, 5, 3, 2]


def load_config():
    with (ROOT / "data" / "processes.json").open(encoding="utf-8") as file:
        return json.load(file)


def show_cpu(config):
    results = run_all_schedulers(config["processes"], config.get("quantum", 3))
    for result in results:
        print_scheduler_result(result)
    try:
        path = plot_scheduler_comparison(results, str(ROOT / "docs" / "comparacao_cpu.png"))
        print(f"\nGráfico de CPU salvo em: {path}")
    except (RuntimeError, ImportError) as exc:
        print(f"Gráfico não gerado: {exc}")
    best_wait = min(results, key=lambda r: r["averages"]["waiting"])
    best_response = min(results, key=lambda r: r["averages"]["response"])
    print("\n=== Resumo da CPU ===")
    print(f"Menor espera média: {best_wait['algorithm']} ({best_wait['averages']['waiting']})")
    print(f"Menor resposta média: {best_response['algorithm']} ({best_response['averages']['response']})")
    print("Atenção: menor média não significa automaticamente maior justiça ou melhor segurança.")


def show_memory(config):
    memory_config = config.get("memory", {})
    sequence = memory_config.get("sequence", DEFAULT_SEQUENCE)
    frame_count = memory_config.get("frame_count", 4)
    results = compare_memory(sequence, frame_count=frame_count)
    for result in results:
        print_memory_result(result)
    try:
        path = plot_memory_comparison(results, str(ROOT / "docs" / "comparacao_memoria.png"))
        print(f"\nGráfico de memória salvo em: {path}")
    except ImportError:
        print("Matplotlib não instalado; gráfico não gerado.")


def show_devices():
    print("\n=== Matriz de acesso ===")
    print("Processo | Disco | Rede | Áudio | Logs")
    for pid, permissions in ACCESS_MATRIX.items():
        print(f'{pid:>8} | {permissions["disco"]:>5} | {permissions["rede"]:>4} | {permissions["audio"]:>5} | {permissions["logs"]:>4}')
    requests = [
        {"process": "P3", "operation": "read", "duration": 0},
        {"process": "P5", "operation": "write", "duration": 0},
        {"process": "P4", "operation": "write", "duration": 0},
    ]
    print("\n=== Fila de solicitações ao disco ===")
    for event in simulate_device_requests(requests, "disco", concurrent=True):
        print("-", event)


def main():
    config = load_config()
    while True:
        print("\n========== KernelLab ==========")
        print("1 - Executar escalonadores de CPU")
        print("2 - Executar algoritmos de memória")
        print("3 - Demonstrar dispositivos e permissões")
        print("4 - Executar tudo")
        print("0 - Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            show_cpu(config)
        elif choice == "2":
            show_memory(config)
        elif choice == "3":
            show_devices()
        elif choice == "4":
            show_cpu(config)
            show_memory(config)
            show_devices()
        elif choice == "0":
            print("Encerrando o KernelLab.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
