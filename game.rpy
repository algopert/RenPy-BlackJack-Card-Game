init python:

    import pygame
    import math

    deckNumber = 6

    LEFT=450

    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    clock = pygame.time.Clock()

    messages = {
        "bet": "Bet !",
        "win": "You win !",
        "draw": "Draw !",
        "lose": "Dealer wins",
        "pass": "Pass !",
        "warning": {
            "bet": { "msg": "You need to bet first", "x": 900 },
            "insurance": { "msg": "You can not use insurance", "x": 900 },
            "insured": { "msg": "insurance used !", "x": 900 },
            "double": { "msg": "You can not double now", "x": 900 },
            "funds": { "msg": "You haven't got enough funds", "x": 900 },
            "hit": { "msg": "You can not hit anymore", "x": 900 },
            "doubled": { "msg": "Bet doubled !", "x": 900 },
            "giveUp": { "msg": "You can not give up now !", "x": 900 },
            "gaveUp": { "msg": "You gave up", "x": 900 },
        }
    }

    chipsValue = {
        "blue": 500,
        "black": 100,
        "green": 25,
        "red": 5,
        "white": 1
    }

    def rand(min, max):
        return renpy.random.randint(min, max)

    class Game(renpy.Displayable):

        def __init__(self, mcname="", **kwargs):

            renpy.Displayable.__init__(self, **kwargs)
          
            self.chipImgs = {
                "blue": Transform("assets/PNG/Chips/chipBlueWhite_side.png"),
                "black": Transform("assets/PNG/Chips/chipBlackWhite_side.png"),
                "green": Transform("assets/PNG/Chips/chipGreenWhite_side.png"),
                "red": Transform("assets/PNG/Chips/chipRedWhite_side.png"),
                "white": Transform("assets/PNG/Chips/chipWhiteBlue_side.png")
            }

            self.clock = pygame.time.Clock()

            self.mcname = mcname

            self.player = {
                "deck": [],
                "name": {
                    "value": mcname,
                    "text": False,
                },
                "cardsContainer": False,
                "chipsContainer": False,
                "blackjack": False,
                "insurance": False,
                "doubled": False,
                "funds": 1000,
                "betted": False,
                "dealt": 0,
                "chips": self.balanceChips(1000),
                "render_chips": {
                    "blue": [],
                    "black": [],
                    "green": [],
                    "red": [],
                    "white": []
                }
            }

            self.bank = {
                "deck": [],
                "cardsContainer": False,
                "blackjack": False
            }

            self.deck = []
            self.chipsValue = {
                "blue": 500,
                "black": 100,
                "green": 25,
                "red": 5,
                "white": 1
            }
            self.startContainer = False
            self.buttonContainer = False
            self.dealtChipContainer = False
            self.inProgress = False
            self.dealt = {
                "blue": 0,
                "black": 0,
                "green": 0,
                "red": 0,
                "white": 0
            }

            self.render_chips = {
                "blue": [],
                "black": [],
                "green": [],
                "red": [],
                "white": []
            }

            self.message = {
                "text": "",
                "xoffset": 0,
                "yoffset": 0,
                "show": False
            }

            self._alert_message = {
                "text": "",
                "xoffset": 0,
                "yoffset": 0,
                "show": False
            }

            self.chips_over = {
                "blue": False,
                "black": False,
                "green": False,
                "red": False,
                "white": False
            }

            self.render_cards = []

            self.animate_text = {
                "text": 'animate',
                "x": 0,
                "y": 0
            }

        def show(self, layer='master'):

            ui.layer(layer)
            ui.add(self)
            ui.close()

        def hide(self, layer='master'):

            ui.layer(layer)
            ui.remove(self)
            ui.close()

        def render(self, width, height, st, at):

            rv = renpy.Render(width, height)

            text = Text(self.mcname, color="#ffffff", size=30)
            text_render = renpy.render(text, 0, 0, 0, 0)
            rv.blit(text_render, (260, 35))

            text = Text(str(self.player["funds"]), color="#ffffff", size=26)
            text_render = renpy.render(text, 0, 0, 0, 0)
            rv.blit(text_render, (710, 640))

            self.chips_render_to(rv, width, height, st, at)

            if (self.message["show"]):
                text = Text(self.message["text"], color="#ffffff", size=40)
                text_render = renpy.render(text, 300, 0, 0, 0)
                rv.blit(text_render, (self.message["xoffset"], self.message["yoffset"]))

            for card in self.render_cards:
                card.render_to(rv, width, height, st, at)

            if (self._alert_message["show"]):
                text = Text(self._alert_message["text"], color="#ffa500", size=30)
                text_render = renpy.render(text, 400, 0, 0, 0)
                rv.blit(text_render, (self._alert_message["xoffset"], self._alert_message["yoffset"]))

            return rv

        def event(self, ev, x, y, st):
            
            for chip_key in self.player["render_chips"].keys():
                last_chip_offset = None
                if len(self.player["render_chips"][chip_key]) > 0:
                    last_chip_offset = self.player["render_chips"][chip_key][len(self.player["render_chips"][chip_key]) - 1]
                if not last_chip_offset:
                    continue
                chip_inner_position = x > last_chip_offset["xoffset"] and (x < last_chip_offset["xoffset"] + 68) and y > last_chip_offset["yoffset"] - 10 and (y < last_chip_offset["yoffset"] + 48)

                if chip_inner_position and not self.chips_over[chip_key]:
                    
                    last_chip_offset["yoffset"] -= 8
                    self.chips_over[chip_key] = True
                    renpy.redraw(self, 0)
                    
                elif not chip_inner_position and self.chips_over[chip_key]:
                    last_chip_offset["yoffset"] += 8
                    self.chips_over[chip_key] = False
                    renpy.redraw(self, 0)

            if ev.type == pygame.MOUSEBUTTONDOWN:
                for chip_key in self.player["render_chips"].keys():
                    last_chip_offset = None
                    if len(self.player["render_chips"][chip_key]) > 0:
                        last_chip_offset = self.player["render_chips"][chip_key][len(self.player["render_chips"][chip_key]) - 1]
                    if not last_chip_offset:
                        continue
                    
                    chip_inner_position = x > last_chip_offset["xoffset"] and (x < last_chip_offset["xoffset"] + 68) and y > last_chip_offset["yoffset"] - 10 and (y < last_chip_offset["yoffset"] + 48)
                    if chip_inner_position and self.chips_over[chip_key]:
                        self.throwChip(last_chip_offset)

            return

        def chips_render_to(self, rv, width, height, st, at):

            for chip_key in self.player["render_chips"].keys():

                for chip_offset in self.player["render_chips"][chip_key]:

                    surf = renpy.render(self.chipImgs[chip_key], width, height, st, at)
                    cw, ch = surf.get_size()
                    rv.blit(surf, (chip_offset["xoffset"], chip_offset["yoffset"]))

            for chip_key in self.render_chips.keys():

                for chip_offset in self.render_chips[chip_key]:

                    surf = renpy.render(self.chipImgs[chip_key], width, height, st, at)
                    cw, ch = surf.get_size()
                    rv.blit(surf, (chip_offset["xoffset"], chip_offset["yoffset"]))

        def player_hit(self):
            
            if self.player["betted"]:
                if self.player["doubled"] and len(self.player["deck"]) != 2:
                    return self._alert(messages["warning"]["hit"])
                elif self.player["doubled"]:
                    return self.distributeCard("player", True)
                self.distributeCard("player")
            else:
                self._alert(messages["warning"]["bet"])
            
        def player_stand(self):
            
            if not self.player["betted"]:
                return self._alert(messages["warning"]["bet"])
            self.inProgress = True
            self.bank_play()

        def player_insure(self):
            
            if self.inProgress and len(self.bank["deck"]) == 2 and self.bank["deck"][0].value == "A":
                self.player["insurance"] = math.floor(self.player["dealt"] / 2 + 0.5)
                self.player["funds"] -= self.player["insurance"]
                self.player["chips"] = self.balanceChips(self.player["funds"])
                self._alert(messages["warning"]["insured"])
            else:
                self._alert(messages["warning"]["insurance"])

        def player_double(self):

            if self.inProgress and len(self.player["deck"]) == 2 and not self.player["doubled"]:
                if self.player["funds"] >= self.player["dealt"]:
                    self._alert(messages["warning"]["doubled"])
                    self.player["doubled"] = True
                    self.player["funds"] -= self.player["dealt"]
                    self.player["dealt"] *= 2
                    self.player["chips"] = self.balanceChips(self.player["funds"])
                    self.addChips()

                    for chip_key in self.dealt.keys():
                        for i in range(self.dealt[chip_key]):
                            chip = {
                                "xoffset": rand(350, 800),
                                "yoffset": rand(210, 450),
                                "color": chip_key
                            }
                            self.render_chips[chip_key].append(chip)
                            
                    for chip in self.dealt.keys():
                        if self.dealt[chip]:
                            self.dealt[chip] *= 2
                else:
                    self._alert(messages["warning"]["funds"])
            else:
                self._alert(messages["warning"]["double"])

        def player_giveUp(self):
            
            if self.inProgress and len(self.player["deck"]) == 2 and len(self.bank["deck"]) == 2:
                self._alert(messages["warning"]["gaveUp"])
                self.player["funds"] += math.floor(self.player["dealt"] / 2 + 0.5)
                self.player["chips"] = self.balanceChips(self.player["funds"])
                self.addChips()
                self.end()
            else:
                self._alert(messages["warning"]["giveUp"])

        def player_win(self):

            self.message["show"] = True
            self.message["text"] = messages["win"]
            renpy.redraw(self, 0)

            renpy.pause(2)

            if self.player["blackjack"]:
                self.player["funds"] += self.player["dealt"] * 3
            else:
                self.player["funds"] += self.player["dealt"] * 2
            self.end()

        def player_lose(self):

            self.message["show"] = True
            self.message["text"] = messages["lose"]

            if self.player["doubled"] and len(self.player["deck"]) == 3:
                card = self.player["deck"][2]
                card.set_hidden(False)

            renpy.redraw(self, 0)

            renpy.pause(2)
                    
            if self.bank["blackjack"] and self.player["insurance"]:
                self.player["funds"] += self.player["insurance"] * 2
                self.player["chips"] = self.balanceChips(self.player["funds"])
            
            if self.player["funds"] <= 0:
                return self.over()
            self.end()
        
        def player_pass(self):
            
            self.message["show"] = True
            self.message["text"] = messages["pass"]
            renpy.redraw(self, 0)

            renpy.pause(2)

            self.player["funds"] += self.player["dealt"]
            self.end()
            
        def player_draw(self):

            self.message["show"] = True
            self.message["text"] = messages["draw"]
            renpy.redraw(self, 0)

            renpy.pause(2)

            if self.bank["blackjack"] and self.player["insurance"]:
                self.player["funds"] += self.player["insurance"] * 2
                self.player["chips"] = self.balanceChips(self.player["funds"])
            
            self.player["funds"] += self.player["dealt"]
            self.end()
            
        def bank_play(self):

            if self.player["doubled"] and len(self.player["deck"]) > 2:
                card = self.player["deck"][2]
                card.set_hidden(False)
                renpy.redraw(self, 0)

            if len(self.bank["deck"]) == 2:
                card = self.bank["deck"][1]
                card.set_hidden(False)
                renpy.redraw(self, 0)

            total = self.deckValue(self.bank["deck"])

            if total < 17:
                self.distributeCard("bank")
                if self.deckValue(self.bank["deck"]) < 17:
                    renpy.pause(1)
                    self.bank_play()
                else:
                    self.check()
            else:
                self.check()

        def resetChips(self):
            
            for color in self.dealt.keys():
                self.dealt[color] = 0

        def _alert(self, msg):

            self._alert_message["show"] = True
            self._alert_message["text"] = msg["msg"]

            if msg["x"]:
                self._alert_message["xoffset"] = msg["x"]    
            else:
                self._alert_message["xoffset"] = 850
            self._alert_message["yoffset"] = 140
            renpy.redraw(self, 0)

            renpy.pause(1)

            self._alert_message["show"] = False
            renpy.redraw(self, 0)

        def over(self):
            
            self.render_cards = []
            self.render_chips = {
                "blue": [],
                "black": [],
                "green": [],
                "red": [],
                "white": []
            }

            self.message["show"] = True
            self.message["text"] = "Game Over"
            self.message["xoffset"] = 500
            self.message["yoffset"] = 300

            renpy.redraw(self, 0)

        def balanceChips(self, value):

            chips = {
                "blue": 0,
                "black": 0,
                "green": 0,
                "red": 0,
                "white": 0,
            }

            while value != 0:

                for chip in list(reversed(sorted(chips.keys()))):
                    if value >= chipsValue[chip]:
                        value -= chipsValue[chip]
                        chips[chip] += 1

            return chips

        def start(self):

            self.message["show"] = True
            self.message["text"] = messages["bet"]
            self.message["xoffset"] = 1020
            self.message["yoffset"] = 40
            renpy.redraw(self, 0)

            self.buildDeck()
            self.addChips()

        def go(self):

            if self.player["dealt"] and not self.inProgress:
                self.inProgress = True
                self.player["betted"] = True
                self.message["show"] = False
                self.message["text"] = ""
                self.new()
            elif not self.player["dealt"]:
                self._alert(messages["warning"]["bet"])

        def end(self):

            self.inProgress = False
            self.player["betted"] = False
            self.player["insurance"] = False
            self.player["doubled"] = False
            self.player["deck"] = []
            self.player["blackjack"] = False
            self.bank["blackjack"] = False
            self.bank["deck"] = []
            self.player["dealt"] = 0
            self.player["chips"] = self.balanceChips(self.player["funds"])
            self.resetChips()
            self.addChips()
            self.render_cards = []
            self.render_chips = {
                "blue": [],
                "black": [],
                "green": [],
                "red": [],
                "white": []
            }
            self.message["show"] = True
            self.message["text"] = messages["bet"]
            renpy.redraw(self, 0)

        def new(self):

            self.distributeCard("player")
            renpy.pause(0.5)
            self.distributeCard("player")
            renpy.pause(0.5)
            self.distributeCard("bank")
            renpy.pause(0.5)
            self.distributeCard("bank", True)

        def buildDeck(self):

            for i in range(deckNumber):
                for suit in suits:
                    for j in range(2, 11):
                        self.deck.append(__Card(suit, str(j)))

                    for v in ["J", "Q", "K", "A"]:
                        self.deck.append(__Card(suit, v))
            
        def deckValue(self, deck):

            total = 0
            a_number = 0
            deck_value = 0
            check_value = 0

            for card in deck:
                if "A" == card.value:
                    a_number += 1

                if "J" == card.value or "K" == card.value or "Q" == card.value:
                    total += 10

                if card.value.isnumeric() and int(card.value) > 1 and int(card.value) < 11:
                    total += int(card.value)
            
            deck_value = total
            for number in range(a_number + 1):

                check_value = total + 10 * number + a_number

                if check_value <=21:
                    deck_value = check_value

            return deck_value
    
        def distributeCard(self, to, hidden = False):

            index = rand(0, len(self.deck) - 1)

            card = self.deck[index]
            if hidden:
                card.set_hidden(True)

            if to == "bank":
                self.bank["deck"].append(card)

            elif to == "player":
                self.player["deck"].append(card)

            self.deck = self.deck[:index] + self.deck[index+1:]
            self.displayCard(card, to)

        def displayCard(self, card, owner):

            top_offset = 0
            left_offset = 0
            
            if owner == "player":
                top_offset = 500
                left_offset = LEFT + len(self.player["deck"]) * 50
            elif owner == "bank":
                top_offset = 10
                left_offset = LEFT + len(self.bank["deck"]) * 50

            card.set_offset(left_offset, top_offset)

            self.render_cards.append(card)
            renpy.redraw(self, 0)

            if owner == "player" and self.deckValue(self.player["deck"]) > 21:
                self.player_lose()

        def addChips(self):

            base = { "x": 560, "y": 570 }

            for chip_key in self.player["chips"].keys():
                self.player["render_chips"][chip_key] = []
                for i in range(self.player["chips"][chip_key]):

                    self.player["render_chips"][chip_key].append({
                        "xoffset": base["x"],
                        "yoffset": base["y"],
                        "color": chip_key
                    })
                    base["y"] -= 10

                base["y"] = 570
                base["x"] += 75
            renpy.redraw(self, 0)

        def throwChip(self, chip):

            if self.inProgress:
                return
            chip["xoffset"] = rand(350, 800)
            chip["yoffset"] = rand(210, 400)
            renpy.redraw(self, 0)
            color = chip["color"]

            self.chips_over[color] = False
            self.player["dealt"] += self.chipsValue[color]
            self.player["chips"][color] -= 1
            self.player["funds"] -= self.chipsValue[color]
            self.dealt[color] += 1
            self.render_chips[color].append(chip)
            self.addChips()

        def check(self):

            bankScore = self.deckValue(self.bank["deck"])
            playerScore = self.deckValue(self.player["deck"])

            if bankScore == 21 and len(self.bank["deck"]) == 2:
                self.bank["blackjack"] = True
            if playerScore == 21 and len(self.player["deck"]) == 2:
                self.player["blackjack"] = True

            if self.bank["blackjack"] and self.player["blackjack"]:
                self.player_draw()
            elif self.bank["blackjack"]:
                return self.player_lose()
            elif self.player["blackjack"]: 
                return self.player_win()

            if bankScore > 21:
                self.player_win()
            elif bankScore >= 17 and bankScore <= 21:
                if playerScore > bankScore:
                    self.player_win()
                elif playerScore == bankScore:
                    self.player_pass()
                else:
                    self.player_lose()


    class __Card(object):

        def __init__(self, suit, value, hidden = False, x = 0, y = 0):

            self.suit = suit

            self.value = value

            self.hidden = hidden

            self.face = Transform("assets/PNG/Cards/card" + str(suit) + str(value) + ".png")

            self.back = Transform("assets/PNG/Cards/cardBack_red5.png")

            self.x = x

            self.y = y

        def set_hidden(self, hidden):

            self.hidden = hidden

        def get_offset(self):

            return self.x, self.y

        def set_offset(self, x, y):

            self.x = x

            self.y = y

        def render_to(self, rv, width, height, st, at):

            x, y = self.get_offset()

            if self.hidden:
                d = self.back
            else:
                d = self.face

            surf = renpy.render(d, width, height, st, at)

            rv.blit(surf, (x, y))