import srcomapi, srcomapi.datatypes as dt

import csv,requests,sys
from bs4 import BeautifulSoup

api = srcomapi.SpeedrunCom()

res = api.search(srcomapi.datatypes.Game, {"name": "minecraft: java edition"})

game = res[0]

category = game.categories[0]

mc_runs = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))

data = mc_runs.runs

labels = ['Game Ver', 'Time']

c = 0

with open("records.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(labels)

    for data_item in data:
        run_obj = data_item['run']

        link = run_obj.weblink

        print(f"Getting {link}")

        r = requests.get(link)

        soup = BeautifulSoup(r.content, 'html.parser')

        lol = soup.find_all("div", {"class": "valuesList"})

        tag = lol[0]
        ver = tag.contents[0].replace("Version: ", "").strip().replace('"',"") # hell on earth

        csv_row = [ver , str(run_obj.times['ingame_t'])]
        
        writer.writerow(csv_row)

        c += 1

        if c == 300:
            break