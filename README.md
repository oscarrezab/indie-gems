# Indie Gems
Get indie song recommendations, because the ones in our music players are not too good!

## How does this work?
The idea is to recommend songs that sound similar, so rhythmic and tonality factors should play an important role in suggesting similar songs. With this in mind, each recommendation is based on similarities between the BPM (beats per minute), the Camelot value (which is related to musical key), and the lyrics of two songs.

## About the scraped data
Tools for scraping the web are stored in the `scraping` directory. 
* `spotify_scraper.py` will take in a command-line argument with a url to a Spotify playlist. This script is no longer necessary as we can easily download a playlist as a csv from Chosic, so a nice change would be to automate this.
* `lyrics_scraper.py` looks for lyrics of the songs in AZLyrics. It starts the search in Google, which brings problems if the lyrics for the song are not present within the first results. A solution would be to automate the search within the AZLyrics website.
* `table_merger.py` puts together the lyric information with the other data from Chosic or the Spotify scraper.

## About lyric vectorization
Tools used for lyric vectorization are stored in the `lyrics` directory.
* `lyrics_preprocessing.py` uses NLTK to put lyrics in lowercase and remove special characters
* `lyrics_vectorization.py` takes in the pre-processed lyrics and puts them in a vector form. This vector is formed by extracting the final classification of DistilBERT from HuggingFace and using it to extract features from the lyrics.

## Current plans for improvement
* Improve the comparison of song lyrics. Currently, the vanilla version of DistilBERT is used for producing vector embeddings for the lyrics. The computed Pearson correlations lie mostly around 90-95%, such lack of significant differences makes the computation of similarity scores unreliable. The first ideas are to fine-tune the model with a dataset specific to text comparison, remove stop words ('the', 'is', 'it'...), or simply use a different model that was trained specifically for comparing texts.
* Update scraping scripts for a straightforward method of increasing the dataset.
* Refactor code to retrieve data from the SQLite table to avoid dependency on pkl and csv files
* Add functionality to customize weight given to each similarity score 
* Handle 'fuzzy' search to account for typos or other factors that may make a text input different to the values stored in the dataset.