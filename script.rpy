# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
define Albero = Character('Albero', color="#DD3B10")
#characters
define mc = Character("[mcname]", color="#357E9A")
default albero_affection = 0

# The game starts here.

label start:
   $ mcname = renpy.input ("What is your name?", default = "Celso")
   
   $ mcname = mcname.strip()

   if mcname == "":
      $ mcname = "Celso"

# The game starts here.

# play a music files

play music "audio/music/Smooth_Jazz__3_Min.wav"

scene bg nj
with dissolve
"It's a tranquil evening in New Jersey."
"You are ambulating through the bustling city, examining your surroundings."
scene bg vonelmancasino

# play a music file

play music "audio/music/Electro_Swing_Jazz_Full.wav"
"As you venture further along, you stumble across a refulgently-lit casino building."
"The lights are alluring to you, so you enter the establishment."
scene bg casino
with dissolve
"Upon entering, you look around."
"You descry a variety of table games, slot machines, and a lounge in the back."
scene bg lounge
with dissolve
"Feeling like you need to repose your feet for a moment, you enter the lounge, making yourself comfortable in one of the chairs."
"When suddenly..."
show albero normal at center
with dissolve
"You are approached by a handsome, auburn-furred beaver with a neatly-kept unibrow and spiffy attire."
show albero smug at center 
with dissolve
Albero "Benvenuti al Casinò von Elman!" 
Albero "(Welcome to Casino von Elman!)"
menu:
   "Italiano? Grazie!":
      mc "Italiano? Grazie! Thank you so much for the warm welcome! By the way, I LOVE your attire. You have astounding taste in fashion. I wish I could pull that off!"
      $ albero_affection += 3
      show albero normal
      with dissolve
      Albero "Why, thank you for noticing. After all, I just HAD to wear something de rigueur enough to match my immaculate unibrow."
      jump continue_story
   "Hey, thanks!":
      mc "Hey, thanks! By the way, your clothes are pretty nice."
      $ albero_affection += 1
      show albero normal at center
      with dissolve
      Albero "Of course they are. I need to wear a fabulous outfit to match my fabulous unibrow, don't I?"
      jump continue_story
   "Is that Spanish?":
      $ albero_affection -= 1
      mc "Is that Spanish? And like...are you a talking ferret?"
      show albero annoyed at center
      with dissolve
      Albero "No..."
      Albero "First of all, I speak Italian. Second of all, I'm a beaver..."
      jump continue_story

      label continue_story:
      show albero normal at center
      with dissolve
      Albero "Anyway...this is my private casino. My name is Albero von Elman, and I run the establishment. You're free to stay here as long as you like."
      show albero smug
      with dissolve
      Albero "We offer a large variety of games, including blackjack, craps, roulette, and slots. Poker is in the back room."
      show albero normal at center
      with dissolve
      Albero "Drinks are on the house."
      show albero normal at center
      Albero "Oh...and one more thing..."
      Albero "I didn't catch your name?"

menu:
   "My name's [mcname].":
      $ albero_affection += 1
      mc "My name's [mcname]. It's nice to meet you, Albero!"
      Albero "It's nice to meet you, too."
      jump continue_story2
   "It's a pleasure...":
      $ albero_affection += 3
      mc "It's a pleasure to make your acquaintance, Albero. Piacere! My name is [mcname]."
      Albero "Piacere! It's a pleasure to meet you as well."
      jump continue_story2
   "I'm not telling you my name!":
      mc "I'm not telling you my name! I don't even know you!"
      $ albero_affection -= 1
      show albero annoyed at center
      Albero "Suit yourself..."
      Albero "(Why am I choosing to interact with this peasant...)"
      jump continue_story2

      label continue_story2:
      show albero normal at center
      Albero "Moving on..."
      Albero "I just had a brilliant idea!"
      Albero "Since you're already here, why not join me for a game of blackjack?"
    

menu:
   "Sure! That sounds like fun!":
      $ albero_affection += 3
      show albero smug at center
      Albero "Perfetto! Right this way, please..."
   "No, thank you. But I appreciate the offer!":
      $ albero_affection += 1
      show albero normal at center
      Albero "No worries. Maybe some other time."

scene bg blackjack

python:
   k = Klondike(mcname=mcname)
   k.show()

label continue:

   show albero small at right
   with dissolve

label quick_continue:

   style mbutton_text:
      size 28
      idle_color "#aaaaaa"
      hover_color "#cc6600"
   while True:

      python:

         ui.textbutton("Hit", ui.jumps("hit"), None, text_style="mbutton_text", xalign=.02, yalign=.96)
         ui.textbutton("Stand", ui.jumps("stand"), None, text_style="mbutton_text", xalign=.1, yalign=.96)
         ui.textbutton("Give up", ui.jumps("giveup"), None, text_style="mbutton_text", xalign=.02, yalign=.82)
         ui.textbutton("Double", ui.jumps("double"), None, text_style="mbutton_text", xalign=.02, yalign=.75)
         ui.textbutton("Insurance", ui.jumps("insurance"), None, text_style="mbutton_text", xalign=.02, yalign=.68)
         ui.textbutton("New game", ui.jumps("newgame"), None, text_style="mbutton_text", xalign=.02, yalign=.04)
         ui.textbutton("Go", ui.jumps("go"), None, text_style="mbutton_text", xalign=.92, yalign=.13)
         
         event = k.interact()

         if event:
            renpy.checkpoint()

label giveup:
   
   python:

      k.giveUp()

   jump quick_continue

label newgame:

   python:
      k.hide()

   menu:
      Albero "Would you like to try again?"

      "Yes":
         pass

      "No":
         Albero "Well, I hope to see you again soon."
         return 

   Albero "Okay, here we go!"

   $ mcname = renpy.input ("What is your name?", default = "Celso")
   
   $ mcname = mcname.strip()

   if mcname == "":
      $ mcname = "Celso"
    
   scene bg blackjack
   python:

      k = Klondike(mcname=mcname)
      k.show()

   jump continue

label hit:

   python:

      k.hit()

   jump quick_continue

label stand:

   python:

      k.stand()

   jump quick_continue

label double:

   python:

      k.double()

   jump quick_continue

label insurance:

   python:

      k.insurance()

   jump quick_continue

label go:

   python:

      k.go()

   jump quick_continue