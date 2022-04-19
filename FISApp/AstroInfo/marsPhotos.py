from datetime import datetime, timedelta
import requests
from django.shortcuts import render


def marsPhotos(request):
    date = datetime.today() - timedelta(days=7)
    date.strftime('%Y-%m-%d')
    url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=' + (str)(
        date) + '=2015-6-3&api_key=q85qDjg2dRNIebCwToX523S7jqmrfZYcDrnQCZzk'
    response = requests.get(url).json()
    # print(response['photos'][2]['name'])
    images = response['photos']
    size = len(images)
    nasa_photos = []
    # if (size >= 10):
    #     for i in range(10):
    #         nasa_photos.append(images[i]['img_src'])
    # else:
    for i in range(size):
        nasa_photos.append(images[i]['img_src'])
    return render(request, 'marsPhotos.html', {'nasa_photos': nasa_photos})
