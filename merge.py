import os
import csv

# Укажите путь к папке с CSV-файлами
folder = "outs"  # замените на ваш путь

merged_data = {}

# Функция для преобразования строки progress в целое число (без символа "%")
def progress_to_int(progress_str):
    return int(progress_str.strip().replace("%", ""))

# Проходим по всем файлам в папке
for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(folder, filename)
        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row["name"]
                hours = int(row["hours"])
                minutes = int(row["minutes"])
                progress = row["progress"]
                
                if name in merged_data:
                    merged_data[name]["hours"] += hours
                    merged_data[name]["minutes"] += minutes
                    # Выбираем максимальное progress
                    current_progress = progress_to_int(merged_data[name]["progress"])
                    new_progress = progress_to_int(progress)
                    if new_progress > current_progress:
                        merged_data[name]["progress"] = progress
                else:
                    merged_data[name] = {
                        "name": name,
                        "hours": hours,
                        "minutes": minutes,
                        "progress": progress  # инициализация progress
                    }

# Приводим минуты к нормальному виду: 60 минут = 1 час
for data in merged_data.values():
    extra_hours = data["minutes"] // 60
    data["hours"] += extra_hours
    data["minutes"] = data["minutes"] % 60

# Сортировка данных по количеству часов в порядке убывания
sorted_data = sorted(merged_data.values(), key=lambda x: x["hours"], reverse=True)

# Записываем объединённые и отсортированные данные в новый CSV-файл
output_path = "merged.csv"
with open(output_path, mode="w", newline="", encoding="utf-8") as out_file:
    fieldnames = ["name", "hours", "minutes", "progress"]
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in sorted_data:
        writer.writerow(row)

print("Объединение файлов завершено. Результат записан в", output_path)
