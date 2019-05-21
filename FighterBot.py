from Bot import Bot
import keyboard as kb
from time import sleep
from random import randint

class FighterBot(Bot):

    MIN_ATTACKS = 5
    MAX_ATTACKS = 6

    SPELLS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    AA_KEY = ['0']
    FW_KEY = ['w']
    BW_KEY = ['s']
    RIGHT_KEY = ['d']
    LEFT_KEY = ['a']
    MOVE_RIGHT = ['e']
    MOVE_LEFT = ['q']
    JUMP_KEY = ['Space']
    REST_KEY = 'c'
    REBUFF_KEY = 'r'
    STOP_KEY = 'Ctrl'

    NUM_BUFFS = 2
    MIN_SPELL_DELAY = 150 # /100 to get number of seconds
    MAX_SPELL_DELAY = 250 # /100 to get number of seconds

    JUMP_PROBABILITY = -1 # in %
    REST_TIME = 15 # in seconds
    REST_THRESHOLD = 1000 # in number of mobs killed

    def __init__(self):
        Bot.__init__(self)
        self.name = "mage_bot"
        self.killed_mobs = 0
        self.total_killed = 0

    def rebuff(self):
        for i in xrange(FighterBot.NUM_BUFFS):
            sleep(3)
            kb.press_and_release(FighterBot.REBUFF_KEY)

    """
    Should write an heuristic for selecting next monster
    At this moment just auto the closest one
    """
    def select_next_monster(self):
        kb.press_and_release(FighterBot.AA_KEY)
        sleep(0.25)
        #kb.press_and_release(FighterBot.BW_KEY)

    """
    Should write an heuristic for using more spells.
    At this moment it is just MagicArrow.
    """
    def attack(self):
        num_attacks = randint(FighterBot.MIN_ATTACKS, FighterBot.MAX_ATTACKS)
        #print("Attacking {} times".format(num_attacks))
        print("Monster {}.".format(self.killed_mobs))
        for i in xrange(num_attacks):
            # jump with a givenprobability
            #if randint(0, 100) < FighterBot.JUMP_PROBABILITY:
            #    kb.press_and_release(FighterBot.J1UMP_KEY)

            if i == 0:
                kb.press_and_release(FighterBot.SPELLS[0])
            elif i == 1:
                kb.press_and_release(FighterBot.SPELLS[1])
            else:
                kb.press_and_release(FighterBot.SPELLS[2])
            delay = randint(FighterBot.MIN_SPELL_DELAY, FighterBot.MAX_SPELL_DELAY) / 100.0
            #print("Wait {} until next attack".format(delay))
            sleep(delay)
        self.killed_mobs += 1

    def rest(self):
        # make sure you finish killing last monster but do not select another one
        self.attack()

        # sit then press forward to get up
        kb.press_and_release(FighterBot.REST_KEY)
        sleep(FighterBot.REST_TIME)
        kb.press_and_release(FighterBot.FW_KEY)

    def main_loop(self):
        print("Waiting {} key to start. Stop it using the same key".format(FighterBot.STOP_KEY))
        kb.wait(FighterBot.STOP_KEY)

        for i in range(5):
            print("Starting in {} sec...".format(5 - i))
            sleep(1)

        #self.rebuff()

        self.killed_mobs = 0
        while True:
            # exit key
            if kb.is_pressed(FighterBot.STOP_KEY):
                print("Killed ~ {} mobs".format(self.total_killed + self.killed_mobs))
                break

            self.select_next_monster()
            self.attack()

            if self.killed_mobs % 10 == 0:
                kb.press_and_release('z')
            if self.killed_mobs == FighterBot.REST_THRESHOLD:
                self.rest()
                self.total_killed += self.killed_mobs
                self.killed_mobs = 0
