from django.shortcuts import render
import pandas as pd

from .SongRecommender import SongRecommendation

def home_page(request):
    home = ""
    return render(request, 'index.html', {'home_page': home})

def recommendations_view(request):
    song_titles_map = get_all_song_titles()
    recommendations = None
    form_submitted = False

    if request.method == "POST":
        form_submitted = True
        song_title = request.POST.get('song_title')
        bpm_weight = request.POST.get('bpm_slider')
        key_weight = request.POST.get('key_slider')
        lyrics_weight = request.POST.get('lyrics_slider')

        try:
            if song_title:
                recommendations = get_recommendations(song_titles_map[song_title], bpm_weight, key_weight, lyrics_weight) 
        except Exception:
            return render(request, 'recommendations.html', {'invalid_title': "invalid", 'form_submitted': form_submitted,})


    return render(request, 'recommendations.html', {'recommendations': recommendations, 'form_submitted': form_submitted, 'all_song_titles': song_titles_map})

def get_recommendations(id, bpm_weight, key_weight, lyrics_weight):
    return SongRecommendation(int(id), float(bpm_weight), float(key_weight), float(lyrics_weight))

def get_all_song_titles():
    recommender = SongRecommendation(-1)
    return recommender.get_all_songs_and_ids()
