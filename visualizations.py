import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Crear carpeta 'visualizations' si no existe
os.makedirs("visualizations", exist_ok=True)

# ==========================================
# 1. Cargar y Procesar Datos desde CSV
# ==========================================

raw_cols = ['N', 'Strategy', 'TimeMs',
            'Speedup_Int', 'Speedup_Dec',
            'Eff_Int', 'Eff_Dec',
            'CPU_Int', 'CPU_Dec',
            'MemoryBytes']

try:
    df = pd.read_csv('results.csv', names=raw_cols, skiprows=1, dtype=str)
except FileNotFoundError:
    print("Error: No se encuentra el archivo 'results2.csv' en el directorio.")
    exit()

df['Speedup'] = (df['Speedup_Int'] + '.' + df['Speedup_Dec']).astype(float)
df['Efficiency'] = (df['Eff_Int'] + '.' + df['Eff_Dec']).astype(float)
df['CPU%'] = (df['CPU_Int'] + '.' + df['CPU_Dec']).astype(float)

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

plt.figure()
sns.lineplot(data=df, x='N', y='TimeMs', hue='Strategy', marker='o', linewidth=2.5)
plt.title('Execution Time vs Matrix Size (Log Scale)')
plt.ylabel('Time (ms)')
plt.xlabel('Matrix Size (N)')
plt.yscale('log')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/execution_time_log.png', dpi=300)
plt.close()

plt.figure()
sns.lineplot(data=df, x='N', y='TimeMs', hue='Strategy', marker='o', linewidth=2.5)
plt.title('Execution Time vs Matrix Size')
plt.ylabel('Time (ms)')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/execution_time_linear.png', dpi=300)
plt.close()

plt.figure()
sns.lineplot(data=df, x='N', y='Speedup', hue='Strategy', marker='o', linewidth=2.5)
plt.axhline(1, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
plt.title('Speedup vs Matrix Size')
plt.ylabel('Speedup Factor')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/speedup.png', dpi=300)
plt.close()

plt.figure()
sns.lineplot(data=df, x='N', y='Efficiency', hue='Strategy', marker='o', linewidth=2.5)
plt.title('Efficiency vs Matrix Size')
plt.ylabel('Efficiency (Speedup / Cores)')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/efficiency.png', dpi=300)
plt.close()

plt.figure()
sns.barplot(data=df, x='N', y='CPU%', hue='Strategy')
plt.title('CPU Usage (%) by Matrix Size')
plt.ylabel('Max CPU Load (%)')
plt.xlabel('Matrix Size (N)')
plt.legend(title='Strategy', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualizations/cpu_usage.png', dpi=300)
plt.close()

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
plt.savefig('visualizations/time_n2048.png', dpi=300)
plt.close()

print("¡Completed ! Plots generated successfully.")