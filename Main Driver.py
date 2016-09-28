import random
import time
import linecache
import Turns

class playerstats():
    def __init__(self):
        self.health = 50
        self.cash = 0
        self.focus = 1
        self.item = ""
        self.DamMod = 0
        self.prepcount = 0
        self.itemlist = []
#This is creating a class for the player; it means I dont need to send every single variable inbetween functions

class enemystats():
    def __init__(self):
        self.health = 50
        self.name = ""
        self.type = 0
        self.accuracy = 10
#This class is containing statistics about the enemy

class gameinfo():
    def __init__(self):
        self.alive = 1
        self.play = 1
        self.fights = 0
        self.boss = 0

def LoadEnemy(game):
    if game.boss == 0:
        filename = "EnemyList.txt"
    elif game.boss == 1:
        filename = "BossList.txt"
    for i, line in enumerate(file):
        TotalLines = i
    TotalLines += 1
    enemytofight = int(random.randint(1, TotalLines + 1))   
    EnemyInfo = linecache.getline(filename, enemytofight)
    print(EnemyInfo)
    EnemyFought = (EnemyInfo.split(" "))
    EnemyFought[2] = EnemyFought[2].replace("\n", "")
    EnemyFought[0] = EnemyFought[0].replace("_", " ")
    EnemyFought[1] = int(EnemyFought[1])
    EnemyFought[2] = int(EnemyFought[2])
    linecache.clearcache()
    file.close()
    return EnemyFought

def ShopPhase(player):
    with open("Stock.txt") as f:
        stock = [line.strip('\n') for line in f.readlines()]    
    for x in range (0, len(stock)):
        stock[x] = stock[x].split(" ")
        stock[x][0] = stock[x][0].replace("_", " ")
        stock[x][1] = int(stock[x][1])
    print(stock)
    print("")
    print("Welcome to the shop!\n")
    time.sleep(1)
    print("We have a selection of fine wares available here. Take a pick!")
    print("You have "+str(player.cash)+" gold available.")
    time.sleep(1)
    print("")
    for x in range (len(stock)):
        print (str(x+1)+")"+stock[x][0]+" : "+str(stock[x][1])+" gold.")
    print("")
    print("Please type the number of which option you select.")
    print("Or type q to leave")
    selection = "a"
    leave = 0

    while not selection.isdigit():
        selection = str(input())
        if not selection.isdigit():
            if not selection[0].upper() == "Q":
                print("That is not a correct input, please retry.")
            elif selection[0].upper() == "Q":
                leave = 1
                selection = "1"

    selection = int(selection)
    selection = selection - 1
    
    if leave == 0:
        for x in range (len(stock)):
            if selection == x:
                print ("You have selected "+stock[x][0])
                break;

        if stock[selection][1] <= player.cash:
            time.sleep(1)
            print("You have purchased "+stock[selection][0]+"!")
            player.cash = player.cash - stock[selection][1]
            time.sleep(1)
            print("You now have "+str(player.cash)+" gold!")
            player.itemlist.append(stock[selection][0])
        else:
            print("You 'avent got enough gold you wally! Get out!")
    else:
        print("Fair enough, have a good one!")
    return player

def IntroduceEnemy(enemy):
    if enemy.type == 0:
        print("A "+enemy.name+" has entered the arena!")
    elif enemy.type == 1:
        print("A wild "+enemy.name+" is released into the arena!")
    time.sleep(1)
    print("The enemy has "+str(enemy.health)+" health!")

def PlayGame(player, prepared, focused, enemy):
    turn = 1
    while player.health !=0 and enemy.health !=0:
        if turn == 1:
            print("")
            time.sleep(1)
            print ("your attack!")
            player, prepared, focused, enemy = Turns.turnmenu(player, prepared, focused, enemy)
            turn = 0
        elif turn == 0:
            print("")
            time.sleep(1)
            print ("enemy attack!")
            player = Turns.enemyattack(player, enemy)
            turn = 1
    return player, prepared, focused, enemy

def PostGame(player, game, enemy):
    if player.health != 0:
        game.fights += 1
    if player.health == 0:
        print ("you died! unlucky!")
        print("")
        print("You have won "+str(game.fights)+" fights!")
        PlayAgain = 1
        while PlayAgain != "Y" and PlayAgain != "N":
            PlayAgain = input("Would you like to play again? (Yes/No) ")
            PlayAgain = PlayAgain[0].upper()
            if PlayAgain == "Y":
                game.alive = 1
                game.play = 0
            else:
                game.alive = 0
                game.play = 0
    else:
        print("")
        print ("the enemy died! hooray!")
        print("")
        print("You have won "+str(game.fights)+" fights!")
        cashearned = random.randint(1, 10)
        if game.boss == 1:
            cashearned += 10
        player.cash = player.cash + cashearned
        time.sleep(1)
        print("")
        print("You have found "+str(cashearned)+" gold!")
        print("You now have "+str(player.cash)+" gold!")
        player.health += 15
        if player.health > 50:
            player.health = 50
        time.sleep(1)
        print("")
        print("you have restored 15 health! You now have "+str(player.health)+" health!")
        shopping = 1
        time.sleep(1)
        print("")
        print("Would you like to go shopping? (Yes/No) ")
        while shopping != "Y" and shopping != "N":
            shopping = str(input())
            shopping = shopping[0].upper()
            if shopping != "Y" and shopping != "N":
                print("That is not a valid option, please enter a new value.")
            if shopping == "Y":
                player = ShopPhase(player)
            elif shopping == "N":
                print("")
                print("So be it! We didn't want you anyway!")
        enemy = enemystats()
        if (game.fights % 3) == 0:
            game.boss = 1
        else:
            game.boss = 0
    return player, game, enemy

if __name__ == "__main__":
    game = gameinfo()
    game.alive = 1
    while game.alive == 1:
        prepared = 0
        focused = 0
        player = playerstats()
        enemy = enemystats()
        player.itemlist = ["Health potion", "Weapon Poison", "Luck potion"]        
        game.fights  = 0
        game.play = 1
        game.boss = 0
        while game.play == 1:
            print ("welcome to the arena!")
            EnemyFought = LoadEnemy(game)
            enemy.health = EnemyFought[2]
            enemy.name = EnemyFought[0]
            IntroduceEnemy(enemy)
            player, prepared, focused, enemy = PlayGame(player, prepared, focused, enemy)
            time.sleep(1)
            player, game, enemy = PostGame(player, game, enemy)         
