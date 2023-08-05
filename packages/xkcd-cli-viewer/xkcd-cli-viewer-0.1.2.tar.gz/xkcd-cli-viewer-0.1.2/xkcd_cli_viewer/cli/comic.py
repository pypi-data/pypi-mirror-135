from dataclasses import dataclass
import requests
from io import BytesIO
from PIL import Image


@dataclass
class Comic:
    id: int
    date: str
    title: str
    hover_text: str
    image_url: str
    page_url: str

    def show(self):
        image = requests.get(self.image_url).content
        Image.open(BytesIO(image)).show(self.title)
