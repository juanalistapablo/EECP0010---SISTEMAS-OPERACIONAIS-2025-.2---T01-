import tkinter as tk
from tkinter import ttk
import psutil
import threading

# Funções para obter as informações do sistema
def get_cpu_info():
    cpu_cores = psutil.cpu_count(logical=True)
    return f"Núcleos CPU: {cpu_cores}"

def get_memory_info():
    memory = psutil.virtual_memory()
    used_memory = memory.used / (1024 ** 3)  # GB
    free_memory = memory.available / (1024 ** 3)  # GB
    return f"Memória Usada: {used_memory:.2f} GB | Memória Livre: {free_memory:.2f} GB"

def get_process_list():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append(f"ID: {proc.info['pid']} - Nome: {proc.info['name']}")
    return processes

def get_process_details(pid):
    try:
        process = psutil.Process(pid)
        details = {
            "PID": process.pid,
            "Nome": process.name(),
            "Status": process.status(),
            "CPU%": process.cpu_percent(interval=1),
            "Memória%": process.memory_percent(),
            "Usuário": process.username(),
            "Iniciado em": process.create_time(),
        }
        return details
    except psutil.NoSuchProcess:
        return f"Processo com ID {pid} não encontrado."

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        power_plugged = battery.power_plugged
        return f"Bateria: {percent}% {'(plugado)' if power_plugged else '(desconectado)'}"
    else:
        return "Informações da bateria não disponíveis."

# Função para atualizar as informações no dashboard
def update_dashboard():
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    battery_info = get_battery_info()

    # Atualizando os labels do dashboard
    label_cpu.config(text=cpu_info)
    label_memory.config(text=memory_info)
    label_battery.config(text=battery_info)

    # Atualizar a lista de processos
    processes = get_process_list()
    process_listbox.delete(0, tk.END)
    for process in processes[:10]:  # Limitar a 10 processos
        process_listbox.insert(tk.END, process)

    # Chamando a função novamente a cada 5 segundos para atualizar
    root.after(5000, update_dashboard)

# Função para mostrar detalhes de um processo selecionado
def show_process_details():
    try:
        pid = int(process_id_entry.get())
        details = get_process_details(pid)
        details_text = "\n".join([f"{key}: {value}" for key, value in details.items()])
        details_label.config(text=details_text)
    except ValueError:
        details_label.config(text="Digite um PID válido.")

# Criando a interface gráfica
root = tk.Tk()
root.title("Dashboard de Sistema Operacional")

# Layout
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0)

# Labels para exibir as informações
label_cpu = ttk.Label(frame, text="CPU: Carregando...", width=50)
label_cpu.grid(row=0, column=0, sticky="w", padx=5, pady=5)

label_memory = ttk.Label(frame, text="Memória: Carregando...", width=50)
label_memory.grid(row=1, column=0, sticky="w", padx=5, pady=5)

label_battery = ttk.Label(frame, text="Bateria: Carregando...", width=50)
label_battery.grid(row=2, column=0, sticky="w", padx=5, pady=5)

# Listbox para exibir os processos
process_listbox = tk.Listbox(frame, width=50, height=10)
process_listbox.grid(row=3, column=0, padx=5, pady=5)

# Entrar com o PID para detalhes
process_id_label = ttk.Label(frame, text="Digite o ID do processo:")
process_id_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

process_id_entry = ttk.Entry(frame, width=10)
process_id_entry.grid(row=4, column=1, padx=5, pady=5)

show_details_button = ttk.Button(frame, text="Mostrar Detalhes", command=show_process_details)
show_details_button.grid(row=4, column=2, padx=5, pady=5)

# Label para exibir detalhes do processo
details_label = ttk.Label(frame, text="Detalhes do processo aparecerão aqui.", width=50, justify="left")
details_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=5)

# Iniciar a atualização do dashboard
update_dashboard()

# Iniciar a interface gráfica
root.mainloop()
