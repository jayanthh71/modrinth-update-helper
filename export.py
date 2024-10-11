import inquirer
import json
import requests


class ExportMods:
    def __init__(self, props):
        self.mod_list = []
        self.props = props
        self.name = inquirer.prompt(
            [inquirer.Text("name", message="Enter name of the pack")]
        )["name"]
        print()
        choices = [
            inquirer.List(
                "choice",
                message="What do you want to do?",
                choices=["List", "Append", "Delete", "Clear", "Save", "Go Back"],
            ),
        ]
        while True:
            selected_mod = inquirer.prompt(choices)
            match selected_mod["choice"]:
                case "List":
                    self.list_mods()
                case "Append":
                    self.append_mod()
                case "Delete":
                    self.delete_mod()
                case "Clear":
                    self.clear_mods()
                case "Save":
                    self.save_mods()
                    break
                case "Go Back":
                    break

    def list_mods(self):
        if not self.mod_list:
            print("There are no mods in the pack\n")
            return

        for i in range(len(self.mod_list)):
            print(f"{i + 1}. {self.mod_list[i]["title"]}")
        print(f"\n{len(self.mod_list)} mods in pack\n")
        return

    def append_mod(self):
        query_list = []
        query = inquirer.prompt(
            [inquirer.Text("name", message="Enter name of the mod")]
        )["name"]
        print()
        res = json.loads(
            requests.get(f"https://api.modrinth.com/v2/search?query={query}").text
        )
        for hit in res["hits"]:
            if self.props["mod_loader"].lower() in hit["categories"]:
                query_list.append(
                    [hit, f"{hit["title"]} --> {hit["description"]}"[:132]]
                )

        if not query_list:
            print("Unable to find a mod with this name.\n")
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

        self.mod_list.append(mod)
        print(f"{mod["title"]} successfully added\n")
        return

    def delete_mod(self):
        print()
        if not self.mod_list:
            print("There are no mods in the pack\n")
            return

        query_list = []
        for mod in self.mod_list:
            query_list.append([mod, f"{mod["title"]} --> {mod["description"]}"[:132]])

        mod_list = [
            inquirer.List(
                "selected_mod",
                message="Select the mod to be deleted",
                choices=list(mod[1] for mod in query_list),
            )
        ]
        selected_mod = inquirer.prompt(mod_list)["selected_mod"]

        for query in query_list:
            if selected_mod == query[1]:
                mod = query[0]

        self.mod_list.remove(mod)
        print(f"{mod["title"]} successfully removed\n")
        return

    def clear_mods(self):
        self.mod_list = []
        print("Mod list cleared\n")

    def save_mods(self):
        if not self.mod_list:
            print("There are no mods in the pack\n")
            return

        with open(f"{self.name}.txt", "w") as file:
            for mod in self.mod_list:
                file.write(mod["project_id"])
        print("Pack successfully saved\n")


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
    ExportMods(filters)
