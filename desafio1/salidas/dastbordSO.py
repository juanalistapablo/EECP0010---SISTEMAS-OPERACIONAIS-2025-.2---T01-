import psutil
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

class DashboardSO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dashboard Sistema Operativo")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables para datos
        self.cpu_data = []
        self.memory_data = []
        self.updating = False
        
        self.setup_ui()
        self.start_updates()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Dashboard Sistema Operativo", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame izquierdo - Información del sistema
        left_frame = ttk.LabelFrame(main_frame, text="Información del Sistema", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # CPU Info
        self.cpu_label = ttk.Label(left_frame, text="", font=('Arial', 10, 'bold'))
        self.cpu_label.pack(anchor=tk.W, pady=5)
        
        # Memoria Info
        self.memory_label = ttk.Label(left_frame, text="", font=('Arial', 10, 'bold'))
        self.memory_label.pack(anchor=tk.W, pady=5)
        
        # Batería Info
        self.battery_label = ttk.Label(left_frame, text="", font=('Arial', 10, 'bold'))
        self.battery_label.pack(anchor=tk.W, pady=5)
        
        # Frame central - Gráficos
        center_frame = ttk.LabelFrame(main_frame, text="Gráficos de Rendimiento", padding="10")
        center_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        center_frame.rowconfigure(0, weight=1)
        center_frame.columnconfigure(0, weight=1)
        
        # Crear gráfico de CPU y memoria
        self.create_performance_chart(center_frame)
        
        # Frame derecho - Procesos
        right_frame = ttk.LabelFrame(main_frame, text="Gestión de Procesos", padding="10")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Búsqueda de proceso
        ttk.Label(right_frame, text="Buscar proceso por PID:").pack(anchor=tk.W)
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.pid_entry = ttk.Entry(search_frame)
        self.pid_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pid_entry.bind('<Return>', self.search_process)
        
        search_btn = ttk.Button(search_frame, text="Buscar", command=self.search_process)
        search_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Lista de procesos
        ttk.Label(right_frame, text="Lista de Procesos:").pack(anchor=tk.W, pady=(10, 5))
        
        # Treeview para procesos
        columns = ('PID', 'Nombre', 'CPU%', 'Memoria MB')
        self.process_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        # Scrollbar para la lista de procesos
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame inferior - Detalles del proceso
        details_frame = ttk.LabelFrame(main_frame, text="Detalles del Proceso", padding="10")
        details_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(0, weight=1)
        
        self.process_details = scrolledtext.ScrolledText(details_frame, height=8, state=tk.DISABLED)
        self.process_details.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones de control
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        self.update_btn = ttk.Button(control_frame, text="Actualizar", command=self.manual_update)
        self.update_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.auto_update_var = tk.BooleanVar(value=True)
        auto_update_check = ttk.Checkbutton(control_frame, text="Actualización automática", 
                                          variable=self.auto_update_var)
        auto_update_check.pack(side=tk.LEFT)
        
        # Bind para selección de proceso
        self.process_tree.bind('<<TreeviewSelect>>', self.on_process_select)
        
    def create_performance_chart(self, parent):
        """Crear gráfico de rendimiento en tiempo real"""
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        
        self.fig.tight_layout()
        
        # Canvas para matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_system_info(self):
        """Actualizar información del sistema"""
        try:
            # CPU
            cpu_count = psutil.cpu_count(logical=False)
            cpu_usage = psutil.cpu_percent(interval=0.1)
            self.cpu_label.config(text=f"CPU: {cpu_count} núcleos - Uso: {cpu_usage}%")
            
            # Memoria
            mem = psutil.virtual_memory()
            used_gb = mem.used / (1024 ** 3)
            total_gb = mem.total / (1024 ** 3)
            self.memory_label.config(text=f"Memoria: {used_gb:.1f}GB / {total_gb:.1f}GB usada ({mem.percent}%)")
            
            # Batería
            battery = psutil.sensors_battery()
            if battery:
                battery_text = f"Batería: {battery.percent}%"
                if battery.power_plugged:
                    battery_text += " (Conectada)"
                else:
                    battery_text += " (Desconectada)"
                self.battery_label.config(text=battery_text)
            else:
                self.battery_label.config(text="Batería: No disponible")
                
            # Actualizar datos para gráficos
            self.cpu_data.append(cpu_usage)
            self.memory_data.append(mem.percent)
            
            # Mantener solo los últimos 50 puntos
            if len(self.cpu_data) > 50:
                self.cpu_data = self.cpu_data[-50:]
                self.memory_data = self.memory_data[-50:]
                
        except Exception as e:
            print(f"Error actualizando información del sistema: {e}")
            
    def update_performance_chart(self):
        """Actualizar gráficos de rendimiento"""
        try:
            self.ax1.clear()
            self.ax2.clear()
            
            if self.cpu_data:
                # Gráfico de CPU
                self.ax1.plot(self.cpu_data, 'b-', linewidth=2)
                self.ax1.set_title('Uso de CPU (%)', fontsize=10)
                self.ax1.set_ylim(0, 100)
                self.ax1.grid(True, alpha=0.3)
                
            if self.memory_data:
                # Gráfico de memoria
                self.ax2.plot(self.memory_data, 'r-', linewidth=2)
                self.ax2.set_title('Uso de Memoria (%)', fontsize=10)
                self.ax2.set_ylim(0, 100)
                self.ax2.grid(True, alpha=0.3)
                
            self.fig.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")
            
    def update_process_list(self):
        """Actualizar lista de procesos"""
        try:
            # Limpiar lista actual
            for item in self.process_tree.get_children():
                self.process_tree.delete(item)
                
            # Obtener procesos y ordenar por uso de CPU
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    cpu_percent = proc.info['cpu_percent']
                    memory_mb = proc.info['memory_info'].rss / (1024 ** 2) if proc.info['memory_info'] else 0
                    processes.append((
                        proc.info['pid'],
                        proc.info['name'][:20],  # Truncar nombre largo
                        f"{cpu_percent:.1f}" if cpu_percent else "0.0",
                        f"{memory_mb:.1f}"
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Ordenar por CPU (descendente)
            processes.sort(key=lambda x: float(x[2]), reverse=True)
            
            # Agregar a la lista (máximo 100 procesos)
            for proc_info in processes[:100]:
                self.process_tree.insert('', 'end', values=proc_info)
                
        except Exception as e:
            print(f"Error actualizando lista de procesos: {e}")
            
    def search_process(self, event=None):
        """Buscar proceso por PID"""
        try:
            pid_text = self.pid_entry.get().strip()
            if not pid_text:
                return
                
            pid = int(pid_text)
            proc = psutil.Process(pid)
            
            # Mostrar detalles en el área de texto
            self.show_process_details(proc)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un PID válido (número entero)")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", f"Proceso con PID {pid_text} no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar proceso: {e}")
            
    def on_process_select(self, event):
        """Manejar selección de proceso en la lista"""
        selection = self.process_tree.selection()
        if selection:
            item = self.process_tree.item(selection[0])
            pid = item['values'][0]
            
            try:
                proc = psutil.Process(pid)
                self.show_process_details(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                messagebox.showerror("Error", "No se puede acceder a los detalles del proceso")
                
    def show_process_details(self, proc):
        """Mostrar detalles del proceso"""
        try:
            self.process_details.config(state=tk.NORMAL)
            self.process_details.delete(1.0, tk.END)
            
            details = f"""DETALLES DEL PROCESO PID {proc.pid}
{'='*50}

Nombre: {proc.name()}
Estado: {proc.status()}
Creación: {time.ctime(proc.create_time())}

USO DE RECURSOS:
CPU: {proc.cpu_percent(interval=0.1):.1f}%
Memoria RSS: {proc.memory_info().rss / (1024**2):.1f} MB
Memoria VMS: {proc.memory_info().vms / (1024**2):.1f} MB
Memoria %: {proc.memory_percent():.2f}%

INFORMACIÓN ADICIONAL:
Usuario: {proc.username() if hasattr(proc, 'username') else 'N/A'}
Núcleos: {proc.num_threads()}
Archivos abiertos: {len(proc.open_files()) if hasattr(proc, 'open_files') else 'N/A'}
Conexiones: {len(proc.connections()) if hasattr(proc, 'connections') else 'N/A'}

COMANDO COMPLETO:
{proc.cmdline()}
"""
            
            self.process_details.insert(1.0, details)
            self.process_details.config(state=tk.DISABLED)
            
        except Exception as e:
            self.process_details.config(state=tk.NORMAL)
            self.process_details.delete(1.0, tk.END)
            self.process_details.insert(1.0, f"Error obteniendo detalles: {e}")
            self.process_details.config(state=tk.DISABLED)
            
    def manual_update(self):
        """Actualización manual de todos los datos"""
        if not self.updating:
            self.update_all_data()
            
    def update_all_data(self):
        """Actualizar todos los datos"""
        try:
            self.updating = True
            self.update_btn.config(text="Actualizando...", state=tk.DISABLED)
            
            # Actualizar en hilo separado para no bloquear UI
            def update_thread():
                self.update_system_info()
                self.update_process_list()
                self.root.after(0, self.update_performance_chart)
                self.root.after(0, lambda: self.update_btn.config(text="Actualizar", state=tk.NORMAL))
                self.root.after(0, lambda: setattr(self, 'updating', False))
                
            threading.Thread(target=update_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en actualización: {e}")
            self.update_btn.config(text="Actualizar", state=tk.NORMAL)
            self.updating = False
            
    def start_updates(self):
        """Iniciar actualizaciones automáticas"""
        def auto_update():
            while True:
                if self.auto_update_var.get() and not self.updating:
                    try:
                        self.update_system_info()
                        self.root.after(0, self.update_performance_chart)
                        time.sleep(2)  # Actualizar cada 2 segundos
                    except Exception:
                        time.sleep(5)  # Esperar más tiempo si hay error
                else:
                    time.sleep(1)
                    
        # Iniciar hilo de actualización automática
        threading.Thread(target=auto_update, daemon=True).start()
        
        # Actualización inicial
        self.root.after(1000, self.update_all_data)
        
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    dashboard = DashboardSO()
    dashboard.run()
