from django.shortcuts import render

from .SongRecommender import SongRecommendation

def home_page(request):
    home = "hey, you have reached the home page!"
    return render(request, 'index.html', {'home_page': home})

def get_recommendations(request):
    recommendations = SongRecommendation(song_id=358)

    # Return the recommendations as a response
    return render(request, 'recommendations.html', {'recommendations': recommendations})
