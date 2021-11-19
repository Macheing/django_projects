#from django.shortcuts import render
from django.views import View
#from django.conf import settings
from django.http import HttpResponse

# Create your views here.

# session section view
def set_sessions(request):
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits
    if visits >= 5:
        del(request.session['visits'])

    response = HttpResponse("view count="+str(visits))
    return(response)

# cookie section view
def set_cookies(request):
    #print(request.COOKIES)
    response = HttpResponse(set_sessions(request))
    response.set_cookie('dj4e_cookie', '6afb69ea', max_age=1000)

    return response


#def set_cookies(request):
    # http response
#    response = HttpResponse('Practicing with cookies and sessions in django framework')
    # set cookie
#    response.set_cookie('dj4e_cookie', '6afb69ea', max_age=1000)
#    return (response)





