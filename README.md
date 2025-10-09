# Dashboard Sistema Operativo

Un dashboard interactivo para visualizar información del sistema operativo en tiempo real.

## Características

- **Información de CPU**: Muestra el número de núcleos y uso actual
- **Información de Memoria**: Visualiza memoria usada, libre y total
- **Lista de Procesos**: Tabla interactiva con todos los procesos del sistema
- **Detalles de Proceso**: Información detallada al seleccionar o buscar por PID
- **Nivel de Batería**: Estado de la batería (si está disponible)
- **Gráficos en Tiempo Real**: Visualización gráfica del uso de CPU y memoria
- **Actualización Automática**: Los datos se actualizan automáticamente cada 2 segundos

## Requisitos

- Python 3.6 o superior
- Las dependencias se instalan automáticamente con pip

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar el dashboard:
```bash
python dastbordSO.py
```

## Funcionalidades

### Panel de Información del Sistema
- **CPU**: Número de núcleos físicos y porcentaje de uso actual
- **Memoria**: Cantidad de memoria usada, total y porcentaje de uso
- **Batería**: Nivel de carga y estado de conexión (si aplica)

### Gráficos de Rendimiento
- **Gráfico de CPU**: Muestra el uso de CPU en tiempo real
- **Gráfico de Memoria**: Visualiza el uso de memoria en tiempo real
- Los gráficos mantienen un historial de los últimos 50 puntos de datos

### Gestión de Procesos
- **Lista de Procesos**: Tabla con PID, nombre, uso de CPU y memoria
- **Búsqueda por PID**: Campo para buscar un proceso específico por su ID
- **Detalles Completos**: Al seleccionar un proceso se muestran:
  - Nombre y estado del proceso
  - Uso de CPU y memoria (RSS, VMS, porcentaje)
  - Usuario propietario
  - Número de hilos
  - Archivos abiertos y conexiones de red
  - Comando completo de ejecución

### Controles
- **Botón Actualizar**: Actualización manual de todos los datos
- **Actualización Automática**: Checkbox para habilitar/deshabilitar actualizaciones automáticas

## Estructura del Código

El dashboard está implementado como una clase `DashboardSO` con los siguientes componentes principales:

- `setup_ui()`: Configuración de la interfaz gráfica
- `update_system_info()`: Actualización de información del sistema
- `update_performance_chart()`: Actualización de gráficos
- `update_process_list()`: Actualización de la lista de procesos
- `show_process_details()`: Mostrar detalles de un proceso específico
- `start_updates()`: Iniciar hilos de actualización automática

## Tecnologías Utilizadas

- **tkinter**: Interfaz gráfica
- **psutil**: Obtención de información del sistema
- **matplotlib**: Gráficos en tiempo real
- **threading**: Actualizaciones en segundo plano