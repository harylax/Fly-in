from enum import Enum


class Ansi(Enum):
    clear = "\033[2J\033[H"
    reset = "\033[0m"
    bold = "\033[1m"

    blue = "\033[94m"
    cyan = "\033[96m"
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"
    purple = "\033[95m"
    white = "\033[97m"


class Menu:
    def __init__(self) -> None:
        self.title: str = (
            "╔════════════════════════════════════════════════════╗\n"
            "║                                                    ║\n"
            "║    ███████╗██╗     ██╗   ██╗      ██╗███╗   ██╗    ║\n"
            "║    ██╔════╝██║     ╚██╗ ██╔╝      ██║████╗  ██║    ║\n"
            "║    █████╗  ██║      ╚████╔╝ █████╗██║██╔██╗ ██║    ║\n"
            "║    ██╔══╝  ██║       ╚██╔╝  ╚════╝██║██║╚██╗██║    ║\n"
            "║    ██║     ███████╗   ██║         ██║██║ ╚████║    ║\n"
            "║    ╚═╝     ╚══════╝   ╚═╝         ╚═╝╚═╝  ╚═══╝    ║\n"
            "║                                                    ║\n"
            "║                 42 Drone Simulation                ║\n"
            "╚════════════════════════════════════════════════════╝"
        )
        self.main_menu: str = (
            "[1] 🚀 Run default map\n\n"
            "[2] 🗺️ Choose map\n\n"
            "[3] 📂 Enter your existing map path\n\n"
            "[4] ❌ Quit\n\n"
            "──────────────────────────────────────────────────────\n"
        )
        self.difficulty: str = (
            "Choose difficulty\n\n"
            "\t[1] 🟢 Easy\n"
            "\t[1] 🟡 Medium\n"
            "\t[1] 🔴 Hard\n"
            "\t[1] 💀 Challenger\n"
            "\n\t[0] ← Back\n\n"
            "──────────────────────────────────────────────────────\n"
            "Choose > "
        )
        self.exit_message: str = (
            "══════════════════════════════════════════════════════\n\n"
            "\t   Thank you for using Fly-in 42\n\n"
            "\t\tHave a nice flight ✈\n\n"
            "\t\t      Bye bye!\n\n"
            "══════════════════════════════════════════════════════"
        )

    def home(self) -> int:
        print(Ansi.clear.value, end="")
        print(f"{Ansi.bold.value}{self.title}{Ansi.reset.value}")
        print(self.main_menu)
        print("Choose an option [1-4] > ", end="")
        try:
            return int(input())
        except ValueError:
            return -1


def main() -> None:
    menu = Menu()
    while True:
        x = menu.home()
        if x == 4:
            print(Ansi.clear.value, end="")
            print(menu.title)
            print(menu.exit_message)
            return


if __name__ == "__main__":
    main()
