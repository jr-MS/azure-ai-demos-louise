import pandas as pd

# 读取 Markdown 文件
with open("test.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 提取表格部分
table_lines = []
in_table = False
for line in lines:
    if line.strip().startswith("|"):
        in_table = True
        table_lines.append(line)
    elif in_table and not line.strip().startswith("|"):
        break  # 表格结束

# 保存为临时 Markdown 表格
with open("temp_table.md", "w", encoding="utf-8") as f:
    f.writelines(table_lines)

# 用 pandas 读取并写入 Excel
df = pd.read_table("temp_table.md", sep="|", engine="python", skipinitialspace=True)
df = df.drop(df.columns[[0, -1]], axis=1)  # 去掉首尾空列
df.to_excel("test.xlsx", index=False)

print("已将 test.md 中的表格导出为 test.xlsx")
