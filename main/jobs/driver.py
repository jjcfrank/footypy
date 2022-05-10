#!/usr/bin/python3

import logging
import json, os, re, sys
from typing import Callable, Optional
from pandas import DataFrame

from requests import get

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = f"{project_dir}/logs/job-{os.path.basename(__file__)}.log"
LOG_FORMAT = f"%(asctime)s - LINE:%(lineno)d - %(name)s - %(levelname)s - %(funcName)s - %(message)s"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
# logger = logging.getLogger('py4j')

sys.path.insert(1, project_dir)
from classes import class_scraper

def main(project_dir:str) -> None:

    stats = match_stats(2021, "laliga")
    save_data(stats)
    # get_teams_names(2021, "laliga")
    # get_match_info(2021, "Sevilla")

def get_teams_names(season:int, league:str) -> list:
    return class_scraper.scraper_class().get_teams_names(season, league)

def get_match_info(season:int, team:str, ) -> DataFrame:
    return class_scraper.scraper_class().get_match_info(season, team)

def get_match_data(matchid:int, side:str) -> DataFrame:
    return class_scraper.scraper_class().get_match_data(matchid, side)

def match_stats(season:int, league:str) -> DataFrame:
    return class_scraper.scraper_class().match_stats(season, league)

def save_data(data:DataFrame) -> None:
    return class_scraper.scraper_class().save_data(data)

if __name__ == '__main__':
    main(project_dir)