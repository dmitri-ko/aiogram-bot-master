
from data.config import FOOTBALL_API_KEY
from datetime import datetime
import json
import logging
from typing import Any, Dict, List
import requests
from .matchday import MatchDay, Match
from .standings_data import Position, Standings


class EFLData:
    _BASE_URL: str = "http://api.football-data.org"
    _API_VERSION: str = "v2"
    _COMPETITION_ID: str = "ELC"

    def __init__(self) -> None:
        try:
            competition_info: Any = self.get_competition()
            self.data: Dict = {}
            self.name = competition_info.get("name")
            self.match_day = int(competition_info.get("currentSeason").get(
                "currentMatchday"
            ))
            self.start_date = datetime.strptime(
                competition_info.get("currentSeason").get(
                    "startDate"), "%Y-%m-%d"
            ).strftime("%d.%m.%Y")
            self.end_date = datetime.strptime(
                competition_info.get("currentSeason").get(
                    "endDate"), "%Y-%m-%d"
            ).strftime("%d.%m.%Y")
            self.season_year = int(self.start_date[-4:])
        except Exception as e:
            logging.exception(f"Error during object init {repr(e)}")

    def get_data(self, uri: str, filters: Dict[str, str] = {}) -> Any:
        """Get data from API

        Args:
            uri (str): URI string of API
            filters (Dict[str, str], optional): filter to apply. Defaults to {}.

        Returns:
            Any: result formatted as json string 
        """
        return json.loads(
            requests.get(
                uri,
                headers={"X-Auth-Token": FOOTBALL_API_KEY},
                params=filters,
            ).text
        )

    def get_competition(self) -> Any:
        """Get competition object

        Returns:
            Any: competition object formatted as json string
        """
        URI = (
            f"{self._BASE_URL}/{self._API_VERSION}/competitions/{self._COMPETITION_ID}"
        )
        return self.get_data(URI)

    def get_standings(self, standins_type: str = "TOTAL") -> Standings:
        """Get standings object

        Args:
            standins_type (str, optional): standing type filters. List of valid types is ["TOTAL", "HOME", "AWAY"]. Defaults to "TOTAL".

        Returns:
            Any: standings object formatted as json string
        """
        PROMOTION_ZONE:int = 2
        PLAYOFF_ZONE:int = 6
        RELEGATION_ZONE:int = 22
        
        accepted_types: List[str] = ["TOTAL", "HOME", "AWAY"]
        filter_value: str = "TOTAL"
        if standins_type in accepted_types:
            filter_value = standins_type

        filter: Dict[str, str] = {"standingType": filter_value}
        URI: str = f"{self._BASE_URL}/{self._API_VERSION}/competitions/{self._COMPETITION_ID}/standings"
        try:
            raw_data: Dict = self.get_data(uri=URI, filters=filter)
            standings: Standings = Standings(
                last_updated=raw_data.get("competition").get("lastUpdated"),
                table=[ 
                         Position(
                             position=pos.get("position"),
                             team=pos.get("team").get("name"),
                             games=pos.get("playedGames"),
                             won=pos.get("won"),
                             draw=pos.get("draw"),
                             lost=pos.get("lost"),
                             goals_for=pos.get("goalsFor"),
                             goals_against=pos.get("goalsAgainst"),
                             points=pos.get("points"),
                             zone="promotion" if int(pos.get("position")) <= PROMOTION_ZONE else "playoff" if int(pos.get("position")) <= PLAYOFF_ZONE else "relegation" if int(pos.get("position")) >= RELEGATION_ZONE else ""
                         ) for pos in raw_data.get("standings")[0].get("table")
                       ] 
            )
            return standings
        except Exception as e:
            logging.e(e)
            return None
        

    def get_matches(self, matchday: int) -> MatchDay:
        """Get match object

        Args:
            matchday (int): matchday match for results

        Returns:
            Any: match object formatted as json string
        """
        filter: Dict[str, str] = {}
        try:
            if matchday <= self.match_day:
                filter["matchday"] = matchday
            filter["status"] = "FINISHED"

            URI: str = f"{self._BASE_URL}/{self._API_VERSION}/competitions/{self._COMPETITION_ID}/matches"
            matchday_list: List[Any] = self.get_data(uri=URI, filters=filter)
            matchday_cls: MatchDay = MatchDay(games=[
                Match(home_team=match.get("homeTeam").get("name"), 
                      away_team=match.get("awayTeam").get("name"), 
                      home_goals=match.get("score").get("fullTime").get("homeTeam"),
                      away_goals=match.get("score").get("fullTime").get("awayTeam")
                      ) for match in matchday_list.get("matches")
            ])
            return matchday_cls
        except TypeError as e:
            logging.exception(e)
            return None

    @property
    def name(self) -> str:
        """Competition name property

        Returns:
            str: name of competition
        """
        return self.data.get("name")

    @name.setter
    def name(self, name: str) -> None:
        """Competition name setter

        Args:
            name (str): [name of competition
        """
        self.data["name"] = name

    @property
    def season_year(self) -> int:
        """Season year property

        Returns:
            int: year of the season
        """
        return self.data.get("year")

    @season_year.setter
    def season_year(self, year: int) -> None:
        """Season year setter

        Args:
            year (int): year of the season
        """
        self.data["year"] = year

    @property
    def start_date(self) -> str:
        """ Start date property

        Returns:
            str: season start date
        """
        return self.data.get("startDate")

    @start_date.setter
    def start_date(self, start_date: str) -> None:
        """Start date setter

        Args:
            start_date (str): season start date
        """
        self.data["startDate"] = start_date

    @property
    def end_date(self) -> str:
        """End date property

        Returns:
            str: season end date
        """
        return self.data.get("endDate")

    @end_date.setter
    def end_date(self, end_date: str) -> None:
        """End date setter

        Args:
            end_date (str): season end date
        """
        self.data["endDate"] = end_date

    @property
    def match_day(self) -> int:
        """Match day property

        Returns:
            int: match day
        """
        return self.data.get("currentMatchday")

    @match_day.setter
    def match_day(self, match_day: int) -> None:
        """Match day setter

        Args:
            match_day (int): match day
        """
        self.data["currentMatchday"] = match_day


di = EFLData()
