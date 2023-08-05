import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from .links import Links
from .comic import Comic
from random import choice
from thefuzz import process


class Scraper:
    archive_soup: BeautifulSoup

    def __init__(self) -> None:
        self.archive_soup = BeautifulSoup(
            requests.get(Links.archive()).content, "html.parser"
        )

    def search(self, term: str, limit=10):
        middle_container = self.archive_soup.find(id="middleContainer")
        assert isinstance(middle_container, Tag)

        comic_names = map(lambda link: link.text, middle_container.find_all("a"))
        return list(map(
            lambda match: match[0], process.extract(term, comic_names, limit=limit)
        ))

    def get_by_exact_title(self, title: str):
        middle_container = self.archive_soup.find(id="middleContainer")
        assert isinstance(middle_container, Tag)

        latest_link = middle_container.find("a", text=title)
        assert isinstance(latest_link, Tag)

        return self.get_from_archive_link(latest_link)

    def get_latest(self):
        middle_container = self.archive_soup.find(id="middleContainer")
        assert isinstance(middle_container, Tag)

        latest_link = middle_container.find_all("a")[0]
        assert isinstance(latest_link, Tag)

        return self.get_from_archive_link(latest_link)

    def get_latest_id(self):
        middle_container = self.archive_soup.find(id="middleContainer")
        assert isinstance(middle_container, Tag)

        latest_link = middle_container.find_all("a")[0]
        assert isinstance(latest_link, Tag)

        href = latest_link["href"]
        assert isinstance(href, str)

        return int(href.replace("/", ""))

    def get_random(self):
        middle_container = self.archive_soup.find(id="middleContainer")
        assert isinstance(middle_container, Tag)

        random_link = choice(middle_container.find_all("a"))
        assert isinstance(random_link, Tag)

        return self.get_from_archive_link(random_link)

    def get_by_id(self, id: int):
        comic_link = self.archive_soup.find("a", {"href": f"/{id}/"})
        if not isinstance(comic_link, Tag):
            return None

        return self.get_from_archive_link(comic_link)

    def get_from_archive_link(self, comic_link: Tag):
        date = comic_link["title"]
        assert isinstance(date, str)

        href = comic_link["href"]
        assert isinstance(href, str)

        title = comic_link.text
        id = int(href.replace("/", ""))

        comic_soup = BeautifulSoup(requests.get(Links.id(id)).content, "html.parser")

        middle_container = comic_soup.find(id="comic")
        assert isinstance(middle_container, Tag)

        latest_image = middle_container.find("img")
        assert isinstance(latest_image, Tag)

        hover_text = latest_image["title"]
        assert isinstance(hover_text, str)

        image_src = latest_image["src"]
        assert isinstance(image_src, str)

        image_url = "https:" + image_src
        assert isinstance(image_url, str)

        return Comic(id, date, title, hover_text, image_url, Links.id(id))
