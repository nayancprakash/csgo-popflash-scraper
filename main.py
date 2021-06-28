import requests
import csv
from bs4 import BeautifulSoup

def get_title(data):
    title = data.get("title")
    if title == None:
        return data.get("tile")
    return title

if __name__ == "__main__":

    match_id = input("Please enter the popflash match ID:")
    csv_file = input("Please enter the CSV file to output to:")

    URL = "https://popflash.site/match/" + match_id.strip()
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    scoreboard = soup.find(class_="scoreboards")
    stats = {}
    for table in scoreboard.find_all("table"):
        stat_names = []
        for y, row in enumerate(table.find_all("tr")):
            player = None
            for x, data in enumerate(row.find_all("td")):
                if y == 0 and x > 0:
                    stat_names.append(get_title(data))
                elif y > 0 and x == 0:
                    player = get_title(data)
                elif y > 0 and x > 0:
                    # print(player)
                    if player not in stats:
                        stats[player] = {}
                    stats[player][stat_names[x-1]] = data.text

    csv_lines = [["Names"]]
    csv_lines[0].extend(stats.keys())
    
    for player_stats in stats.values():
        if len(csv_lines) == 1:
            for key in player_stats.keys():
                csv_lines.append([key])
        for index, (_, value) in enumerate(player_stats.items()):
            csv_lines[index + 1].append(value)

    writer = csv.writer(open(csv_file + ".csv", "w", newline=""))
    for row in csv_lines:
        writer.writerow(row)