import psutil

# Quantidade de núcleos da CPU
print(f"Número de núcleos da CPU: {psutil.cpu_count(logical=False)}")

# Quantidade de memória usada e livre
mem = psutil.virtual_memory()
print(f"Memória usada: {mem.used / (1024 ** 3):.2f} GB")
print(f"Memória livre: {mem.available / (1024 ** 3):.2f} GB")

# Lista de processos
print("\nLista de processos:")
for proc in psutil.process_iter(['pid', 'name']):
    print(f"PID: {proc.info['pid']} - Nome: {proc.info['name']}")

# Detalhamento de processo por ID (exemplo com PID 1)
pid = 1  # Pode-se alterar para o PID desejado
try:
    proc = psutil.Process(pid)
    print(f"\nDetalhes do processo com PID {pid}:")
    print(f"Nome: {proc.name()}")
    print(f"Status: {proc.status()}")
    print(f"Uso de CPU: {proc.cpu_percent(interval=1.0)}%")
    print(f"Uso de memória: {proc.memory_info().rss / (1024 ** 2):.2f} MB")
except psutil.NoSuchProcess:
    print(f"Processo com PID {pid} não encontrado.")

# Nível de bateria
battery = psutil.sensors_battery()
print(f"\nNível de bateria: {battery.percent}%")
