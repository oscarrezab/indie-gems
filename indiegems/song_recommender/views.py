from django.shortcuts import render

from .SongRecommender import SongRecommendation

def home_page(request):
    home = "hey, you have reached the home page!"
    return render(request, 'index.html', {'home_page': home})

def recommendations_view(request):
    recommendations = None
    form_submitted = False
    if request.method == "POST":
        form_submitted = True
        song_id = request.POST.get('song_id')
        if song_id:
            recommendations = get_recommendations(song_id) 

    return render(request, 'recommendations.html', {'recommendations': recommendations, 'form_submitted': form_submitted})

def get_recommendations(id):
    return SongRecommendation(int(id))
