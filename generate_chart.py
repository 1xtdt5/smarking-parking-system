# 数据集分布分析代码 - 生成两个独立图表
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 实际数据集分布数据
data = {
    '数据集划分': ['训练集', '验证集', '测试集'],
    '图像数量': [26, 3, 3],
    '空车位数量': [156, 18, 18],
    '占用车位数量': [104, 12, 12]
}

# 图表1：数据集划分比例饼图
plt.figure(figsize=(8, 8))
plt.pie(data['图像数量'], labels=data['数据集划分'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#99ff99', '#ffcc99'])
plt.title('数据集划分比例', fontsize=16, fontweight='bold')
plt.axis('equal')  # 保证饼图为圆形
plt.tight_layout()
plt.savefig('dataset_split_chart.png', dpi=300, bbox_inches='tight')
plt.close()
print("图表1生成完成：dataset_split_chart.png")

# 图表2：车位状态分布柱状图
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(data['数据集划分']))
plt.bar(index, data['空车位数量'], bar_width, label='空车位', color='#66b3ff')
plt.bar([i + bar_width for i in index], data['占用车位数量'], bar_width, label='占用车位', color='#ff6666')
plt.xlabel('数据集划分', fontsize=12)
plt.ylabel('车位数量', fontsize=12)
plt.title('车位状态分布', fontsize=16, fontweight='bold')
plt.xticks([i + bar_width/2 for i in index], data['数据集划分'], fontsize=10)
plt.legend(title='车位状态', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('parking_status_chart.png', dpi=300, bbox_inches='tight')
plt.close()
print("图表2生成完成：parking_status_chart.png")

print("所有图表生成完成！")