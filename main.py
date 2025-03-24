import csv

from psn import PSN
from utils import convert_play_duration, duration_sorter, build_duration


# Token from https://ca.account.sony.com/api/v1/ssocookie
NPSSO = "ololol"
OUTPUT_TABLE = "psn.csv"


if __name__ == "__main__":
    psn_client = PSN(npsso=NPSSO)

    show_records = []
    for game in psn_client.game_list():
        play_duration = convert_play_duration(game.get("playDuration"))
        if not play_duration:
            continue

        trophy_progress = psn_client.game_trophy_progress(game["titleId"])
        if not trophy_progress:
            continue

        record = {
            "name": game["name"],
            "playDuration": play_duration,
            "definedTrophiesTotal": sum(trophy_progress["definedTrophies"].values()),
            "earnedTrophiesTotal": sum(trophy_progress["earnedTrophies"].values()),
        }
        record["progress"] = int(
            record["earnedTrophiesTotal"] / record["definedTrophiesTotal"] * 100
        )
        show_records.append(record)
    show_records.sort(key=duration_sorter, reverse=True)

    with open(OUTPUT_TABLE, "w", newline="") as csvfile:
        fieldnames = ["name", "hours", "minutes", "progress"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in show_records:
            duration = build_duration(record["playDuration"])
            line = {
                "name": record["name"],
                "hours": str(duration.hours),
                "minutes": str(duration.minutes),
                "progress": str(record["progress"]) + "%",
            }

            writer.writerow(line)
