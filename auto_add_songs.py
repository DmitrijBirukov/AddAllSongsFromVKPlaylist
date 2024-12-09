import json
import time
import random

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


MIN_SLEEP_DURATION = 1
MAX_SLEEP_DURATION = 3
OPTIONS_ARGS = ['--start-maximized', 
                '--incognito',
                '--disable-extensions',
                '--no-sandbox',
                '--disable-gpu',
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36']


def random_sleep() -> None:
    time.sleep(random.uniform(MIN_SLEEP_DURATION, MAX_SLEEP_DURATION))


def setup_driver(*args) -> WebDriver:
    """Initializes and configures the Selenium WebDriver with the provided Chrome options."""
    
    options = Options()
    for arg in args:
        options.add_argument(arg)
    
    driver = webdriver.Chrome(options=options)
    return driver

def login_vk(driver: WebDriver, phone: str, password: str) -> None:
    """Logs into the VKontakte website using the provided credentials. 
       
       Note:
           Currently not implemented
    """

    driver.get('https://vk.com')

    time.sleep(20)
    pass

def get_playlist(driver: WebDriver, playlist_url: str) -> WebElement:
    """Navigates to the specified playlist URL and retrieves the playlist element."""

    driver.get(playlist_url)
    
    time.sleep(15)

    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "audio_pl_snippet__list"))
    )

def get_songs_from_playlist(playlist: WebElement) -> list[WebElement]:
    """Extracts and returns a list of songs from the playlist."""

    return playlist.find_elements(By.CLASS_NAME, 'audio_row__inner')

def add_songs(driver: WebDriver, songs: list[WebElement]):
    """Iterates through the songs in the playlist and clicks the "add" button for each song."""

    actions = ActionChains(driver)
    count = 0
    n = len(songs)

    while n > 0:
        song = songs[count]
        actions.move_to_element(song).perform()

        random_sleep()

        try:
            button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "audio_row__action_add"))
            )
            button.click()
            print(f'Song №{count + 1} was succesfully added to your music')
            random_sleep()

        except Exception as e:
             print(f"Couldn't click add button: {e}")
             print(f"Song №{count + 1} wasn't added")
             continue
        
        finally:
            n -= 1
            count += 1


if __name__ == '__main__':
    with open('auto_add_config.json', encoding='utf-8') as file:
        config = json.load(file)
    driver = setup_driver(*OPTIONS_ARGS)
    
    login_vk(driver, config['phone'], config['password'])
    
    playlist = get_playlist(driver, config['playlist_url'])
    songs = get_songs_from_playlist(playlist)

    add_songs(driver, songs)


    driver.quit()
