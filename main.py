import requests
import csv
from bs4 import BeautifulSoup

def request_html_soup(match_id):
    cookie = get_cookie()
    URL = "https://popflash.site/match/" + match_id.strip()
    page = requests.get(URL, headers={"cookie": cookie})
    return BeautifulSoup(page.content, "html.parser")

def get_cookie(cookie_file="cookie.cookie"):
    cookie_file = open(cookie_file, "r")
    return cookie_file.read()

def get_title(data):
    title = data.get("title")
    if title == None:
        return data.get("tile")
    return title

def write_to_csv(filename, stats):
    csv_lines = [["Names"]]
    csv_lines[0].extend(stats.keys())
    
    for player_stats in stats.values():
        if len(csv_lines) == 1:
            for key in player_stats.keys():
                csv_lines.append([key])
        for index, (_, value) in enumerate(player_stats.items()):
            csv_lines[index + 1].append(value)

    writer = csv.writer(open(filename + ".csv", "w", newline=""))
    for row in csv_lines:
        writer.writerow(row)

def generate_match_stats(match_container_elem, match_id):
    match_text = match_container_elem.find_all("div")[0].find_all("div")[0].text.split()
    scores = match_text[0:2]
    map_name = match_text[3]
    date = match_container_elem.find_all("span")[0].get("data-date")
    
    match_stats = {}
    match_stats["match_id"] = match_id
    match_stats["match_date"] = date
    match_stats["map"] = map_name
    match_stats["scores"] = scores
    return match_stats

def generate_player_stats(scoreboard_elem):
    stats = {}
    for table_count, table in enumerate(scoreboard_elem.find_all("table")):
        stat_names = []
        for y, row in enumerate(table.find_all("tr")):
            player = None
            for x, data in enumerate(row.find_all("td")):
                if y == 0 and x > 0:
                    stat_names.append(get_title(data))
                elif y > 0 and x == 0:
                    player = get_title(data)
                elif y > 0 and x > 0:
                    if player not in stats:
                        stats[player] = {}
                        stats[player]["Team"] = (table_count // 4) + 1
                    stats[player][stat_names[x-1]] = data.text
    return stats

if __name__ == "__main__":

    match_id = input("Please enter the popflash match ID: ")

    soup = request_html_soup(match_id)

    match_stats = generate_match_stats(soup.find(id="match-container"), match_id)
    match_stats["player_stats"] = generate_player_stats(soup.find(class_="scoreboards"))

    write_to_csv(match_id, match_stats["player_stats"])
    print(match_stats)