# Take in a textfile called "List of all modpacks supported by Aternos.txt" as input
# and output a json file called "modpacks.json"

import json, requests
from bs4 import BeautifulSoup

with open("aternos_modpacks.txt", "r") as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]
    lines = [x for x in lines if x != ""]

# create output text file
with open("found_modpacks.txt", "w") as f:
    f.write("[")

for line in lines:
    # Get the CurseForge modpack whose name is this line
    # The name is the same as the URL
    url = "https://www.curseforge.com/minecraft/modpacks/" + line

    # search and get first response from https://www.modpackindex.com/api/v1/modpacks?limit=1&page=1&name=
    search_url = "https://www.modpackindex.com/api/v1/modpacks?limit=1&page=1&name=" + line.replace("-", " ")
    response = requests.get(search_url)
    response = json.loads(response.text)
    
    # check if response is empty
    if response["data"] == []:
        print("No modpack found for " + line)
        continue

    # check if modpack url matches our url
    if response["data"][0]["url"] != url:
        print("Modpack URL does not match for " + line)
        continue

    # get the modpack ModpackIndex id
    modpack_id = response["data"][0]["id"]

    # get modpack info from https://www.modpackindex.com/api/v1/modpacks/
    modpack_url = "https://www.modpackindex.com/api/v1/modpack/" + str(modpack_id)
    response = requests.get(modpack_url)
    
    # for every version in minecraft_version, find 1.19.2
    versions = json.loads(response.text)["data"]["minecraft_versions"]
    for version in versions:
        if version["name"] == "1.19.2":
            print(line + " has 1.19.2")
            # now get the mods in this modpack
            mods_url = "https://www.modpackindex.com/api/v1/modpack/" + str(modpack_id) + "/mods"
            response = requests.get(mods_url)
            mods = json.loads(response.text)["data"]
            # and check if it has anything with 'origins' in it
            for mod in mods:
                if "origins" in mod["name"].lower():
                    print("Found Origins for " + line)
                    # write to output file
                    with open("found_modpacks.txt", "a") as f:
                        f.write(json.dumps(modpack_id) + ",")
                    continue
