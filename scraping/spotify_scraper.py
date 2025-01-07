''' 
Spotify Playlist Scraper, a script to get song information from a Spotify Playlist and save it onto a csv file.
Note: some code was re-purposed from https://github.com/lixx21/spotify-scrapping

Example usages
- For indie test: 
python3.12 scraping/spotify_scraper.py -u https://open.spotify.com/playlist/3XEAOR628UeeD8HVqKXjxR -o res/indie-test-1.csv
- For indie test 2: 
python3.12 scraping/spotify_scraper.py -u https://open.spotify.com/playlist/73VF6vqOuYup3CdDjmUunN -o res/indie-test-2.csv

Created: January 2025 by Oscar Reza B.
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import argparse

import pandas as pd

def scraping(spotify_playlist_url, output_csv):
    chrome_service = Service(executable_path='/Users/oscarrezab/Downloads/chromedriver-mac-arm64/chromedriver')
    driver = webdriver.Chrome(service=chrome_service)

    # Go to the playlist
    driver.get(spotify_playlist_url)
    driver.maximize_window()

    time.sleep(2)  # let the page load
    body = driver.find_element(By.TAG_NAME, 'body')  # click <body> to focus on browser
    body.click()  # ensures the page has focus

    # Initiate list for storing data
    all_data = []

    # Get number of songs
    num_songs = int(driver.find_element(By.XPATH, '//span[@class="encore-text encore-text-body-small encore-internal-color-text-subdued w1TBi3o5CTM7zW1EB3Bm"]').text.split()[0])
    print(f"Playlist contains {num_songs} songs")

    for _ in range(10):  # scroll down 10 times (should be enough for a playlist of 300 songs)
        for _ in range(40):  # chose 40 because it is enough to going down about 25 songs
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(1)  # allow time for new content to load

        # Scrape data after scrolling
        titles = driver.find_elements(By.XPATH, '//div[@class="encore-text encore-text-body-medium encore-internal-color-text-base btE2c3IKaOXZ4VNAb8WQ standalone-ellipsis-one-line"]')
        artists = driver.find_elements(By.XPATH, '//span[@class="encore-text encore-text-body-small encore-internal-color-text-subdued UudGCx16EmBkuFPllvss standalone-ellipsis-one-line"]')
        albums = driver.find_elements(By.XPATH, '//span[@class="encore-text encore-text-body-small"]')
        durations = driver.find_elements(By.XPATH, '//div[@class="encore-text encore-text-body-small encore-internal-color-text-subdued l5CmSxiQaap8rWOOpEpk"]')
        songs_img = driver.find_elements(By.XPATH, '//img[@class="mMx2LUixlnN_Fu45JpFB IqDKYprOtD_EJR1WClPv Yn2Ei5QZn19gria6LjZj"]')

        # Iterate through elements and append to data list
        for index in range(len(titles)):
            try:
                all_data.append({
                    "title": titles[index].text,
                    "artist": artists[index].text if index < len(artists) else "",
                    "album": albums[index].text if index < len(albums) else "",
                    "duration": durations[index].text if index < len(durations) else "",
                    "album_image": songs_img[index].get_attribute('src') if index < len(songs_img) else "",
                })
            except Exception as e:
                print(f"Error processing item {index}: {e}")

    driver.quit()

    # Remove duplicates
    unique_data = {entry['title']: entry for entry in all_data}.values()

    # Put data into dataframe
    df = pd.DataFrame(data=unique_data)
    # Remove songs outside of playlist bounds
    df.drop(df.tail(len(df.index) - num_songs).index,
        inplace = True)
    # save as csv
    df.to_csv(output_csv, index=False)

    print(f"Data has been saved in {output_csv}")
    print(f"Successfylly scraped {len(df.index)} songs")


if __name__ == "__main__":
    # Create and parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Spotify playlist URL")
    parser.add_argument("-o", "--output", help="Output CSV filepath")
    args = parser.parse_args()

    # Call the scraping function
    scraping(args.url, args.output)
