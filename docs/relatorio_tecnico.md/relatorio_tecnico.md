# Relatório Técnico — KernelLab

## 1. Contextualização
A MedControl Systems é um cenário fictício que reúne monitoramento cardíaco, transmissão de telemetria, geração de relatórios, alarmes, backups e atualização de dados. Esses trabalhos disputam CPU, memória e dispositivos. A simulação permite comparar políticas de alocação e discutir os compromissos entre eficiência, prioridade e justiça.

## 2. Estados e ciclo de vida dos processos
Um processo pode estar novo, pronto, executando, bloqueado/em espera por I/O ou terminado. O escalonador escolhe entre processos prontos. Nesta versão, os algoritmos de CPU modelam chegada e execução em CPU; a fila de dispositivos é demonstrada separadamente, sem bloquear e reativar os processos no timeline da CPU.

## 3. Escalonamento da CPU
- **FCFS:** atende por ordem de chegada. É simples e previsível, mas um trabalho longo pode atrasar tarefas curtas.
- **SJF:** escolhe o menor burst entre os processos prontos. Pode reduzir espera média, mas depende de conhecer a duração e pode atrasar tarefas longas.
- **Round Robin:** divide CPU em fatias de tamanho quantum. Melhora a oportunidade de resposta e a justiça, mas quanta pequenos aumentam trocas de contexto.
- **Prioridade:** escolhe o menor valor numérico de prioridade. A versão implementada é preemptiva e pode atrasar processos de baixa prioridade sem aging ou limite de espera.

## 4. Métricas
- Espera = tempo de retorno menos burst.
- Retorno = conclusão menos chegada.
- Resposta = primeira execução menos chegada.
- Troca de contexto: mudança entre processos diferentes em segmentos consecutivos.
Os números são unidades abstratas de tempo, não milissegundos de um equipamento real.

## 5. Memória virtual e substituição de páginas
A memória virtual permite que processos usem um espaço de endereçamento maior que a memória física disponível, trazendo páginas conforme necessário. Uma falta de página ocorre quando a referência não está nos frames simulados.
- **FIFO:** substitui a página que está há mais tempo na memória.
- **LRU:** substitui a página usada há mais tempo no passado.
- **Optimal:** substitui a página cujo próximo uso ocorrerá mais distante no futuro; é uma referência teórica, pois requer conhecimento das referências futuras.
A taxa de faltas é `page faults / total de referências`.

## 6. Concorrência, mutex e semáforos
Quando processos disputam um dispositivo compartilhado, operações simultâneas podem gerar inconsistência. Um mutex/lock protege a seção crítica e permite que apenas um solicitante utilize o dispositivo por vez. Um semáforo também pode limitar a quantidade de acessos concorrentes. A demonstração utiliza threads concorrentes, `threading.Lock` e uma fila simplificada. A matriz diferencia leitura, gravação, execução, uso e autorização para solicitar acesso exclusivo.

## 7. Segurança no acesso a dispositivos
A matriz associa cada processo a permissões de leitura, gravação, execução e uso. O princípio de menor privilégio recomenda conceder apenas as permissões necessárias. A matriz deste projeto é didática e precisaria de análise de ameaças, autenticação, auditoria e validação antes de qualquer uso real.

## 8. Relação com a MedControl
O processo P4 representa o alarme crítico e recebe prioridade 0. A política de prioridade favorece esse processo, mas não garante prazo máximo de resposta. Para um sistema crítico, seria necessário especificar deadlines, comportamento sob sobrecarga, preempção, inversão de prioridade, falhas e mecanismos de segurança. Round Robin oferece compartilhamento mais regular, enquanto prioridade atende melhor à criticidade. Uma política híbrida com prioridades, limites de execução e aging pode ser uma proposta futura, mas precisa ser avaliada por testes.

## 9. Resultados
Executar `python src/main.py` para obter diagramas de Gantt, métricas médias, trocas de contexto, page hits/faults e gráficos. Inserir nesta seção capturas ou tabelas geradas na execução final. Não registrar valores não verificados.

## 10. Limitações
O simulador não é um sistema operacional, não integra I/O bloqueante ao escalonamento de CPU e não simula memória física por processo. O escalonamento por prioridade não possui aging. A contagem de trocas de contexto segue a convenção documentada no README.

## 11. Referências
- TANENBAUM, Andrew S.; BOS, Herbert. *Sistemas Operacionais Modernos*.
- Materiais da disciplina Sistemas Operacionais disponibilizados no AVA.
- Tecnoblog. “O que é um sistema operacional?”. https://tecnoblog.net/responde/o-que-e-um-sistema-operacional/
- Artigos e materiais indicados no enunciado da atividade.
