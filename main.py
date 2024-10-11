import inquirer
from search import search_mod
from export import ExportMods


def main(props):
    choices = [
        inquirer.List(
            "choice",
            message="What would you like to do?",
            choices=["Search", "Import", "Export", "Exit"],
        )
    ]

    while True:
        choice = inquirer.prompt(choices)
        match choice["choice"]:
            case "Search":
                search_mod(props)
            case "Import":
                pass
            case "Export":
                ExportMods(props)
            case "Exit":
                exit()


if __name__ == "__main__":
    print("Tool for verifing if mods can be updated to latest versions\n")

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
    main(filters)
