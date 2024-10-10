import requests
import json
import inquirer


def search_mod(props):
    query_list = []
    query = input("Enter name of mod to search: ")
    print()
    res = json.loads(
        requests.get(f"https://api.modrinth.com/v2/search?query={query}").text
    )
    for hit in res["hits"]:
        if props["mod_loader"].lower() in hit["categories"]:
            query_list.append([hit, f"{hit["title"]} --> {hit["description"]}"[:132]])

    if not query_list:
        print("Unable to find a mod with this name.")
        return

    mod_list = [
        inquirer.List(
            "selected_mod",
            message="Select the correct mod",
            choices=list(mod[1] for mod in query_list),
        )
    ]
    selected_mod = inquirer.prompt(mod_list)["selected_mod"]

    for query in query_list:
        if selected_mod == query[1]:
            mod = query[0]

    if props["version"] in mod["versions"]:
        print(f"The mod can be updated to {props["version"]}!")
    else:
        print(f"The mod cannot be updated to {props["version"]}.")

if __name__ == "__main__":
    search_mod({"mod_loader": "fabric", "version": "1.21.1"})
