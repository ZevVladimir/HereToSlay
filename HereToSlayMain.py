import tkinter as tk
from tkinter import *
import random


here_to_slay = tk.Tk()
set_up = tk.Frame(here_to_slay)
party_leader_choice = tk.Frame(here_to_slay)
set_up.pack_forget()
width = here_to_slay.winfo_screenwidth()
height = here_to_slay.winfo_screenheight()
here_to_slay.geometry("%dx%d" % (width, height))
party_number = 5
action_point_display = 3
action_point = 4
monster_placement = 0
player_turn = True
chosen_enemy_hand = None
chosen_hand_spot = None
chosen_party_spot = None
chosen_e_party_spot = None

place_holder = PhotoImage(file="placeHolder.png")
fighter_icon = PhotoImage(file="fighterIcon.png")
bard_icon = PhotoImage(file="bardIcon.png")
guardian_icon = PhotoImage(file="guardianIcon.png")
ranger_icon = PhotoImage(file="rangerIcon.png")
thief_icon = PhotoImage(file="thiefIcon.png")
wizard_icon = PhotoImage(file="wizardIcon.png")

party_leader_text = ["Fighter" + "\n" + "Everytime you roll in a" + "\n" + "challenge +2 to your roll", "Bard" +
                     "\n" + "Each time you roll a hero's" + "\n" + "effect +1 to your roll", "Guardian" + "\n" +
                     "Each time you play a modifier card" + "\n" + "+1 or -1 to that roll", "Ranger" + "\n" +
                     "Each time you attack a monster card" + "\n" + "+1 to your roll", "Thief" + "\n" +
                     "Once per turn, on your turn, you may" + "\n" + "spend 1 action point to pull a card" + "\n" +
                     "from another player's hand", "Wizard" + "\n" + "Each time you play a magic card" + "\n" +
                     "draw a card"]

monsters = [["Abyss Queen \n Each time another player plays \n a Modifier cards on one \n of your rolls, \n +1 to your roll \n 5-: Sacrifice"
             "a hero card \n 8+: Slay this monster card", [5, 8], [2, 0, 0, 0, 0, 0, 0]],
            ["Anuran Cauldron \n Each time you roll, \n +1 to that roll \n 6-: Sacrifice a hero card \n 7+: Slay this monster card",
             [6, 7], [3, 0, 0, 0, 0, 0, 0]],
            ["Arctic Aries \n Each time you successfully \n roll to use a Hero Card's \n effect, you may draw a card. \n "
             "6-: Sacrifice a Hero Card \n 10+: Slay this monster card", [6, 7], [1, 0, 0, 0, 0, 0, 0]],
            ["Bloodwing \n Each time another player \n CHALLENGES you, that player must \n DISCARD a card. \n 6-: SACRIFICE a Hero card"
             "\n 9+: SLAY this Monster card", [6, 9], [2, 0, 0, 0, 0, 0, 0]],
            ["Corrupted Sabertooth \n Each time you would \n DESTROY a Hero card, \n you may STEAL that Hero \n card instead.\n"
             "6-: Sacrifice a Hero Card \n 9+: Slay this Monster card \n and DRAW a card", [6, 9], [3, 0, 0, 0, 0, 0, 0]]]


class HeroAbilities:
    def use_ability(self):
        use_ability = True
        if action_point_display <= 0:
            display_message.warning_messages('not_enough_ap')
            use_ability = False
        return use_ability

    def pull_card(self, event):
        global chosen_enemy_hand
        global chosen_party_spot
        if action_point_display <= 0:
            display_message.warning_messages('not_enough_ap')
        else:
            if chosen_enemy_hand is None:
                display_message.warning_messages("select_e_hand")
            else:
                roll = rolling_dice.roll_the_dice()
                minimum = party_storage[chosen_party_spot]['roll']
                use_action_point(1, action_point_display)
                if roll >= minimum:
                    player_hand_storage.append(enemy_hand_storage[chosen_enemy_hand])
                    enemy_hand_storage.pop(chosen_enemy_hand)
                    reset_player_hand(player_hand_storage)
                    reset_enemy_hand(enemy_hand_storage)
                    chosen_enemy_hand = None

                elif roll < minimum:
                    display_message.warning_messages('Roll is too low')


    def destroy_hero(self, event):
        if self.use_ability():
            global chosen_e_party_spot
            global enemy_party_storage
            if chosen_e_party_spot is None:
                display_message.warning_messages(("select_e_party"))
            else:
                destroy_me_button = enemy_party_button_storage[chosen_e_party_spot]
                destroy_me_button.destroy()
                chosen_e_party_spot = None

    def draw_card(self, event):
        if self.use_ability():
            roll = rolling_dice.roll_the_dice()
            minimum = party_storage[chosen_party_spot]['roll']
            use_action_point(1, action_point_display)
            if roll >= minimum:
                amount = party_storage[chosen_party_spot]['draw_num']
                while amount > 0:
                    player_hand_storage.append(shuffled_deck[0])
                    shuffled_deck.pop(0)
                    amount -= 1
                reset_player_hand(player_hand_storage)
            else:
                display_message.warning_messages('Roll is too low')


hero_ability_creator = HeroAbilities()


all_heroes = [{'text': "Bad Axe \n DESTROY a hero card \n Roll: 8+", 'roll': 8, 'ability': hero_ability_creator.destroy_hero, 'type': "fight", 'image': fighter_icon},
              {'text': "Bear Claw \n Pull a card from \n another player's hand. \n If it is a Hero Card, \n pull a "
               "second card \n from that player's hand \n Roll: 7+", 'roll': 7, 'ability': hero_ability_creator.pull_card, 'type': "fight", 'image': fighter_icon},
              {'text': "Beary Wise \n Each other player \n must discard a card. \n Chose one of the discarded \n cards "
               "and add it to your hand \n Roll: 7+", 'roll': 7, 'type': "fight", 'image': fighter_icon},
              {'text': "Fury Knuckle \n Pull a card if it \n is a challenge card \n pull a second card \n Roll: 5+", 'roll': 5,
               'ability': hero_ability_creator.pull_card, 'type': "fight", 'image': fighter_icon},
              {'text': "Heavy Bear \n Choose a player. That \n player must discard \n two cards \n Roll: 5+", 'roll': 5, 'type': "fight", 'image': fighter_icon},
              {'text': "Pan Chucks \n Draw two cards if \n at least one of those \n cards is a challenge card \n you may"
               " destroy a hero card \n Roll: 8+", 'roll': 8, 'ability': hero_ability_creator.draw_card, 'draw_num': 2, 'type': "fight", 'image': fighter_icon},
              {'text': "Qi Bear \n Discard up to three \n cards. For each card \n discarded destroy a \n hero card \n "
               "Roll: 10+", 'roll': 10, 'type': "fight", 'image': fighter_icon},
              {'text': "Tough Teddy \n Each player with \n a fighter has to \n discard a card \n Roll: 4+", 'roll': 4, 'type': "fight", 'image': fighter_icon},
              {'text': "Dodgy Dealer \n Trade hands with \n another player.", 'roll': 9, 'ability': hero_ability_creator.draw_card, 'draw_num': 1, 'type': "bard", 'image': bard_icon},
              {'text': "Fuzzy Cheeks \n DRAW a card and \n play a Hero card from \n your hand immediately. \n Roll: 8+", 'roll': 8, 'ability': hero_ability_creator.draw_card, 'draw_num': 1, 'type': "bard", 'image': bard_icon},
              {'text': "Greedy Cheeks \n Each other player \n must give you a card from \n their hand.", 'roll': 8, 'type': "bard", 'image': bard_icon},
              {'text': "Lucky Bucky \n Pull a card from \n another player's hand. \n If that card is a Hero card, \n "
               "you may play it immediately", 'roll': 7, 'ability': hero_ability_creator.pull_card, 'type': "bard", 'image': bard_icon},
              {'text': "Mellow Dee \n DRAW a card. If \n that card is a \n Hero card, you \n may play it immediately.", 'roll': 7, 'ability': hero_ability_creator.draw_card, 'draw_num': 1, 'image': bard_icon},
              {'text': "Napping Nibbles \n Do nothing.", 'roll': 2, 'type': "bard", 'image': bard_icon},
              {'text': "Peanut \n DRAW 2 cards.", 'roll': 7, 'ability': hero_ability_creator.draw_card, 'draw_num': 2, 'type': "bard", 'image': bard_icon},
              {'text': "Tipsy Tootie \n Choose a player. \n STEAL a Hero card from \n that player's Party and \n move "
               "Tipsy Tootie to \n that player's Party.", 'roll': 6, 'type': "bard", 'image': bard_icon},
              {'text': "Calming Voice \n Hero cards in your \n Party cannot be stolen until \n your next turn.", 'roll': 9, 'type': "guard", 'image': guardian_icon},
              {'text': "Guiding Light \n Search the discard pile \n for a Hero card and add \n it to your hand.", 'roll': 7, 'type': "guard", 'image': guardian_icon},
              {'text': "Holy Curselifter \n Return a Cursed Item card \n equipped to a Hero card in \n your Party to your hand", 'roll': 5, 'type': "guard", 'image': guardian_icon},
              {'text': "Iron Resolve \n Cards you play cannot \n be challenged for the rest \n of your turn.", 'roll': 8, 'type': "guard", 'image': guardian_icon},
              {'text': "Mighty Blade \n Hero cards in your \n Party cannot be destroyed until \n your next turn.", 'roll': 8, 'type': "guard", 'image': guardian_icon},
              {'text': "Radiant Horn \n Search the discard pile for \n a Modifier card and add it \n to your hand.", 'roll': 6, 'type': "guard", 'image': guardian_icon},
              {'text': "Vibrant Glow \n +5 to all your rolls \n until the end of your turn.", 'roll': 9, 'type': "guard", 'image': guardian_icon},
              {'text': "Wise Shield \n +3 to all your rolls \n until the end of your turn.", 'roll': 6, 'type': "guard", 'image': guardian_icon}]

all_magic = [{'text': "Call to the Fallen \n Search the discard pile \n for a Hero card and add \n it to your hand.", 'image': place_holder},
             {'text': "Critical Boost \n DRAW 3 cards and \n DISCARD a card.", 'ability': hero_ability_creator.draw_card, 'draw_num': 3, 'image': place_holder},
             {'text': "Destructive Spell \n DISCARD a card, \n then DESTROY a \n Hero card.", 'ability': hero_ability_creator.destroy_hero, 'image': place_holder},
             {'text': "Enchanted Spell \n +2 to all of your \n rolls until the end \n of your turn.", 'image': place_holder},
             {'text': "Entangling Trap \n DISCARD 2 cards, \n then STEAL a Hero card.", 'image': place_holder},
             {'text': "Forced Exchange \n Choose a player. \n STEAL a Hero card from that \n player's Party, then move a Hero \n "
              "card from your Party \n to that player's Party.", 'image': place_holder},
             {'text': "Forceful Winds \n Return every equipped item \n card to its respective player's \n hand.", 'image': place_holder},
             {'text': "Winds of Change \n Return an Item card \n equipped to any player's \n Hero card to that player's \n hand, "
              "then DRAW a card.", 'image': place_holder}]
all_items = []
all_modifiers = []
all_challenges = []

shuffled_deck = []
used_cards = []


def right_click(event):
    print("right")


hero_class = [fighter_icon, bard_icon, guardian_icon, ranger_icon, thief_icon, wizard_icon]
player_starting_hand_storage = []
player_hand_storage = []
party_storage = [{'text': "Party 1", 'ability': right_click, 'image': place_holder}, {'text': "Party 2", 'ability': right_click, 'image': place_holder},
                 {'text': "Party 3", 'ability': right_click, 'image': place_holder}, {'text': "Party 4", 'ability': right_click, 'image': place_holder},
                 {'text': "Party 5", 'ability': right_click, 'image': place_holder}]
player_hand_button_storage = []
party_button_storage = []
monster_board_storage = []
monster_button_storage = []
player_monster_storage = []
monster_roll_values = []

enemy_hand_storage = []
enemy_party_storage = []
enemy_party_button_storage = []
enemy_hand_button_storage = []
enemy_monster_storage = []

action_point_label = tk.Label(set_up, text="Action Points: \n 3", font=("Ariel", 25))
action_point_label.grid(row=3, column=8, padx=1, pady=1)


def enemy_hand_num(e_hand_number):
    global chosen_enemy_hand
    chosen_enemy_hand = e_hand_number


def party_num(chosen_party_num):
    global chosen_party_spot
    chosen_party_spot = chosen_party_num


def use_action_point(how_much, current):
    current -= how_much
    global action_point_display
    action_point_display = current
    global action_point
    action_point -= 1
    action_point_label.configure(text="Action Points: \n" + str(current))


def win_con(owned_monster):
    if len(owned_monster) == 3 and player_turn is True:
        display_message.warning_messages("game_win")
    elif len(owned_monster) == 3 and player_turn is False:
        display_message.warning_messages("game_loss")


def end_turn():
    global action_point_display
    action_point_display = 3
    global action_point
    action_point = 4
    action_point_label.configure(text="Action Points: \n 3")
    global player_turn
    if player_turn is True:
        win_con(player_monster_storage)
        player_turn = False
        enemy_creator.decision()
    elif player_turn is not True:
        win_con(enemy_monster_storage)
        player_turn = True

def draw_card_pile():
    if action_point_display > 0:
        use_action_point(1, action_point_display)
        player_hand_storage.append(shuffled_deck[0])
        reset_player_hand(player_hand_storage)
    else:
        display_message.warning_messages('not_enough_ap')


class CreateCard:
    def __init__(self):
        shuffled_deck.extend(all_heroes)
        shuffled_deck.extend(all_magic)
        shuffled_deck.extend(all_items)
        shuffled_deck.extend(all_modifiers)
        shuffled_deck.extend(all_challenges)

        random.shuffle(shuffled_deck)

    def create_card_func(self):  # function to create a card
        chosen_number = random.randint(0, len(shuffled_deck) - 1)
        chosen_card = shuffled_deck[chosen_number]
        used_cards.append(shuffled_deck[chosen_number])
        shuffled_deck.pop(chosen_number)
        return chosen_card


class Monster:
    def create_monster_card(self):
        try:
            choose_monster = random.randint(0, len(monsters) - 1)  # Choose a random monster
            global monster_roll_values
            monster_roll_values.append(monsters[choose_monster][1])
            chosen_monster = monsters[choose_monster][0]
            monsters.pop(choose_monster)  # Remove chosen monster
            return chosen_monster
        except:
            print()

    def attack_monster(self, current_monster, monster_button, placement_from, success, fail):
        global monster_dice_roll
        if action_point_display > 1:
            monster_dice_roll = rolling_dice.roll_the_dice()
            use_action_point(2, action_point_display)
            if player_turn is True and monster_dice_roll >= int(success):
                global monster_placement
                player_monster_storage.append(monster_button[placement_from].cget("text"))
                player_monster = tk.Label(set_up, text=current_monster[placement_from], image=place_holder,
                                          compound="center")
                player_monster.grid(row=monster_placement + 3, column=0, padx=1, pady=1)
                current_monster.pop(placement_from)
                if new_monster.create_monster_card() is not None:
                    current_monster.append(new_monster.create_monster_card())
                counter = len(monster_button_storage) - 1
                while 0 <= counter:
                    destroy_monster_button = monster_button_storage[counter]
                    destroy_monster_button.destroy()
                    counter -= 1
                monster_button_storage.clear()
                base_board_creator.set_up_monster(current_monster, len(current_monster))
                monster_placement += 1

            elif player_turn is True and monster_dice_roll <= int(fail):
                display_message.warning_messages("monster_loss")

        elif action_point_display <= 1:
            display_message.warning_messages("not_enough_ap")


class BaseBoard:  # Sets up board in the default position with nothing set out
    # Sets up the five empty slots that heroes can go

    hand_number = 0
    monster_number = 1

    def set_up_hand(self, hero_storer, amount):  # creates how many cards in hand as needed
        for num in range(0, amount):
            # generic button with functions needed to create attached
            hand_display = tk.Button(set_up, text=hero_storer[num]['text'], image=hero_storer[num]['image'], command=lambda num=num:
                                     [get_hand_num(hero_storer[num], hero_storer)], compound="center")
            hand_display.grid(row=5, column=num + 1, padx=1, pady=10)

            player_hand_button_storage.append(hand_display)
            player_hand_storage.append(hero_storer[num])

    def set_up_party(self, party_storer, amount):
        for num in range(0, amount):  # creates starting 5 party slots: empty for now need functions for button
            party_display = tk.Button(set_up, text=party_storer[num]['text'], image=party_storer[num]['image'],
                                      command=lambda num=num: [add_party_member(player_hand_storage, party_storer, num)],
                                      compound="center")
            party_display.bind("<ButtonPress-3>", lambda event, num=num: party_num(num))
            party_display.bind("<ButtonRelease-3>", party_storer[num]['ability'])
            party_display.grid(row=4, column=num + 1, padx=1, pady=10)

            party_button_storage.append(party_display)

    # Sets up the three empty slots that monsters will go
    def set_up_monster(self, monster_storer, amount):
        for monst_num in range(0, amount):
            monster_display = tk.Button(set_up, text=monster_storer[monst_num], image=place_holder, compound="center",
                                        command=lambda monst_num=monst_num: new_monster.attack_monster(monster_storer, monster_button_storage, monst_num,
                                                                                                       monster_roll_values[monst_num][0], monster_roll_values[monst_num][1]))
            monster_display.grid(row=3, column=monst_num + 2, padx=1, pady=10)

            monster_button_storage.append(monster_display)


    def set_up_enemy_hand(self, amount):
        for e_hand in range(0, amount):
            e_hand_display = tk.Button(set_up, text="Hand " + str(e_hand + 1), image=place_holder, compound="center",
                                       command=lambda e_hand=e_hand: enemy_hand_num(e_hand))
            e_hand_display.grid(row=0, column=e_hand + 1, padx=1, pady=1)

            enemy_hand_button_storage.append(e_hand_display)


    # Sets up remaining places draw and discard pile and party leader
    draw_pile = tk.Button(set_up, text="Draw Pile", image=place_holder, command=lambda: draw_card_pile(), compound="center")
    discard_pile = tk.Button(set_up, text="Discard Pile", image=place_holder, compound="center")

    draw_pile.grid(row=3, column=1, padx=1, pady=1)
    discard_pile.grid(row=3, column=5, padx=1, pady=1)

    end_turn_button = tk.Button(set_up, text="End Turn", image=place_holder, compound="center", command=lambda: end_turn())
    end_turn_button.grid(row=5, column=8, padx=1, pady=1)

    use_action_point(0, action_point_display)


class PartyLeader:
    def set_leader_choice(self, chosen_party_leader_text, enter):  # Takes input from what user enter and then from list outputs the correct party leader
        # text on the actual board
        party_leader_display = tk.Label(set_up, text=chosen_party_leader_text[enter], image=place_holder, compound="center")
        party_leader_display.grid(row=4, column=6, padx=1, pady=1)
        party_leader_choice.forget()
        set_up.pack()

    def party_leader_selection(self, party_leader):  # Sets up the five empty slots that heroes can go: create button to select,
        # create button to display ability and choose selected hero
        for p in range(0, 5):
            party_leader_button = tk.Button(party_leader_choice,
                                            text=party_leader[p], image=place_holder,
                                            command=lambda p=p: self.set_leader_choice(party_leader, p), compound="center")
            party_leader_button.grid(row=0, column=p, padx=1, pady=1)


class RollDice:
    def roll_the_dice(self):
        dice_roll = random.randint(2, 13)
        dice_roll_display.configure(text="Dice Roll: \n" + str(dice_roll))
        return dice_roll


def get_hand_num(chosen_hand_card, current_hand):  # Gets which card from hand player last has chosen
    global chosen_hand_spot
    for i in range(0, len(current_hand)):
        if current_hand[i] == chosen_hand_card:
            chosen_hand_spot = i
            continue


def get_e_party_num(e_party_spot):
    global chosen_e_party_spot
    chosen_e_party_spot = e_party_spot


def remove_card_hand(destroy):  # Removes chosen card from hand after played into party
    if action_point >= 0 and player_turn is True:
        counter = len(player_hand_storage) - 1
        hand_storage_copy = player_hand_storage.copy()  # Create copy to send to recreate buttons after original is cleared
        hand_storage_copy.pop(destroy)  # Remove which card is going to be played

        while 0 <= counter:  # Run for how many cards there are in the hand and destroy all buttons and clear storage
            player_hand_storage.pop(counter)
            destroy_me_button = player_hand_button_storage[counter]
            destroy_me_button.destroy()

            counter -= 1
        player_hand_button_storage.clear()
        base_board_creator.set_up_hand(hand_storage_copy, len(hand_storage_copy))


def add_party_member(current_hand, current_party, placement_to):  # Resets the party so when new card is added that is reflected
    global chosen_hand_spot
    if chosen_hand_spot is not None:
        if action_point_display > 0 and player_turn is True:
            use_action_point(1, action_point_display)
            counter = 4
            placement_from = chosen_hand_spot
            current_party[placement_to] = current_hand[placement_from]  # Take what card is from the hand and make chosen party spot that

            while 0 <= counter:  # Delete all buttons and clear lists
                destroy_me_button = party_button_storage[counter]
                destroy_me_button.destroy()

                counter -= 1
            party_button_storage.clear()
            print(current_party)
            base_board_creator.set_up_party(current_party, 5)  # Recreate the party with adjusted cards

            remove_card_hand(chosen_hand_spot)
        elif action_point_display <= 0:
            display_message.warning_messages("not_enough_ap")


class EnemyAction: # TODO fix how many cards opponent plays
    def clear_e_party(self):
        if len(enemy_party_button_storage) > 0:
            counter = len(enemy_party_button_storage) - 1
            while 0 < counter:  # Delete all buttons and clear lists
                destroy_me_button = enemy_party_button_storage[counter]
                destroy_me_button.destroy()

                counter -= 1
            enemy_party_button_storage.clear()


    def e_play_hero_card(self, enemy_hand_storer, chosen):
        for num in range(0, 1):
            enemy_party_display = tk.Button(set_up, text=enemy_hand_storer[chosen]['text'], image=enemy_hand_storer[chosen]['image'],
                                            compound="center")
            enemy_party_display.grid(row=2, column=num + 1, padx=1, pady=10)
            enemy_party_display.bind("<Button-1>", lambda x: get_e_party_num(num))
            enemy_hand_storer.pop(chosen)
            enemy_party_button_storage.append(enemy_party_display)
            use_action_point(1, action_point_display)

    def decision(self):
        global player_turn
        while action_point_display > 2 and player_turn is False:
            enemy_hand_storage_copy = enemy_hand_storage.copy()
            self.clear_e_party()
            self.e_play_hero_card(enemy_hand_storage_copy, random.randint(0, len(enemy_hand_storage_copy) - 1))
        end_turn()


class PopUpMessage:
    warning = tk.Toplevel()
    warning.geometry("750x250")
    warning.title("Warning!")
    warning_exit_label = tk.Label(warning, text="")
    warning_choices = {'game_win': "You won :)", 'game_loss': "You lost :(", 'not_enough_ap': "Can't do this, not enough Action Points", 'monster_loss': "You lost, choose a hero to sacrifice",
                        'select_e_hand': "You didn't select a card to pull from the enemy's hand", 'select_e_party':
                           "You didn't select a hero to destroy from the enemy's hand", 'Roll is too low': "Your roll was too low and the ability failed"}

    def __init__(self):
        warning_exit_button = tk.Button(self.warning, text="Ok", command=self.warning.withdraw, compound="center")
        self.warning_exit_label.pack()
        warning_exit_button.pack()

    def warning_messages(self, chosen_warning):
        warning = self.warning_choices[chosen_warning]
        self.warning_exit_label.configure(text=warning)
        self.warning.deiconify()


def reset_player_hand(current_hand):
    counter = len(player_hand_button_storage) - 1
    current_hand_copy = current_hand.copy()
    while 0 <= counter:
        destroy_me_button = player_hand_button_storage[counter]
        destroy_me_button.destroy()
        counter -= 1
    current_hand.clear()
    player_hand_storage.clear()
    base_board_creator.set_up_hand(current_hand_copy, len(current_hand_copy))


def reset_enemy_hand(current_e_hand):
    counter = len(enemy_hand_button_storage) - 1
    current_e_hand_copy = current_e_hand.copy()
    while 0 <= counter:
        destroy_me_button = enemy_hand_button_storage[counter]
        destroy_me_button.destroy()
        counter -= 1
    enemy_hand_button_storage.clear()
    base_board_creator.set_up_enemy_hand(len(current_e_hand_copy))


dice_roll_display = tk.Label(set_up, text="Dice Roll: \n --", image=place_holder, compound="center")
dice_roll_display.grid(row=4, column=8, padx=1, pady=1)

new_hero = CreateCard()
for num in range(0, 5):
    player_starting_hand_storage.append(new_hero.create_card_func())

for num in range(0, 5):
    enemy_hand_storage.append(new_hero.create_card_func())

new_monster = Monster()
for num in range(0, 3):
    monster_board_storage.append(new_monster.create_monster_card())
display_message = PopUpMessage()
rolling_dice = RollDice()
party_leader_creator = PartyLeader()
party_leader_choice.pack(pady=10, padx=0)
party_leader_creator.party_leader_selection(party_leader_text)
base_board_creator = BaseBoard()
base_board_creator.set_up_hand(player_starting_hand_storage, 5)
base_board_creator.set_up_party(party_storage, 5)
base_board_creator.set_up_monster(monster_board_storage, 3)
base_board_creator.set_up_enemy_hand(5)
enemy_creator = EnemyAction()

here_to_slay.mainloop()
