# KernelLab — Simulador de Sistemas Operacionais

## 1. Problema e objetivo
O KernelLab é um simulador acadêmico que reproduz decisões de gerenciamento de CPU, memória e dispositivos em um cenário fictício de monitoramento de equipamentos médicos da MedControl Systems. Não é um sistema operacional real e não controla equipamentos médicos.

## 2. Arquitetura
- `src/main.py`: menu e integração.
- `src/schedulers.py`: FCFS, SJF não preemptivo, Round Robin e Prioridade preemptiva.
- `src/metrics.py`: métricas, diagramas de Gantt em texto e gráficos.
- `src/memory.py`: FIFO, LRU e Optimal.
- `src/devices.py`: matriz de permissões e fila de acesso.
- `data/processes.json`: parâmetros editáveis dos seis processos.
- `tests/`: testes automatizados.

## 3. Requisitos
Python 3.10 ou superior recomendado.

## 4. Instalação e execução
No terminal, na pasta raiz do projeto:

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:
```bat
.venv\Scripts\activate.bat
```

Instale dependências:
```bash
python -m pip install -r requirements.txt
```

Execute:
```bash
python src/main.py
```

Rode os testes:
```bash
python -m pytest
```

## 5. Formato de entrada
Edite `data/processes.json`. Cada processo contém:
- `id`: identificador único;
- `name`: descrição;
- `arrival`: instante de chegada;
- `burst`: duração de CPU;
- `priority`: número menor significa prioridade maior;
- `memory_mb`: memória solicitada, em MB;
- `devices`: lista de dispositivos associados.

O campo `quantum` altera o quantum do Round Robin sem modificar a lógica dos algoritmos. A seção `memory` contém `sequence` (sequência de referências) e `frame_count` (quantidade de frames), também configuráveis no JSON.

## 6. Métricas e convenções
- Espera = retorno − burst.
- Retorno = conclusão − chegada.
- Resposta = primeira execução − chegada.
- Trocas de contexto contam mudanças entre processos consecutivos, sem contar entrada/saída do estado ocioso.
- SJF é não preemptivo; Prioridade é preemptiva.
- A contagem de trocas considera segmentos consecutivos no timeline. O escalonador por prioridade junta unidades adjacentes do mesmo processo.

## 7. Memória
A sequência inicial é `[1,2,3,4,1,2,5,1,2,3,4,5,2,1,5,3,2]`, com quatro frames. FIFO remove a página mais antiga; LRU remove a menos recentemente usada; Optimal remove a página cujo próximo uso está mais distante (ou que não será usada novamente).

## 8. Dispositivos e segurança
A matriz é uma política ilustrativa para a atividade, não uma política de segurança validada para produção. A fila de demonstração pode iniciar solicitações em threads concorrentes. Um `threading.Lock` protege o uso do dispositivo para que somente uma thread entre na seção crítica por vez. A matriz contém permissões distintas para leitura, gravação, execução, uso e solicitação de exclusividade.

## 9. Resultados e limitações
O programa imprime métricas e gera gráficos PNG na pasta `docs/`. Os resultados dependem dos dados configurados. O simulador não modela interrupções reais, I/O bloqueante dentro do escalonamento de CPU, paginação integrada com memória dos processos, deadlocks, prioridade herdada ou prazos de tempo real. A política de prioridade preemptiva é uma simplificação acadêmica e não equivale a um escalonador de tempo real certificado.

## 10. Melhorias futuras
- Interface web;
- exportação CSV;
- políticas de aging para reduzir starvation;
- simulação integrada de I/O bloqueante;
- testes concorrentes com threads;
- escalonamento de tempo real com deadlines;
- relatório PDF automatizado.

## 11. Referências
- TANENBAUM, Andrew S.; BOS, Herbert. *Sistemas Operacionais Modernos*.
- Materiais da disciplina Sistemas Operacionais disponibilizados no AVA.
- Tecnoblog. “O que é um sistema operacional?”. https://tecnoblog.net/responde/o-que-e-um-sistema-operacional/
- Material de sistemas multiprogramados indicado no enunciado da atividade.
- Material INF 1316: Sistemas Operacionais indicado no enunciado da atividade.

## 12. Vídeo de apresentação
Adicionar aqui o link público ou não listado do vídeo após a gravação: **[INSERIR LINK DO VÍDEO]**
