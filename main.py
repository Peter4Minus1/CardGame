import random
from copy import deepcopy

from cards import cardlist
from cards import Unused
from cards import Buff, Debuff, Passive



def roll(acc):
    pctMiss = 100 - acc*100
    hit = True
    if pctMiss > 0:
        print("Need " + str(pctMiss))
        roll = random.randint(0,100)
        print("Rolled " + str(roll))

        if roll >= pctMiss:
            hit = True
            print("Hit")
        else:
            hit = False
            print("Miss")
    return hit

def hasEffect(card, effect):
    flag = False
    for e in card.effects:
        if e.type == effect:
            flag = True
    return flag

def usemove(move, x, order):
    self = order[x]

    if str(move.tar) != '\tNone':
        choice = 0
        while choice != "1" and choice != "2":
            print("(1) Team 1:")
            for each in lineups[0]:
                print(f'\t{each.name}')

            print("(2) Team 2:")
            for each in lineups[1]:
                print(f'\t{each.name}')

            choice = input(f"Which team would you like to target?\n")
        targetteam = []
        for i, card in enumerate(order):
            if choice == '1' and i%2 == 0:
                targetteam.append(card)
            elif choice == '2' and i%2 == 1:
                targetteam.append(card)
        targetlist = []
        if move.tar.splash == True:
            targetlist = targetteam
        else:
            while True:

                teamhasshield = False
                for card in targetteam:
                    if hasEffect(card, "shield"):
                        teamhasshield = True

                for card in targetteam:
                    if teamhasshield and not(hasEffect(card, "shield")):
                        targetteam.remove(card)


                print(f"Targeted Team:")
                for i, each in enumerate(targetteam, 1):
                    print(f"\t({i}) {each.name}")
                targetindex = input("Choose a target:\n")
                try:
                    targetindex = int(targetindex)-1
                except:
                    pass
                else:
                    if targetindex in range(len(targetteam)):
                        break
            targetlist.append(targetteam[targetindex])

        confused = False
        for effect in self.effects:
            if effect == "confuse":
                confused = True
        
        
        if move.tar.acc == "all":
            hit = True
        else:
            if confused:
                if roll(.5):
                    targetlist = [self]
                    print(f"{self.name} hits itself in confusion")

            accuracy = 1
            for target in targetlist:
                if move.tar.acc != None:
                    accuracy *= move.tar.acc
                for effect in self.effects:
                    if effect.type == 'accuracy':
                        accuracy *= effect.multiplier
                if hasEffect(self, "invisible"):
                    accuracy *= 0

                if move.tar.splash != True:
                    for effect in target.effects:
                        if effect.type == "evasion":
                            accuracy *= effect.multiplier
                    if hasEffect(target, "invisible"):
                        accuracy *= 0

            hit = roll(accuracy)
        if hit:
            for target in targetlist:
                if move.tar.dmg != None:
                    damage = move.tar.dmg
                    for effect in self.effects:
                        if effect.type == "dmgboost":
                            damage *= effect.multiplier

                    for effect in target.effects:
                        if effect.type == "resistance":
                            damage *= effect.multiplier
                    target.HP -= damage
                if move.tar.cleanse == True:
                    removeeffects(target, "debuff")
                if move.tar.hack == True:
                    removeeffects(target, "buff")
                if move.tar.heal != None:
                    heal = move.tar.heal
                    if hasEffect(target, "antiheal"):
                        heal = 0
                    target.HP += heal
                    if target.HP > target.maxHP:
                        target.HP = target.maxHP
                for effect in move.tar.effects:
                    e = deepcopy(effect)
                    target.effects.append(e)
                    if e.duration != "all":
                        e.duration *= 4
                        e.duration += 1
                    print(e)
            order[target.index] = target
        else:
            print("Miss")

    
    if str(move.slf) != '\tNone':
        accuracy = 1
        if move.slf.acc != None:
            accuracy *= move.slf.acc
        for effect in self.effects:
            if effect.type == 'accuracy':
                accuracy *= effect.multiplier
        selfhit = roll(accuracy)
        if selfhit:
            if move.slf.dmg != None:
                self.HP -= move.slf.dmg
            if move.slf.heal != None:
                heal = move.slf.heal
                if hasEffect(self, "antiheal"):
                    heal = 0
                self.HP += heal
                if self.HP > self.maxHP:
                    self.HP = self.maxHP
            if move.slf.cleanse:
                removeeffects(self, "debuff")
            if move.slf.hack:
                removeeffects(self, "buff")
            for effect in move.slf.effects:
                e = deepcopy(effect)
                self.effects.append(e)
                if e.duration != "all":
                    e.duration *= 4
                    if not(isinstance(move, Passive)):
                        e.duration += 1
                print(e)
        
        else:
            print("Miss")

        order[x] = self
    
    return order

def convert(string):
    value = 0
    for card in cardlist:
        if card.name.lower() == string.strip().lower():
            value = card
    return value
    
def switch(t):
    for i, each in enumerate(teams[t]):
        print(f'({i+1}) {each.name}')
    choice = input("Add card to your lineup:\n")
    replacement = teams[t][int(choice)-1]
    try:
        teams[t].remove(replacement)
        return deepcopy(replacement)
    except:
        return None

def display(x,order):
    for i in range(len(order)):
        if x==i:
            print (f'>> {order[i].name}')
        else:
            print (order[i].name)

        print(f"\tHP: {order[i].HP}/{order[i].maxHP}")

        for effect in order[i].effects:
            print(str(effect))
    print("\n")
def removeeffects(target, type):
    effects = []
    if type == "all":
        pass

    elif type == "buff":
        for effect in target.effects:
            if isinstance(effect, Debuff):
                effects.append(effect)

    elif type == "debuff":
        for effect in target.effects:
            if isinstance(effect, Buff):
                effects.append(effect)
    target.effects = effects
    




teams = []
for i in range(1,3):
    team = []
    points = 25
    while True:
        
        cardstrings = []
        for each in cardlist:
            cardstrings.append(f"{each.name} - ({each.cost})")
        print("\n".join(cardstrings))
        print("Your Team:")
        for each in team:
            print("\t"+ each.name)
        print(f'Points: {points}')
        choice = input(f"Player {i} choose a card:\n") 
        help = False 
        if choice[0] == '?':
            choice = choice[1:]
            choice = convert(choice)
            if choice != 0:
                print(str(choice))
                input()
        elif choice == "end":
            print(team)
            teams.append(team)
            break
        else:
            choice = convert(choice)
            if choice not in team and choice != 0:
                affordable = (points - choice.cost >= 0)
                if affordable:
                    team.append(choice)
                    points -= choice.cost
print(teams)
lineups = [[],[]]
for i in range(2):
    for j in range (2):
        print(f'Team {j+1}:')
        starter = None
        while starter == None:
            starter = switch(j)
        lineups[j].append(starter)       

        

order = []
for i in range(len(lineups[0])):
    for j in range(len(lineups)):
        order.append(deepcopy(lineups[j][i]))
print(order)

for i in range(len(order)):
    if order[i].move[0] != None:
        print(f"{order[i].name}'s Passive:")
        usemove(order[i].move[0], i, order)
        input("Press Enter")
    for e in order[i].effects:
        e.duration = i+1
while True:
    for x, moving in enumerate(order):
        moving.index = x
    for x in range(len(order)):
        moving = order[x]
        display(x, order)
        print(f"Player {x%2 + 1}'s Turn:")

        stunned = False
        confused = False
        poisoned = False
        for effect in moving.effects:
            if effect.type == 'stun':
                stunned = True
            if effect.type == "poison":
                poisoned = True
        if poisoned:
            moving.HP -= 20

        if not(stunned) and moving.move[0] != None:
            print(f"{moving.name}'s Passive: {moving.move[0].name}\n{moving.move[0].slf}")
            usemove(moving.move[0], x, order)

        if not(stunned):
            print(f"{moving.name}: ")

            for i in range(1, len(moving.move)):
                print(f"\t({i}) {moving.move[i].name}")
            print("\t(SWITCH)")
        else:
            input('SKIP')
        
        while True:
            loop = False
            if order[x] == Unused:
                choice == 'SKIP'
            elif stunned:
                choice == 'SKIP'
            else:
                choice = input("Choose a move:")

                try:
                    selected = int(choice)
                
                except:
                    if choice.strip().upper() == 'SWITCH'and len(teams[x%2]) > 0:
                        lineups[x%2].remove(moving)
                        if moving.HP > 0:
                            teams[x%2].append(moving)
                        print(f'Team {x%2+1}')
                        order[x] = switch(x%2)
                        lineups[x%2].append(order[x])
                    elif choice.strip() == "?":
                        loop = True
                        print(f"{moving.name}: ")
                        for i in range(1, len(moving.move)):
                            print(f"({i}) {moving.move[i]}")
                    else:
                        loop = True
                else:
                    order = usemove(moving.move[selected], x, order)

            if loop == False:
                    break

        l1 = []
        l2 = []
        for i, card in enumerate(order):
            
            if i%2 == 0:
                l1.append(card)
            else:
                l2.append(card)
        lineups[0] = l1
        lineups[1] = l2

        #checking for deaths

        for i in range(len(order)):
            card = order[i]
            if card.HP <= 0 and card != Unused:
                lineups[i%2].remove(card)
                card.effects = []

                if teams[i%2] != []:
                    print(f'Team {i%2+1}')
                    order[i] = switch(i%2)
                else:
                    order[i] = Unused

                lineups[i%2].append(order[i])
                    
            effectlist = deepcopy(card.effects)       
            for effect in effectlist:
                if effect.duration != "all":
                    effect.duration -= 1
                if effect.duration == 0:
                    card.effects.remove(effect)
        
    count = 0
    for i in lineups[0]:
        if i == Unused:
            count += 1
    if count == len(lineups[0]):
        Team1Win = False
        break
    
    count = 0
    for i in lineups[1]:
        if i == Unused:
            count += 1
    if count == len(lineups[0]):
        Team1Win = True
        break

if Team1Win:
    print("Team 1 Wins")  
else:
    print("Team 2 Wins")
        
        