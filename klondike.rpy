init python:

    class Klondike(object):

        def __init__(self, mcname=""):

            self.game = game = Game(mcname=mcname)

            self.player = {}
            self.bank = {}

            game.start()
            
        def show(self):
            self.game.show()

        def hide(self):
            self.game.hide()

        def interact(self):

            evt = ui.interact()

            return

        def hit(self):

            self.game.player_hit()

        def stand(self):

            self.game.player_stand()

        def double(self):

            self.game.player_double()

        def insurance(self):

            self.game.player_insure()

        def go(self):

            self.game.go()

        def giveUp(self):

            self.game.player_giveUp()
