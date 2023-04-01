import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Show:
    def __init__(self, url):
        self.url = url
        self.show_name = self.get_showname()
        self.last_season = self.get_last_season()

    def get_dict(self):
        df = pd.DataFrame()
        try:
            for season in range(int(self.last_season)):
                ratings = self.get_ratings((season+1))
                mask = pd.DataFrame.from_dict(ratings)
                df = pd.concat([df, mask], axis=1)

        except IndexError:
            print("Not a serie")

        return df

    def get_showname(self):
        webpage = self.__get_webpage(self.url)
        title = webpage.title
        show_name = re.findall("(?<=>)(.*?)(?=\()", str(title))
        return show_name[0]

    def get_last_season(self):
        splt = self.url.split("/")
        splt[-1] = "episodes/?ref_=tt_ov_epl"
        episode_url = "/".join(splt)

        episode_webpage = self.__get_webpage(episode_url)

        season = re.findall("Season [0-9]+", str(episode_webpage.title))

        return season[0].split()[-1]

    def get_ratings(self, season_num):
        lst = []
        season_with_rating = {}
        season_url = self.__parse_seasons_url(season_num)
        season_webpage = self.__get_webpage(season_url)

        # get the ratings
        ratings = season_webpage.body.find_all("span", class_="ipl-rating-star__rating")
        for rate in ratings:
            rating = re.findall("[0-9]+.[0-9]", str(rate))
            if rating:
                lst.append(rating[0])

        # get the season
        season = re.findall("Season [0-9]+", str(season_webpage.title))
        season_with_rating[season[0]] = lst

        return season_with_rating

    def __parse_seasons_url(self, season_num):
        splt = self.url.split("/")
        splt[-1] = f"episodes?season={season_num}"
        episode_url = "/".join(splt)

        return episode_url

    def __get_webpage(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 '
                                 'Safari/537.36'}

        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.content, "html.parser")
        return soup
