"""Controle de acesso e fila concorrente para dispositivos compartilhados."""
from collections import deque
from threading import Lock, Thread
from time import sleep

DEVICES = ("disco", "rede", "audio", "logs")

# Cada dispositivo tem permissões explícitas:
# r = leitura, w = gravação, x = execução, u = uso, e = pode pedir acesso exclusivo.
ACCESS_MATRIX = {
    "P1": {"disco": "ru",  "rede": "rwu", "audio": "-",   "logs": "wu"},
    "P2": {"disco": "-",   "rede": "rwu", "audio": "-",   "logs": "wu"},
    "P3": {"disco": "rwue","rede": "-",   "audio": "-",   "logs": "wu"},
    "P4": {"disco": "-",   "rede": "rwu", "audio": "xue", "logs": "wu"},
    "P5": {"disco": "rwue","rede": "-",   "audio": "-",   "logs": "wu"},
    "P6": {"disco": "rwue","rede": "rwu", "audio": "-",   "logs": "wu"},
}

OPERATION_PERMISSION = {
    "read": "r",
    "write": "w",
    "execute": "x",
    "use": "u",
    "request_exclusive": "e",
}


def can_access(process_id, device, operation):
    """Valida se o processo possui a permissão solicitada."""
    if device not in DEVICES or process_id not in ACCESS_MATRIX:
        return False
    if operation not in OPERATION_PERMISSION:
        return False
    return OPERATION_PERMISSION[operation] in ACCESS_MATRIX[process_id].get(device, "-")


def access_matrix_rows():
    """Devolve as permissões em formato fácil de apresentar."""
    return [{"process": pid, **permissions} for pid, permissions in ACCESS_MATRIX.items()]


class DeviceQueue:
    """Fila compartilhada e exclusão mútua para simular um dispositivo."""
    def __init__(self, device_name):
        if device_name not in DEVICES:
            raise ValueError(f"Dispositivo desconhecido: {device_name}")
        self.device_name = device_name
        self.queue = deque()
        self.queue_lock = Lock()
        self.device_lock = Lock()
        self.events = []
        self._event_lock = Lock()

    def _log(self, message):
        with self._event_lock:
            self.events.append(message)

    def request(self, process_id, operation, duration=0.02, exclusive=False):
        """Adiciona solicitação à fila e protege o uso real com mutex."""
        request = (process_id, operation)
        with self.queue_lock:
            self.queue.append(request)
            position = len(self.queue)
        self._log(f"{process_id} solicitou {operation} em {self.device_name}; posição observada: {position}")

        # O mutex impede que duas threads usem simultaneamente o dispositivo.
        with self.device_lock:
            with self.queue_lock:
                try:
                    self.queue.remove(request)
                except ValueError:
                    pass
            mode = "exclusivo" if exclusive else "compartilhado"
            self._log(f"{process_id} iniciou {operation} em {self.device_name} ({mode})")
            sleep(max(0, duration))
            self._log(f"{process_id} concluiu {operation} em {self.device_name}")
        return list(self.events)


def simulate_device_requests(requests, device_name="disco", concurrent=False):
    """Valida solicitações e, opcionalmente, as dispara em threads concorrentes."""
    device = DeviceQueue(device_name)
    valid = []
    for req in requests:
        pid = req["process"]
        operation = req["operation"]
        if not can_access(pid, device_name, operation):
            device._log(f"NEGADO: {pid} não possui permissão para {operation} em {device_name}")
            continue
        exclusive = bool(req.get("exclusive", False))
        if exclusive and not can_access(pid, device_name, "request_exclusive"):
            device._log(f"NEGADO: {pid} não pode solicitar acesso exclusivo a {device_name}")
            continue
        valid.append(req)

    if concurrent:
        threads = []
        for req in valid:
            thread = Thread(
                target=device.request,
                args=(req["process"], req["operation"], req.get("duration", 0.02), req.get("exclusive", False)),
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    else:
        for req in valid:
            device.request(req["process"], req["operation"], req.get("duration", 0), req.get("exclusive", False))
    return list(device.events)
