from django.shortcuts import render, redirect, reverse
from django.views import View
from django.utils.html import escape

from .models import Game

import random


# the view for main page, name='guess:index'
def index(request):
    return render(request, 'guess/index.html')


# the view for game page, name='guess:next_try'
class TryView(View):

    # view function for GET method
    def get(self, request):

        # in case there is message saved in session (number was submitted and redirected from POST)
        # save msg into variable and delete it from session
        msg = request.session.get('msg', False)
        if msg:
            del request.session['msg']

        # in case there is no game_id saved in session (no ongoing game)
        # perfom actions to start a new game:
        game_id = request.session.get('game_id', False)
        if not game_id:
            # create new Game object and set a value to guess
            game = Game(guess_try = random.randint(0,500))
            # save Game object to database
            game.save()
            # save game_id to session
            request.session['game_id'] = game.id

        # in case the number is guessed (ongoing attribute is set to False)
        start_new = False
        game = Game.objects.get(id=request.session.get('game_id', False))
        if not game.ongoing:
            # delete previous game_id from session
            del request.session['game_id']
            # create a variable to inform template to set a page for congrats and
            # locate a link to start new game instead of form to submit a number
            start_new = True

        # session data just for debugging
        current_session = {}
        for key, value in request.session.items():
            current_session[escape(key)] = escape(value)

        # COOKIES values just for debugging
        current_cookies = {}
        for key, value in request.COOKIES.items():
            current_cookies[escape(key)] = escape(value)

        # render a response using a template
        # data:
        # sn - True if previous game ended and offer to start new one
        # message - message from redirected POST submit
        # cs - current session data
        # cc - current COOKIES data
        return render(request, 'guess/next_try.html', {'sn' : start_new, 'message' : msg, 'cs' : current_session, 'cc' : current_cookies})

    # view function for POST method
    # POST method is used if user submits guess number
    def post(self, request):

        # first, get guess number from POST data
        guess = request.POST.get('guess')

        # get game object using game_id from session
        game = Game.objects.get(id=request.session.get('game_id', False))

        # if game is found check the guess, save the result into session
        # and redirect browser to game page to use GET method
        if game:
            msg = game.check_guess(guess)
            request.session['msg'] = msg
            return redirect(request.path)

        # if game is not found redirect to the main (home) page
        else:
            return redirect(reverse('guess:index'))
