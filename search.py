import requests
import json
import inquirer


def search_mod(props):
    query_list = []
    query = inquirer.prompt([inquirer.Text("query", message="Enter name of the mod")])[
        "query"
    ]
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
        print(f"The mod can be updated to {props["version"]}!\n")
    else:
        print(f"The mod cannot be updated to {props["version"]}.\n")


if __name__ == "__main__":
    filter_questions = [
        inquirer.List(
            "mod_loader",
            message="Which mod loader do you want to use?",
            choices=["Forge", "Fabric", "Quilt"],
        ),
        inquirer.List(
            "version",
            message="Which version of minecraft do you want to use?",
            choices=["1.21.1", "1.21", "1.20.6"],
        ),
    ]
    filters = inquirer.prompt(filter_questions)
    search_mod(filters)
