
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os

# 喜欢我的史山吗？？
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (16, 20)

# 读取CSV
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ItemData_2026.07.02_11.32.39.csv')
df = pd.read_csv(csv_path)
df.columns = [c.split('__', 1)[-1] if '__' in c else c for c in df.columns]

fig, axes = plt.subplots(5, 2, figsize=(18, 24))
fig.suptitle('充电数据分析 Dashboard', fontsize=16, fontweight='bold', y=0.995)

# 时间轴
time_labels = df['time'].str.replace('2026.07.02_', '')

# 1. SOC变化
ax = axes[0, 0]
if 'SOC' in df.columns and not df['SOC'].isna().all():
    ax.plot(range(len(df)), df['SOC'], 'b-o', linewidth=2, markersize=4)
    ax.set_title('电池SOC变化', fontsize=12, fontweight='bold')
    ax.set_ylabel('SOC (%)')
    ax.set_ylim(-2, 30)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    for i, v in enumerate(df['SOC']):
        if i % 5 == 0:
            ax.annotate(f'{v}%', (i, v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

# 2. 电池电压
ax = axes[0, 1]
if 'VBAT' in df.columns and not df['VBAT'].isna().all():
    ax.plot(range(len(df)), df['VBAT']/1000, 'g-o', linewidth=2, markersize=4)
    ax.set_title('电池电压 (VBAT)', fontsize=12, fontweight='bold')
    ax.set_ylabel('电压 (V)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=3.0, color='r', linestyle='--', alpha=0.5, label='3.0V')
    ax.axhline(y=4.2, color='orange', linestyle='--', alpha=0.5, label='4.2V')
    ax.legend(fontsize=8)

# 3. 充电电流对比
ax = axes[1, 0]
if 'CHG_IBUS' in df.columns and not df['CHG_IBUS'].isna().all():
    ax.plot(range(len(df)), df['CHG_IBUS'], 'r-o', linewidth=2, markersize=3, label='CHG_IBUS')
if 'FC_IBUS' in df.columns and not df['FC_IBUS'].isna().all():
    ax.plot(range(len(df)), df['FC_IBUS'], 'orange', linewidth=2, markersize=3, label='FC_IBUS', linestyle='--')
ax.set_title('充电电流对比', fontsize=12, fontweight='bold')
ax.set_ylabel('电流 (mA)')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)

# 4. 电池电流 (IBAT)
ax = axes[1, 1]
if 'IBAT' in df.columns and not df['IBAT'].isna().all():
    ibat = df['IBAT']
    colors = ['green' if v < -3000 else 'orange' if v < -1000 else 'red' for v in ibat]
    ax.bar(range(len(df)), -ibat, color=colors, alpha=0.7)
    ax.set_title('电池充电电流 (IBAT, 正值=充电)', fontsize=12, fontweight='bold')
    ax.set_ylabel('电流 (mA)')
    ax.grid(True, alpha=0.3)

# 5. 适配器VBUS
ax = axes[2, 0]
if 'ADPT_VBUS' in df.columns and not df['ADPT_VBUS'].isna().all():
    vbus = df['ADPT_VBUS']
    ax.plot(range(len(df)), vbus/1000, 'purple', linewidth=2, marker='o', markersize=3)
    ax.set_title('适配器VBUS电压', fontsize=12, fontweight='bold')
    ax.set_ylabel('电压 (V)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=5, color='gray', linestyle='--', alpha=0.5, label='5V')
    ax.axhline(y=9, color='gray', linestyle='--', alpha=0.5, label='9V')
    ax.legend(fontsize=8)

# 6. 功率估算
ax = axes[2, 1]
if 'ADPT_VBUS' in df.columns and 'ADPT_IBUS' in df.columns:
    power = (df['ADPT_VBUS'] * df['ADPT_IBUS'] / 1000).dropna()
    ax.fill_between(range(len(power)), power/1000, alpha=0.3, color='red')
    ax.plot(range(len(power)), power/1000, 'r-', linewidth=2, marker='o', markersize=3)
    ax.set_title('适配器输出功率', fontsize=12, fontweight='bold')
    ax.set_ylabel('功率 (W)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=18, color='orange', linestyle='--', alpha=0.5, label='18W')
    ax.axhline(y=33, color='red', linestyle='--', alpha=0.5, label='33W')
    ax.legend(fontsize=8)

# 7. 温度监控
ax = axes[3, 0]
temp_plotted = False
if 'TBAT' in df.columns and not df['TBAT'].isna().all():
    ax.plot(range(len(df)), df['TBAT'], 'b-o', linewidth=2, markersize=3, label='电池温度')
    temp_plotted = True
if 'TMBOARD' in df.columns and not df['TMBOARD'].isna().all():
    ax.plot(range(len(df)), df['TMBOARD'], 'g-s', linewidth=2, markersize=3, label='主板温度')
    temp_plotted = True
if temp_plotted:
    ax.set_title('温度监控', fontsize=12, fontweight='bold')
    ax.set_ylabel('温度 (°C)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=45, color='red', linestyle='--', alpha=0.5, label='45°C警戒线')
    ax.legend(fontsize=9)

# 8. 快充相关电压
ax = axes[3, 1]
if 'FC_VBUS' in df.columns and not df['FC_VBUS'].isna().all():
    ax.plot(range(len(df)), df['FC_VBUS']/1000, 'r-o', linewidth=2, markersize=3, label='FC_VBUS')
if 'FC_VBAT' in df.columns and not df['FC_VBAT'].isna().all():
    ax.plot(range(len(df)), df['FC_VBAT']/1000, 'b-s', linewidth=2, markersize=3, label='FC_VBAT')
ax.set_title('快充电压', fontsize=12, fontweight='bold')
ax.set_ylabel('电压 (V)')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9)

# 9. 线缆电阻
ax = axes[4, 0]
if 'FC_CAB_MOHM' in df.columns and not df['FC_CAB_MOHM'].isna().all():
    cab = df['FC_CAB_MOHM']
    ax.bar(range(len(df)), cab, color='teal', alpha=0.7)
    ax.set_title('线缆电阻', fontsize=12, fontweight='bold')
    ax.set_ylabel('电阻 (mΩ)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=100, color='orange', linestyle='--', alpha=0.5, label='100mΩ')
    ax.axhline(y=200, color='red', linestyle='--', alpha=0.5, label='200mΩ')
    ax.legend(fontsize=8)

# 10. 快充使能和模式
ax = axes[4, 1]
fchg_data = []
labels = []
if 'FCHG_EN' in df.columns:
    fchg_data.append(df['FCHG_EN'].values)
    labels.append('FCHG_EN')
if 'FCHG_MODE' in df.columns:
    fchg_data.append(df['FCHG_MODE'].values)
    labels.append('FCHG_MODE')
if fchg_data:
    x = np.arange(len(df))
    width = 0.35
    for i, (data, label) in enumerate(zip(fchg_data, labels)):
        ax.bar(x + i*width - width/2, data, width, label=label, alpha=0.7)
    ax.set_title('快充状态', fontsize=12, fontweight='bold')
    ax.set_ylabel('状态值')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

# 设置x轴标签
for ax_row in axes:
    for ax in ax_row:
        ax.set_xticks(range(0, len(df), 5))
        ax.set_xticklabels([time_labels.iloc[i] if i < len(time_labels) else '' for i in range(0, len(df), 5)], rotation=45, ha='right', fontsize=8)

plt.tight_layout()
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charging_analysis_dashboard.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
plt.show()
print(f"图表已保存: {output_path}")

# 史山到头咯，byebye