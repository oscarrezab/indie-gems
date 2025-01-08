''' 
Song Lyrics Scraper, a script to get song lyrics from a given csv file, such file must be in the format of thoese output
by spotify_scraper.py.
Notes: 
- Lyrics are obtained from AZLyrics, which retrieves them from MusicxMatch
- The Google search is not perfeclty formulated, some songs will not work, but this formulation is the one that works best after
running tests. Retrieved around 93% (506/546) of song lyrics for indie-test 1 and 2, combined.

Example usages
- For indie test: 
python3.12 scraping/lyrics_scraper.py -f res/indie-test-1.csv -o res/indie-test-1-lyrics.csv
- For indie test 2: 
python3.12 scraping/lyrics_scraper.py -f res/indie-test-2.csv -o res/indie-test-2-lyrics.csv
- For first-5 test:
python3.12 scraping/lyrics_scraper.py -f res/indie-test-2.csv -o indie-test-2-lyrics-first-five.csv

Created: January 2025 by Oscar Reza B.
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

import pandas as pd

import time
import argparse

def scraping(songname):
    chrome_service = Service(executable_path='/Users/oscarrezab/Downloads/chromedriver-mac-arm64/chromedriver')

    # Configure chrome options
    chrome_options = Options()
    chrome_options.page_load_strategy = "none"  # allow control over page loading, to stop loading that takes too long
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        # Go to Google
        driver.get("https://www.google.com")
        driver.maximize_window()

        # Look up the song lyrics
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(f"{songname} azlyrics")
        search_box.send_keys(Keys.ENTER)

        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='azlyrics']"))
        )

        time.sleep(2)  # arbitrary number, but website should be able to laod in 2s

        # Find results with relevant URLs
        results = driver.find_elements(By.CSS_SELECTOR, "a[href*='azlyrics.com/lyrics']")
        time.sleep(2)  # also arbitrary choice

        # Try to click the correct link and scrape lyrics
        lyrics = ""
        for result in results:
            if "translate.google.com" not in result.get_attribute("href"):
                result.click()
                time.sleep(4)  # Let the page partially load
                driver.execute_script("window.stop();")  # Stop further loading
                break

        try:
            # Scrape lyrics
            lyrics = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[5]").text
        except NoSuchElementException:
            print(f"Lyrics element not found on the page for {songname}")
            lyrics = "not found"

    except TimeoutException:
        print(f"Timeout while trying to load the page for {songname}")
        lyrics = ""
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        lyrics = "not found"
    finally:
        driver.quit()  # close browser even if an error occurs

    return lyrics

def get_song_names(csv_f):
    song_db = pd.read_csv(csv_f)
    pairs_list = []

    for title, artist in zip(song_db['title'], song_db['artist']):
        pairs_list.append(tuple([title, artist]))
    
    return pairs_list

def extract_song_lyrics(csv_f, output_f):
    all_data = []
    lyrs = []
    loaded_songs = get_song_names(csv_f)
    for title, artist in loaded_songs:
        print(f"Working on: {title} by {artist} \n")
        lyrs = scraping(f"{title} by {artist}")
        all_data.append({
        "title": title,
        "artist": artist,
        "lyrics": lyrs
        })

    # Create df and save as csv
    df = pd.DataFrame(data=all_data)
    df.to_csv(output_f, index=False)


if __name__ == "__main__":
    # Create and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input_file", help="Input CSV filepath")
    parser.add_argument("-o", "--output_file", help="Output CSV filepath")
    args = parser.parse_args()

    extract_song_lyrics(args.input_file, args.output_file)

    
