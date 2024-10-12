import os
import inquirer
import requests
import json


class ImportMods:
    def __init__(self, props):
        self.props = props
        text_files = []
        for file in os.listdir("packs"):
            if file[-4:] == ".txt":
                text_files.append(file)
        if not text_files:
            print("There are no packs in this directory\n")
            return

        file_select = [
            inquirer.List(
                "file",
                message="What pack do you want to import?",
                choices=text_files,
            ),
        ]
        self.selected_file = os.path.join(
            "packs", f"{inquirer.prompt(file_select)["file"]}"
        )
        self.mod_list = []

        with open(self.selected_file, "r") as file:
            try:
                file_contents = file.readlines()
                if not file_contents:
                    print("The packs is empty\n")
                    return
                for mod_id in file_contents:
                    mod = json.loads(
                        requests.get(
                            f"https://api.modrinth.com/v2/project/{mod_id.strip()}"
                        ).text
                    )
                    self.mod_list.append(mod)
            except:
                print(
                    "There was an error in retrieving mods. Please check the pack file\n"
                )
                return
        print("Pack successfully imported.\n")

        choices = [
            inquirer.List(
                "choice",
                message="What do you want to do?",
                choices=[
                    "List",
                    "Append",
                    "Delete",
                    "Clear",
                    "Save",
                    "Delete Pack",
                    "Go Back",
                ],
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
                    if self.mod_list:
                        break
                case "Delete Pack":
                    os.remove(self.selected_file)
                    print("Pack successfully deleted\n")
                    break
                case "Go Back":
                    break

    def list_mods(self):
        if not self.mod_list:
            print("There are no mods in the pack\n")
            return

        for i in range(len(self.mod_list)):
            if self.props["version"] in self.mod_list[i]["game_versions"]:
                print(
                    f"{i + 1}. {self.mod_list[i]["title"]} --> can be updated to {self.props["version"]}"
                )
            else:
                print(
                    f"{i + 1}. {self.mod_list[i]["title"]} --> cannot be updated to {self.props["version"]}"
                )
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

        with open(self.selected_file, "w+") as file:
            for mod in self.mod_list:
                try:
                    file.write(f"{mod["id"]}\n")
                except:
                    file.write(f"{mod["project_id"]}\n")
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
    ImportMods(filters)
