from django.shortcuts import render, redirect
from django.views import View


def index(request):
    return render(request, 'guess/index.html')


def check_guess(guess):
    msg = False
    if guess:
        try:
            if int(guess) < 144:
                msg = 'Guess is too low'
            elif int(guess) > 144:
                msg = 'Guess is too high'
            else:
                msg = 'Congrats!'
        except:
            msg = 'Bad guess format!'
    return msg


class TryView(View):

    def get(self, request):
        msg = request.session.get('msg', False)
        if msg:
            del request.session['msg']
        return render(request, 'guess/next_try.html', {'message' : msg})

    def post(self, request):
        guess = request.POST.get('guess')
        msg = check_guess(guess)
        request.session['msg'] = msg
        return redirect(request.path)
