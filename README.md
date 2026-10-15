# KernelLab — Simulador de CPU, Memória e Dispositivos

Projeto acadêmico que simula decisões de um sistema operacional multitarefa no cenário fictício MedControl Systems. Não é um sistema operacional real nem deve controlar equipamentos médicos.

## Requisitos
- Python 3.10 ou superior
- Git (para clonar o repositório)
- Não há dependências externas obrigatórias.

## Executar no Windows (PowerShell)
```powershell
git clone https://github.com/SEU-USUARIO/kernellab.git
cd kernellab
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python src/main.py
```
Se a ativação do ambiente virtual for bloqueada, execute diretamente `py src/main.py` ou use `.\.venv\Scripts\python.exe src\main.py`.

## Executar no Linux/macOS
```bash
git clone https://github.com/SEU-USUARIO/kernellab.git
cd kernellab
python3 -m venv .venv
source .venv/bin/activate
python src/main.py
```
Substitua `SEU-USUARIO` pelo nome de usuário real do GitHub após criar o repositório.

## Testes
Na raiz do projeto:
```bash
python -m unittest discover -s tests -v
```
Os testes verificam finalização dos processos, validação do quantum, métricas, contagem de hits/faults e negação de acesso não autorizado.

## Funcionalidades
- FCFS, SJF não preemptivo, Round Robin (quantum configurável) e Prioridade não preemptiva.
- Diagramas de Gantt em formato textual.
- Espera, turnaround, resposta, utilização da CPU, makespan e estimativa de trocas de contexto.
- Substituição de páginas FIFO, LRU e Optimal; contagem de page hits, page faults e taxa de hits.
- Matriz de permissões por processo e dispositivo.
- Simulação simplificada de contenção de dispositivos e negação de pedidos não autorizados.
- Comparação dos algoritmos impressa no terminal.
- Testes automatizados com `unittest`.

## Estrutura
```text
src/        código-fonte
data/       processos e dados da simulação
tests/      testes automatizados
docs/       recomendação técnica e limitações
results/    reservado para resultados exportados
```

## Dados de entrada
Edite `data/processes.json`. Cada processo possui `pid`, `name`, `arrival`, `burst`, `priority`, `memory_mb` e `device`. Menor valor numérico em `priority` significa prioridade mais alta. A string de referência de páginas e a matriz de acesso também ficam nesse arquivo.

## Interpretação e recomendação
A política de prioridade combina melhor com a importância do alarme crítico, mas esta versão é **não preemptiva**. Para um sistema real de monitoramento, seria necessário escalonamento preemptivo por prioridade, análise de tempo real, envelhecimento para evitar starvation, sincronização real de dispositivos, auditoria e validação de segurança. Veja `docs/recomendacao_tecnica.md`.

## Publicar no GitHub
1. Crie um repositório público chamado `kernellab` no GitHub. Se já existir, use o repositório existente.
2. Descompacte/coloque estes arquivos na pasta local `KernelLab`.
3. Abra o terminal na pasta que contém `README.md` e execute:
```bash
git init
git add .
git status
git commit -m "Entrega inicial do KernelLab"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/kernellab.git
git push -u origin main
```
Se `origin` já existir, não repita `git remote add origin`; confira com `git remote -v` e corrija com `git remote set-url origin https://github.com/SEU-USUARIO/kernellab.git`.
4. Atualize o README substituindo `SEU-USUARIO` pelo usuário correto.
5. No GitHub, confira se `README.md`, `src/`, `data/`, `tests/` e `docs/` aparecem na página principal.
6. Para validar a entrega, clone em outra pasta e siga as instruções de execução e testes acima.
 lINK DO VIDEO https://youtu.be/jB3d0nFGjFI

## Limitações
O projeto é uma simulação didática. Não modela o kernel real, custos de troca de contexto, paginação física, drivers, interrupções, mutexes/semafóros do sistema operacional nem requisitos certificados de tempo real.
