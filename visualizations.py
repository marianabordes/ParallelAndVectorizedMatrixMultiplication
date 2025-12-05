import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. Cargar y Procesar Datos desde CSV
# ==========================================

# Definimos las columnas manualmente porque el CSV usa comas para separar columnas
# Y TAMBIÉN para los decimales, lo que confunde al parser estándar.
raw_cols = ['N', 'Strategy', 'TimeMs', 
            'Speedup_Int', 'Speedup_Dec', 
            'Eff_Int', 'Eff_Dec', 
            'CPU_Int', 'CPU_Dec', 
            'MemoryBytes']

# Leemos el archivo local 'results.csv'
# dtype=str es crucial para leer "0938" sin perder el cero inicial antes de unirlo
try:
    df = pd.read_csv('results.csv', names=raw_cols, skiprows=1, dtype=str)
except FileNotFoundError:
    print("Error: No se encuentra el archivo 'results2.csv' en el directorio.")
    exit()

# Reconstruimos los números decimales uniendo la parte entera y decimal
df['Speedup'] = (df['Speedup_Int'] + '.' + df['Speedup_Dec']).astype(float)
df['Efficiency'] = (df['Eff_Int'] + '.' + df['Eff_Dec']).astype(float)
df['CPU%'] = (df['CPU_Int'] + '.' + df['CPU_Dec']).astype(float)

# Convertimos las columnas numéricas enteras
df['N'] = df['N'].astype(int)
df['TimeMs'] = df['TimeMs'].astype(int)
df['MemoryBytes'] = df['MemoryBytes'].astype(int)

# ==========================================
# 2. Configuración de Gráficos
# ==========================================
sns.set(style="whitegrid", context="talk")
plt.rcParams['figure.figsize'] = (10, 6)

# ==========================================
# 3. Generación de Gráficos
# ==========================================

# --- Gráfico 1: Tiempo de Ejecución (Escala LOGARÍTMICA) ---
# Útil para ver diferencias de órdenes de magnitud
plt.figure()
sns.lineplot(data=df, x='N', y='TimeMs', hue='Strategy', marker='o', linewidth=2.5)
plt.title('Execution Time vs Matrix Size (Log Scale)')
plt.ylabel('Time (ms)')
plt.xlabel('Matrix Size (N)')
plt.yscale('log')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('execution_time_log.png', dpi=300)
plt.close()

# --- Gráfico 2: Tiempo de Ejecución 
# Útil para mostrar el impacto visual masivo de la complejidad cúbica
plt.figure()
sns.lineplot(data=df, x='N', y='TimeMs', hue='Strategy', marker='o', linewidth=2.5)
plt.title('Execution Time vs Matrix Size')
plt.ylabel('Time (ms)')
plt.xlabel('Matrix Size (N)')
# Sin escala logarítmica aquí
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('execution_time_linear.png', dpi=300)
plt.close()

# --- Gráfico 3: Speedup (Aceleración) ---
plt.figure()
sns.lineplot(data=df, x='N', y='Speedup', hue='Strategy', marker='o', linewidth=2.5)
plt.axhline(1, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
plt.title('Speedup vs Matrix Size')
plt.ylabel('Speedup Factor')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('speedup.png', dpi=300)
plt.close()

# --- Gráfico 4: Eficiencia ---
plt.figure()
sns.lineplot(data=df, x='N', y='Efficiency', hue='Strategy', marker='o', linewidth=2.5)
plt.title('Efficiency vs Matrix Size')
plt.ylabel('Efficiency (Speedup / Cores)')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('efficiency.png', dpi=300)
plt.close()

# --- Gráfico 5: Uso de CPU ---
plt.figure()
sns.barplot(data=df, x='N', y='CPU%', hue='Strategy')
plt.title('CPU Usage (%) by Matrix Size')
plt.ylabel('Max CPU Load (%)')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('cpu_usage.png', dpi=300)
plt.close()

# --- Gráfico 6: Comparativa Final (N=2048) ---
plt.figure()
df_max = df[df['N'] == 2048].sort_values('TimeMs', ascending=False)
bp = sns.barplot(data=df_max, x='Strategy', y='TimeMs', palette='viridis')
plt.title('Execution Time at N=2048 (Worst Case)')
plt.ylabel('Time (ms)')
plt.xlabel('Strategy')
plt.xticks(rotation=15)
for container in bp.containers:
    bp.bar_label(container, fmt='%.0f')
plt.tight_layout()
plt.savefig('time_n2048.png', dpi=300)
plt.close()

print("¡Completed ! Plots generated successfully.")