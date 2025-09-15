from __future__ import annotations
import contextlib
import logging
from typing import Optional, List


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from .config import DEFAULT_HEADLESS, DEFAULT_WAIT_SECONDS, BASE_URL


logger = logging.getLogger(__name__)


class SeleniumScraper:
"""Hermetyzacja sterownika Selenium jako kontekst menedżer.


Przykład:
with SeleniumScraper() as s:
html = s.get_html(url)
"""


def __init__(self, headless: bool = DEFAULT_HEADLESS, wait_seconds: int = DEFAULT_WAIT_SECONDS):
self._headless = headless
self._wait_seconds = wait_seconds
self.driver: Optional[webdriver.Chrome] = None


def __enter__(self) -> "SeleniumScraper":
options = Options()
if self._headless:
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
self.driver = webdriver.Chrome(options=options)
return self


def __exit__(self, exc_type, exc, tb) -> None:
with contextlib.suppress(Exception):
if self.driver:
self.driver.quit()


def get_html(self, url: str, wait_xpath: str = '//script[contains(text(), "matchCentreData")]') -> str:
assert self.driver, "Driver not initialized. Use as a context manager."
self.driver.get(url)
WebDriverWait(self.driver, self._wait_seconds).until(
EC.presence_of_element_located((By.XPATH, wait_xpath))
)
return self.driver.page_source


def find_live_match_urls(self, team_fixtures_url: str) -> List[str]:
html = self.get_html(team_fixtures_url, wait_xpath='//a[contains(@href, "/live/")]')
soup = BeautifulSoup(html, 'html.parser')
anchors = soup.select('a[href*="/live/"]')
urls = sorted(set(f"{BASE_URL}{a['href']}" for a in anchors if a.has_attr('href')))
logger.info("Znaleziono %d url-i live", len(urls))
return urls