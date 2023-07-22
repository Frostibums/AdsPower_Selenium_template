import random
import sys
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from consts import *  # local_link (http://localhost:50325 or http://local.adspower.com:50325) and whatever you need

profile_ids: list[str] = []  # ads profile ids ['id_1', 'id_2', ...]


class Profile(webdriver.Chrome):
    def __init__(self, user_id: str):
        self.user_id = user_id
        chrome_service, chrome_options = self._get_service_and_options()
        super().__init__(service=chrome_service, options=chrome_options)

    def _open_profile(self) -> dict:
        addy = f'{local_link}/api/v1/browser/start?user_id={self.user_id}'
        res = requests.get(addy).json()

        if res.get('code') != 0:
            print(res["msg"])
            print("please check ads_id")
            sys.exit()

        return res

    def _get_service_and_options(self) -> (Service, Options):
        res = self._open_profile()
        chrome_driver = res["data"]["webdriver"]
        chrome_service = Service(executable_path=chrome_driver)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", res["data"]["ws"]["selenium"])

        return chrome_service, chrome_options

    def close_profile(self) -> bool:
        self.quit()
        res = requests.get(f'{local_link}/api/v1/browser/stop?user_id={self.user_id}').json()
        if res.get('code') == -1:
            return False
        return True


if __name__ == '__main__':

    for profile_id in profile_ids:
        profile = Profile(profile_id)
        profile.get('https://github.com/FrostiBums')
        profile.close_profile()
