from django.shortcuts import render, redirect, reverse
from django.views import View
from django.utils.html import escape

from .models import Game

import random


def index(request):
    return render(request, 'guess/index.html')


class TryView(View):

    def get(self, request):
        msg = request.session.get('msg', False)
        if msg:
            del request.session['msg']

        game_id = request.session.get('game_id', False)
        if not game_id:
            game = Game(guess_try = random.randint(0,500))
            game.save()
            request.session['game_id'] = game.id

        start_new = False
        game = Game.objects.get(id=request.session.get('game_id', False))
        if not game.ongoing:
            del request.session['game_id']
            start_new = True

        current_session = {}
        for key, value in request.session.items():
            current_session[escape(key)] = escape(value)

        current_cookies = {}
        for key, value in request.COOKIES.items():
            current_cookies[escape(key)] = escape(value)

        return render(request, 'guess/next_try.html', {'sn' : start_new, 'message' : msg, 'cs' : current_session, 'cc' : current_cookies})


    def post(self, request):
        guess = request.POST.get('guess')
        game = Game.objects.get(id=request.session.get('game_id', False))
        if game:
            msg = game.check_guess(guess)
            request.session['msg'] = msg
            return redirect(request.path)
        else:
            return redirect(reverse('guess:index'))
