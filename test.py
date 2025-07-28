import pandas as pd

# Load file
df_vm = pd.read_csv("/home/thuong/data/merged_output/grouped_metrics_2024-09-01.csv")
df_host = pd.read_csv("/home/thuong/data/merged_output/merged_output.csv")

# Chuyển cột timestamp sang datetime
df_vm['timestamp'] = pd.to_datetime(df_vm['timestamp'])
df_host['timestamp'] = pd.to_datetime(df_host['timestamp'])

# Kiểm tra xem có timestamp nào đúng như vậy không
ts = pd.to_datetime("2024-09-01 01:00:00")

print("Timestamp VM tồn tại?", ts in df_vm['timestamp'].values)
print("Timestamp Host tồn tại?", ts in df_host['timestamp'].values)

# In ra các timestamp gần đúng nếu cần
print("\nCác mốc thời gian có trong VM file:")
print(df_vm['timestamp'].drop_duplicates().sort_values().to_list())

print("\nCác mốc thời gian có trong Host file:")
print(df_host['timestamp'].drop_duplicates().sort_values().to_list())
