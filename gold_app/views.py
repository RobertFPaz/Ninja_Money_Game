from django.shortcuts import render, redirect
import random, pytz
from datetime import datetime
from pytz import timezone
from django.contrib import messages



def index(request):
    if 'gold' not in request.session: 
        request.session['gold'] = 0
        request.session['activities'] = []
        request.session['count'] = 0
     #Checks if player won or lost the game.    
    if request.session['gold'] == 100 and request.session['count'] <= 10:
        request.session['gold'] = 0
        request.session['activities'] = []
        request.session['count'] = 0
        messages.success(request, 'Hooray! You did it!')
    elif request.session['gold'] != 100 and request.session['count'] >= 10:
        request.session['gold'] = 0
        request.session['activities'] = []
        request.session['count'] = 0
        messages.info(request, 'Too bad. Better luck next time.')
        
    return render(request, 'index.html')

def process_money(request):
    request.session['count'] += 1
    if request.method == "POST":
        if 'farm' in request.POST: 
            golds = round(random.random() * 10 + 10)
            request.session['location'] = 'farm'
        elif 'cave' in request.POST:
            golds = round(random.random() * 5 + 5)
            request.session['location'] = 'cave'
        elif 'house' in request.POST:
            request.session['location'] = 'house'
            golds = round(random.random() * 3 + 2)
        elif 'casino' in request.POST: 
            golds = round(random.random() * 100 - 50)
            request.session['location'] = 'casino'
        elif 'reset' in request.POST:
            request.session['gold'] = 0
            request.session['activities'] =[]
            request.session['count'] = 0
            return redirect('/')
        date_format = '%m/%d/%Y %H:%M:%S %Z'
        date = datetime.now(tz=pytz.utc)
        date = date.astimezone(timezone('US/Pacific'))
        my_time = date.strftime(date_format)
        
        location = request.session['location']
        
        if golds >= 0:
            request.session['gold'] += golds
            request.session['activities'].append(f"Earned {golds} gold from the {location}! " + my_time)
            
        else:
            request.session['gold'] += golds
            golds *= -1
            request.session['activities'].append(f"Entered a casino and lost {golds} golds! " + my_time)
            
    return redirect('/')

