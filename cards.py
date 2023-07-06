class Submove:    
    def __init__(self):
        self.dmg = None
        self.heal = None
        self.acc = None 
        self.splash = False
        self.cleanse = False
        self.hack = False
        self.effects = []
        

    def __str__(self):
        string = []
        if self.splash:
            string.append("\tSplash Move")
        if self.acc != None:
            if self.acc == "all":
                acc = "guaranteed hit"
            else:
                acc = str(self.acc*100) + "%"

            string.append(f'\tAccuracy: {acc}')
        if self.dmg != None:
            string.append(f'\tDamage: {self.dmg}')
        if self.heal != None:
            string.append(f'\tHeal: {self.heal}')
        if self.cleanse:
            string.append('\tCleanse all negative effects')
        if self.hack:
            string.append('\tRemove all target\'s buffs')
        for effect in self.effects:
            string.append(str(effect))
        if string == []:
            string = '\tNone'
        else:
            string = '\n'.join(string)
        return string

class Move:
    def __init__(self, name):
        self.name = name
        self.tar = Submove()
        self.slf = Submove()
    def __str__(self):
        string = [self.name]
        if str(self.tar) !='\tNone':
            string.append(str(self.tar))
        if str(self.slf) !='\tNone':
            string.append(' Self Effect:')
            string.append(str(self.slf))
        return '\n'.join(string)

class Passive(Move):
    pass

class Card:
    def __init__(self, name, HP, move, cost):
        self.name = name
        self.HP = HP
        self.maxHP = HP
        self.move = move
        self.cost = cost
        self.effects = []
        self.index = None

    def __str__(self):
        string = [self.name]
        string.append(f"HP: {self.HP}")
        string.append(f"Cost: {self.cost}")
        for i in range(len(self.move)):
            if i == 0:
                movenum = "PASSIVE:"
            else:
                movenum = f"MOVE {i}:"
            string.append(f"{movenum} {str(self.move[i])}")
        return '\n'.join(string)

class Effect:
    def __init__(self, type, duration = 1, multiplier = 1):
        self.type = type
        self.duration = duration
        self.multiplier = multiplier

class Buff(Effect):
    def __str__(self):
        duration = self.duration
        if self.multiplier != 1:
            return f'\t+{abs(self.multiplier*100 - 100)}% {self.type} for {duration} turn(s)'
        else:
            return f'\t{self.type} for {duration} moves(s)'

class Debuff(Effect):
    def __str__(self):
        duration = self.duration
        if self.multiplier != 1:
            return f'\t-{abs(self.multiplier*100 - 100)}% {self.type} for {duration} turn(s)'
        else:
            return f'\t{self.type} for {duration} moves(s)'


cardlist = []

#Unused
moves = []
Unused = Card("--", 0, moves, 0)

if True: #Alex
    BodySlam = Move('BodySlam')
    BodySlam.tar.dmg = 90

    CallMommy = Move('CallMommy')
    CallMommy.tar.heal = 75
    CallMommy.tar.acc = "all"

    StopIt = Move("'GUYS STOP'")
    StopIt.tar.effects = [Debuff("stun", 1)]
    StopIt.tar.acc = 0.75

    moves = [None, BodySlam, CallMommy, StopIt]

    Alex = Card("Alex", 200, moves, 5)
    cardlist.append(Alex)

if True: #Brianna
    Spike = Move('VolleyballSpike')
    Spike.tar.dmg = 80
    MakePlans = Move('MakePlans')
    MakePlans.tar.splash = True
    MakePlans.tar.effects.append(Buff("accuracy", 2, 1.5)) 
    CarCrash = Move('CarCrash')
    CarCrash.tar.dmg = 150
    CarCrash.tar.acc = 0.8
    CarCrash.slf.dmg = 100

    moves = [None, Spike, MakePlans, CarCrash]
    Brianna = Card("Brianna",250,moves,7)
    cardlist.append(Brianna)

if True: #Frank
    BrassFist = Move("BrassFist")
    BrassFist.tar.dmg = 80

    Speed = Move('DriveFast')
    Speed.slf.effects = [Buff("evasion", 2, 0.5)]

    Service = Move("8amCustomerService")
    Service.tar.dmg = 30
    Service.tar.effects = [Debuff("antiheal", 2)]

    moves = [None, BrassFist, Speed, Service]
    Frank = Card("Frank", 200, moves, 5)
    cardlist.append(Frank)

if True: #V
    Set = Move('VolleyballSet')
    Set.tar.effects = [Buff("accuracy", 1, 2), Buff("dmgboost", 1, 2)]
    Set.tar.acc = "all"

    BigBandaid = Move('BigBandaid')
    BigBandaid.tar.heal = 100
    BigBandaid.tar.acc = "all"

    Emt = Move('EMT')
    Emt.tar.cleanse = True
    Emt.tar.acc = "all"

    moves = [None, Set, BigBandaid, Emt]
    Veronica = Card("Veronica", 200, moves, 4)
    cardlist.append(Veronica)

if True: #Clare
    Tall = Passive("Tall")
    Tall.slf.effects = [Buff("resistance", 1, .9)]
    ClareShot = Move("ClareShot")
    ClareShot.tar.dmg = 30
    ClareShot.tar.effects = [Debuff("accuracy", 3, 0.75), Debuff("evasion", 3, 1.25)]

    BiggestBird = Move("BiggestBird")
    BiggestBird.tar.dmg = 100
    BiggestBird.slf.dmg = 100

    Block = Move("VolleyballBlock")
    Block.slf.effects = [Buff("shield", 1), Buff("resistance", 1, 0.6)]
    
    moves = [Tall, ClareShot, BiggestBird, Block]
    Clare = Card("Clare", 300, moves, 7)
    cardlist.append(Clare)

if True: #Peter
    SlideTackle = Move("SlideTackle")
    SlideTackle.tar.dmg = 50
    
    PreCalc = Move("99OnPreCalc")
    PreCalc.slf.effects = [Buff("dmgboost", 2, 3)]

    DiscordMod = Move("DiscordMod")
    DiscordMod.tar.hack = True

    ShutUp = Move("STFU Samir")
    ShutUp.tar.splash = True
    ShutUp.tar.effects = [Debuff("stun", 1)]
    ShutUp.tar.acc = 0.4

    moves = [None, SlideTackle, PreCalc, DiscordMod, ShutUp]
    Peter = Card("Peter", 175, moves, 4)
    cardlist.append(Peter)

if True: #Devaney
    Chevy = Move("WhiteChevyTahoe")
    Chevy.tar.dmg = 70
    Chevy.slf.effects = [Buff("evasion", 1, 0.9)]

    Wifi = Move("ShutOffWifi")
    Wifi.tar.splash = True
    Wifi.tar.hack = True

    Blame = Move("BlameGirlfriend")
    Blame.slf.effects = [Buff("invisible", 2)]
    Blame.slf.acc = 0.7

    moves = [None, Chevy, Wifi, Blame]
    Devaney = Card("Devaney", 200, moves, 5)
    cardlist.append(Devaney)

if True: #Dan
    D1Frisbee = Passive("D1Frisbee")
    D1Frisbee.slf.effects = [Buff("accuracy", 1, 1.1)]

    GuitarRiff = Move("BuddyHollyRiff")
    GuitarRiff.tar.splash = True
    GuitarRiff.tar.dmg = 50

    DweltAmongUs = Move("DweltAmongUs")
    DweltAmongUs.tar.splash = True
    DweltAmongUs.tar.effects = [Buff("resistance", 1, .5)]

    MaidCostume = Move("MaidCostume")
    MaidCostume.tar.splash = True
    MaidCostume.tar.effects = [Debuff("confuse", 1)]
    MaidCostume.tar.acc = 0.8

    moves = [D1Frisbee, GuitarRiff, DweltAmongUs, MaidCostume]
    Dan = Card("Dan", 200, moves, 6)
    cardlist.append(Dan)



if True: #Dean
    Tolerance = Passive("FratGuyTolerance")
    Tolerance.slf.effects = [Buff("resistance", 1, 0.8)]

    Puke = Move("Puke")
    Puke.tar.splash = True
    Puke.tar.dmg = 40
    Puke.tar.effects = [Debuff('poison', 2)]

    FootStank = Move("FootStank")
    FootStank.tar.effects = [Debuff("stun", 1)]
    FootStank.tar.acc = 0.8

    ShaveHead = Move("ShaveHead")
    ShaveHead.tar.effects = [Debuff("confuse", 2)]
    ShaveHead.slf.dmg = 40

    moves = [Tolerance, Puke, FootStank, ShaveHead]
    Dean = Card("Dean",150, moves, 4 )
    cardlist.append(Dean)
    

if True: #Tim
    Bakery = Passive("Bakery")
    Bakery.slf.heal = 20

    BigFart = Move("BIGFART")
    BigFart.tar.dmg = 80
    BigFart.tar.effects = [Debuff("accuracy", 1, 0.9)]
    
    ProteinPowder = Move("ProteinPowder")
    ProteinPowder.slf.heal = 80
    ProteinPowder.slf.effects = [Buff("dmgboost", 1, 1.5)]

    Motorcycle = Move("Motorcycle")
    Motorcycle.tar.splash = True
    Motorcycle.tar.effects = [Buff("evasion", 1, 0.5)]

    moves = [Bakery, BigFart, ProteinPowder, Motorcycle]
    Tim = Card("Tim", 225, moves, 6)
    cardlist.append(Tim)


if True: #Lily
    Slap = Move("SlapTim")
    Slap.tar.dmg = 50

    Gossip = Move("Gossip")
    Gossip.tar.splash = True
    Gossip.tar.effects = [Debuff("antiheal", 2)]

    moves = [None, Slap, Gossip]
    Lily = Card("Lily", 175, moves, 3)
    cardlist.append(Lily)



if True: #Samir
    QuickLearner = Passive("QuickLearner")
    QuickLearner.slf.effects = [Buff("accuracy", 1, 1.25)]

    RightHook = Move("RightHook")
    RightHook.tar.dmg = 40
    RightHook.slf.effects = [Buff("dmgboost", "all", 2)]    

    DarkSouls = Move("DarkSouls")
    DarkSouls.slf.effects = [Buff("evasion", 3, 0.7)]

    Hospitality = Move("Hospitality")
    Hospitality.tar.splash = True
    Hospitality.tar.heal = 60
    Hospitality.tar.acc = "all"

    moves = [QuickLearner, RightHook, DarkSouls, Hospitality]
    Samir = Card("Samir", 250, moves, 6)
    cardlist.append(Samir)


if True: #Dylan
    MartialArts = Move("MartialArts")
    MartialArts.tar.dmg = 80

    Workout = Move("Workout")
    Workout.slf.effects = [Buff("dmgboost", "all", 2), Buff("resistance", 1, 0.75)]

    CookRamen = Move("CookRamen")
    CookRamen.slf.heal = 100

    moves = [None, MartialArts, Workout, CookRamen]
    Dylan = Card("Dylan", 250, moves, 6)
    cardlist.append(Dylan)


if True: #Andrew
    Toxic = Move("TOXIC")
    Toxic.tar.dmg = 60
    Toxic.tar.effects = [Debuff("poison", 3)]

    FactsAndLogic = Move("FactsAndLogic")
    FactsAndLogic.tar.effects = [Debuff("resistance", 1, 1.5), Debuff("dmgboost", 1, 0.5)]

    Roulette = Move("Roulette")
    Roulette.tar.acc = 0.5
    Roulette.tar.dmg = 150
    Roulette.slf.dmg = 150
    Roulette.slf.acc = 0.5

    moves = [None, Toxic, FactsAndLogic, Roulette]
    Andrew = Card("Andrew", 150, moves, 4)
    cardlist.append(Andrew)



while True:
    switchcount = 0
    for i in range(0, len(cardlist)-1):
        temp = cardlist
        card1 = cardlist[i]
        card2 = cardlist[i+1]
        if card1.cost < card2.cost:
            switchcount+=1
            temp[i] = card2
            temp[i+1] = card1
    if switchcount == 0:
        cardlist = temp
        break

cardstrings = []
for each in cardlist:
    cardstrings.append(str(each))

f = open("cardinfo.txt", "w")
f.write("\n\n".join(cardstrings))
f.close()






