from django.db import models


# class to save a single game
class Game(models.Model):
    # True if the game is active, not ended
    ongoing = models.BooleanField(default=True)
    # date game started
    date = models.DateTimeField(auto_now=True)
    # correct number to guess
    guess_try = models.IntegerField()

    # string representation for a game
    def __str__(self):
        return 'Game started {} with {} tries'.format(
            str(self.date),
            str(self.guess_set.count())
        )

    # function to check guess number
    # returns a message to present on the page
    def check_guess(self, guess):
        msg = False
        if guess:
            try:
                # in case the guess is correct
                int_guess = int(guess)

            # in case the guess is not correct
            except:
                msg = 'Bad guess format!'

            # handle guess if it is correct
            else:
                if int_guess < self.guess_try:
                    msg = 'Guess {} is too low'.format(str(guess))
                elif int_guess > self.guess_try:
                    msg = 'Guess {} is too high'.format(str(guess))
                else:
                    msg = 'Congrats! {} is correct!/n You used {} attempts!'.format(
                        guess,
                        str(self.guess_set.count())
                    )

                    # set ongoing attribute to False (game ended) and save to database
                    self.ongoing = False
                    self.save()

                # create a guess object for current guess
                self.guess_set.create(guess=guess, message=msg)

        return msg


# class to save a single guess
class Guess(models.Model):
    # game object related to this guess
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # guess number
    guess = models.IntegerField()
    # date a guess was submitted
    date = models.DateTimeField(auto_now=True)
    # message displayed for your guess
    message = models.CharField(max_length=80, default='')

    # string representation for a single guess
    def __str__(self):
        return '{} - guess on {} - {}'.format(
            str(self.guess),
            str(self.date.strftime('%Y-%m-%d %H:%M')),
            self.message
        )


