import os
from pprint import pprint

import numpy as np
import requests

SESSION = os.environ.get("AOC_SESSION")

if __name__ == "__main__":
    url = "http://www.adventofcode.com/2021/leaderboard/private/view/191458.json"
    page = requests.get(url, cookies={"session": SESSION})
    scores = page.json()
    members = list(scores["members"])
    names = {scores["members"][m]["name"]: m for m in members}

    def get_day_for_name(day, name):
        return scores["members"][names[name]]["completion_day_level"].get(str(day))

    def get_star_time(day, part, name):
        try:
            return get_day_for_name(day, name)[str(part)]["get_star_ts"]
        except (KeyError, TypeError):
            return None

    name_list = list(names)
    name_list = ["jrc-exp", "Kevin McCrea", "sheromon"]
    points = {name: 0 for name in name_list}
    for day in range(1, 26):
        for part in range(1, 3):
            times = []
            for name in name_list:
                times.append(get_star_time(day, part, name))
            order = list(reversed(sorted(range(len(times)), key=lambda k: times[k] if times[k] else 1e20)))
            for score, idx in enumerate(order, start=1):
                if times[idx]:
                    # Standard Score:
                    # points[name_list[idx]] += score
                    # Scaled by ~ Day 25 = 1.5x and Part 2 = 1.7x
                    points[name_list[idx]] += score * day ** 0.25 * part ** 0.5
                    # points[name_list[idx]] += score * np.sqrt(day)
                    # points[name_list[idx]] += score * np.sqrt(day) * part
                    # points[name_list[idx]] += score * day ** 0.25
                    # points[name_list[idx]] += score * part

    for name in points:
        points[name] = int(points[name])

    order = list(reversed(sorted(range(len(name_list)), key=lambda k: points[name_list[k]])))
    for rank, idx in enumerate(order, start=1):
        print("%02d: %16s\t%04d" % (rank, name_list[idx], points[name_list[idx]]))
