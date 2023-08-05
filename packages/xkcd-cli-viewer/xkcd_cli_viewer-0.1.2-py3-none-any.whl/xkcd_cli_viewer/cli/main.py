from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from .comic import Comic
from .scraper import Scraper


def main():
    console = Console()
    while True:
        console.clear()
        command = Prompt.ask(
            '[italic]Enter a Comic ID, "latest" or a search term (leave blank if you\'re feeling lucky)[/italic]'
        )

        scraper = Scraper()
        comic = None
        if command == "latest":
            comic = scraper.get_latest()
        elif command.isdigit():
            id = int(command)
            comic = scraper.get_by_id(id)
        elif len(command) == 0:
            comic = scraper.get_random()
        else:
            comic_matches = scraper.search(command)
            console.print("")
            for i, match in enumerate(comic_matches):
                console.print(f"[{i}] {match}")

            console.print("")
            selected_comic_index = None
            while True:
                selected_comic_index = IntPrompt.ask("Select a comic", default=0)
                if 0 <= selected_comic_index <= 9:
                    break
                console.print("[red]Number must be between 0 and 9[/]")
            comic = scraper.get_by_exact_title(comic_matches[selected_comic_index])

        if not isinstance(comic, Comic):
            console.print("")
            console.print("[red]That comic couldn't be found.[/]")
            exit(1)

        while True:
            comic_time_alert = (
                " (Latest)"
                if comic.id == scraper.get_latest_id()
                else " (Oldest)"
                if comic.id == 1
                else ""
            )

            console.clear()
            console.print(f"[bold underline]{comic.title}[/]")
            console.print(
                f"[italic]ID {comic.id}{comic_time_alert} | Created {comic.date}[/]"
            )
            console.print(f"Hover Text: {comic.hover_text}")
            console.print(f"URL: {comic.page_url}")
            console.print("")

            choices = ["view", "next", "prev", "back", "exit"]
            if comic.id == scraper.get_latest_id():
                choices.remove("next")
            elif comic.id == 1:
                choices.remove("prev")

            command = Prompt.ask(
                "What would you like to do?",
                choices=choices,
                default="view",
            )

            if command == "view":
                comic.show()
            elif command == "next":
                comic = scraper.get_by_id(comic.id + 1)
                assert isinstance(comic, Comic)
            elif command == "prev":
                comic = scraper.get_by_id(comic.id - 1)
                assert isinstance(comic, Comic)
            elif command == "back":
                break
            elif command == "exit":
                exit(0)


if __name__ == "__main__":
    main()
