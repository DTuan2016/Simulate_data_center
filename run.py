from simulate import Inspector

if __name__ == "__main__":
    file_path = "/home/thuong/data/merged_output/grouped_metrics_2024-09-01.csv"
    timestamp = "2024-09-01 02:00:00"

    inspector = Inspector(file_path)
    inspector.inspect_by_timestamp(timestamp)
