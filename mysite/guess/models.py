from django.db import models


class Game(models.Model):
    ongoing = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    guess_try = models.IntegerField()

    def __str__(self):
        return 'Game started {} with {} tries'#.format(str(self.date),str(self.guess_set.count()))

    def check_guess(self, guess):
        msg = False
        if guess:
            try:
                self.guess_set.create(guess=guess)
                if int(guess) < self.guess_try:
                    msg = 'Guess {} is too low'.format(str(guess))
                elif int(guess) > self.guess_try:
                    msg = 'Guess {} is too high'.format(str(guess))
                else:
                    msg = 'Congrats! {} is correct guess!\nYou used {} attempts!'#.format(str(guess),str(self.guess_set.count()))
                    self.ongoing = False
                    self.save()
            except:
                msg = 'Bad guess format!'
        return msg


class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guess = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - guess {} ({}) for game {}'#.format(str(self.guess),str(self.id),str(self.date),str(self.game.id))


