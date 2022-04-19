from django.shortcuts import render
import json
import urllib.request


#For uploading turtle graphics to webpage I used https://trinket.io/
#Link :- https://trinket.io/library/trinkets/b741024f65?go=1
def isslocation(request):
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    astronauts = result['number']
    context = {'astronauts': astronauts}
    return render(request, 'ISSLocation.html', context)
