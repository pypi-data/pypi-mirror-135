class Links:
    @staticmethod
    def latest():
        return "https://xkcd.com/"

    @staticmethod
    def archive():
        return "https://xkcd.com/archive/"

    @staticmethod
    def id(id: int):
        return f"https://xkcd.com/{id}/"
