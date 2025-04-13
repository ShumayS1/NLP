
import csv
import os
from datetime import datetime

HISTORY_LOG = "analysis_history.csv"

def save_analysis_result(texts, results, compatibility):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = []

    for i, text in enumerate(texts):
        entry = {
            "timestamp": timestamp,
            "employee": f"Сотрудник {i + 1}",
            "text": text,
            "pluses": ", ".join(results[i]["pluses"]),
            "minuses": ", ".join(results[i]["minuses"]),
            "sentiment": results[i]["sentiment"]
        }
        data.append(entry)

    # Запись в историю
    write_header = not os.path.exists(HISTORY_LOG)
    with open(HISTORY_LOG, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(data)

"""  # Совместимость сохраняется отдельно
    compatibility_path = f"compatibility_{timestamp.replace(':', '-')}.csv"
    with open(compatibility_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Сотрудник A", "Сотрудник B", "Совместимость (%)"])
        for pair, score in compatibility:
            writer.writerow([pair[0] + 1, pair[1] + 1, round(score, 1)])

    return HISTORY_LOG, compatibility_path
 """