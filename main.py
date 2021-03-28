import random


class Player:
    def __init__(self, alignment, role, charisma=0):
        self.alignment = alignment
        self.role = role
        self.charisma = charisma

    def get_alignment(self):
        return self.alignment

    def get_charisma(self):
        return self.charisma

    def set_charisma(self, charisma):
        self.charisma = charisma


class Setup:
    def __init__(self, populace):
        self.populace = populace

    def get_populace(self):
        return self.populace


class Game:
    def __init__(self, populace):
        self.populace = populace

    def get_populace(self):
        return self.populace

    def assign_charismas(self):
        random.shuffle(populace)
        for idx in range(0, len(populace)):
            populace[idx].set_charisma(idx)

    def sort_by_charisma(self):
        populace.sort(key=lambda x: x.get_charisma(), reverse=True)

    def check_parity(self):
        num_town = len(list(filter(lambda x: x.get_alignment() == "town", populace)))
        num_mafia = len(list(filter(lambda x: x.get_alignment() == "mafia", populace)))
        if num_mafia >= num_town:
            return True

    def check_town_victory(self):
        num_mafia = len(list(filter(lambda x: x.get_alignment() == "mafia", populace)))
        if num_mafia == 0:
            return True
        return False

    def day_elimination(self):
        self.sort_by_charisma()
        return populace.pop()

    def night_kill(self):
        self.sort_by_charisma()
        idx = next(x for x in list(enumerate(populace)) if x[1].get_alignment() == "town")[0]
        return populace.pop(idx)

    def run(self, print_bool=False):
        self.assign_charismas()
        self.sort_by_charisma()
        day = 1
        running = True
        while running:
            eliminated = self.day_elimination()
            if (print_bool):
                print("Day " + str(day) + ": " + eliminated.get_alignment() + " was eliminated.")
            if (self.check_parity() or self.check_town_victory()):
                running = False
            if (running):
                eliminated = self.night_kill()
                if (print_bool):
                    print("Night " + str(day) + ": " + eliminated.get_alignment() + " was killed.")
            if (self.check_parity() or self.check_town_victory()):
                running = False
                if (print_bool):
                    print("Game over!")
                return self.check_town_victory()
            day += 1


def mountainous(num_town, num_mafia):
    populace = []
    for idx in range(0, num_town):
        player = Player("town", "vanilla")
        populace.append(player)
    for idx in range(0, num_mafia):
        player = Player("mafia", "vanilla")
        populace.append(player)
    return populace


town_victories = 0
mafia_victories = 0
n = 50000


for i in range(0, n):
    populace = mountainous(7, 2)
    game = Game(populace)
    if game.run():
        town_victories += 1
    else:
        mafia_victories += 1


print(town_victories/n)
print(mafia_victories/n)