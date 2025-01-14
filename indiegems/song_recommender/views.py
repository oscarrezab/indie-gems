from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd

from .Song import Song
from .SongRecommender import SongRecommendation

# Create your views here.
def get_recommendations(request):
    recommendations = SongRecommendation(song_id=358)

    # Return the recommendations as a response
    return render(request, 'recommendations.html', {'recommendations': recommendations})