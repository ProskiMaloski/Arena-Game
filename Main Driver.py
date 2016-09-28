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
        0
        self.boss = 0

#this loads an enemy at random from an external file
def LoadEnemy(game):
    #asks if the enemy is a boss or not
    if game.boss == 0:
        file = open("EnemyList.txt", "r")
        filename = "EnemyList.txt"
    elif game.boss == 1:
        file = open("BossList.txt", "r")
        filename = "BossList.txt"
    #counts how many enemies there are in the file, so the game knows the limits of the random number
    for i, line in enumerate(file):
        TotalLines = i
    #adding +1 to the total lines, so that the last enemy in the list is included
    TotalLines += 1
    #generates which enemy to fight
    enemytofight = int(random.randint(1, TotalLines))
    #every enemy is on a seperate line in the text file, so it gathers information on an enemy by randomly selecting which
    #line to get information from, using linecache
    EnemyInfo = linecache.getline(filename, enemytofight)
    #splits the single line string into an array, with all information on the enemy
    EnemyFought = (EnemyInfo.split(" "))
    #gets rid of the \n that is automatically at the end of a line
    EnemyFought[2] = EnemyFought[2].replace("\n", "")
    #replaces underscores with spaces so that the UI output looks nicer
    EnemyFought[0] = EnemyFought[0].replace("_", " ")
    #converts any values that should be integers to integers
    EnemyFought[1] = int(EnemyFought[1])
    EnemyFought[2] = int(EnemyFought[2])
    #clears the linecache cache
    linecache.clearcache()
    #closes the file
    file.close()
    return EnemyFought

#this is where the player buys an item
def ShopPhase(player):
    #the stock never changes, so whenever the function is loaded it reloads the stock text file to read from
    with open("Stock.txt") as f:
        #this appends every line from stock into the stock array in python
        stock = [line.strip('\n') for line in f.readlines()]    
    for x in range (0, len(stock)):
        #formats the information about the stock, so it looks better
        stock[x] = stock[x].split(" ")
        stock[x][0] = stock[x][0].replace("_", " ")
        #converts the price (stock[x][1]) to an integer
        stock[x][1] = int(stock[x][1])
    #printing information to the player to help how easy it is to use
    print("")
    print("Welcome to the shop!\n")
    time.sleep(1)
    print("We have a selection of fine wares available here. Take a pick!")
    print("You have "+str(player.cash)+" gold available.")
    time.sleep(1)
    print("")
    #uses iteration to print all the items in the stock array
    for x in range (len(stock)):
        print (str(x+1)+")"+stock[x][0]+" : "+str(stock[x][1])+" gold.")
    print("")
    print("Please type the number of which option you select.")
    print("Or type q to leave")
    #makes selection a to start the iteration
    selection = "a"
    #if they choose to leave the shop, the letter Q breaks the loop, and changes a variable to inform the player has left
    leave = 0

    while not selection.isdigit():
        #only strings can be put through the .isdigit() function
        selection = str(input())
        if not selection.isdigit():
            if not selection[0].upper() == "Q":
                print("That is not a correct input, please retry.")
            elif selection[0].upper() == "Q":
                leave = 1
                #this converts selection to a number, so the game wont break when it tries to convert it to an integer
                selection = "1"

    #make selection an integer so it can be used for iteration
    selection = int(selection)
    selection = selection - 1
    
    #if the player didnt leave, iterate through the stock to see which item the player chose to buy
    if leave == 0:
        for x in range (len(stock)):
            if selection == x:
                #if the game finds the item the player chose, it breaks from the loop
                print ("You have selected "+stock[x][0])
                break;

        #asks if the player has enough money to buy the item
        if stock[selection][1] <= player.cash:
            time.sleep(1)
            print("You have purchased "+stock[selection][0]+"!")
            player.cash = player.cash - stock[selection][1]
            time.sleep(1)
            print("You now have "+str(player.cash)+" gold!")
            #maths to remove the price from the players cash pool, then append the item to the players inventory
            player.itemlist.append(stock[selection][0])
        else:
            #if the player hasnt got enough money, theyre kicked out.
            print("You 'avent got enough gold you wally! Get out!")
    else:
        print("Fair enough, have a good one!")
    return player

#introduce the enemy youre fighting
def IntroduceEnemy(enemy):
    if enemy.type == 0:
        print("A "+enemy.name+" has entered the arena!")
    elif enemy.type == 1:
        print("A wild "+enemy.name+" is released into the arena!")
    time.sleep(1)
    print("The enemy has "+str(enemy.health)+" health!")

#the main block of code to run the iteration of turns between the enemy and the player
def PlayGame(player, prepared, focused, enemy):
    turn = 1
    #iterates until a character is dead
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

#the function that runs as of completion of the game
def PostGame(player, game, enemy):
    #if the player isnt dead, increase their health by 1
    if player.health != 0:
        game.fights += 1
    #if the player is dead, inform the player of this and ask if they want to play again
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
        #inform the player how many fights they have won
        print("You have won "+str(game.fights)+" fights!")
        #calculate what the player earned from the fight
        cashearned = random.randint(1, 10)
        #if the enemy was a boss, the player gets an additional 10 gold
        if game.boss == 1:
            cashearned += 10
        player.cash = player.cash + cashearned
        time.sleep(1)
        print("")
        #tell the player how much cash they got, and how much they have now
        print("You have found "+str(cashearned)+" gold!")
        print("You now have "+str(player.cash)+" gold!")
        #restore the player for 15 health
        player.health += 15
        if player.health > 50:
            player.health = 50
        time.sleep(1)
        print("")
        print("you have restored 15 health! You now have "+str(player.health)+" health!")
        #begin asking if the player wants to go shopping
        shopping = 1
        time.sleep(1)
        print("")
        print("Would you like to go shopping? (Yes/No) ")
        #iterates while the player hasnt input a correct input
        while shopping != "Y" and shopping != "N":
            shopping = str(input())
            #so the program only checks the first letter of the players input
            shopping = shopping[0].upper()
            if shopping != "Y" and shopping != "N":
                #informs the player of an incorrect input, weird order i know
                print("That is not a valid option, please enter a new value.")
            if shopping == "Y":
                #runs the shop phase
                player = ShopPhase(player)
            elif shopping == "N":
                #a fun message to tell the player they didnt go shopping
                print("")
                print("So be it! We didn't want you anyway!")
        #resets information about the enemy
        enemy = enemystats()
        #calculation to check if its time for a boss fight, aka every 3 fights
        if (game.fights % 3) == 0:
            game.boss = 1
        else:
            game.boss = 0
    return player, game, enemy

#main module
if __name__ == "__main__":
    game = gameinfo()
    game.alive = 1
    #wont run if the player wants to quit. Runs upon every restart
    while game.alive == 1:
        prepared = 0
        focused = 0
        player = playerstats()
        enemy = enemystats()
        player.itemlist = ["Health potion", "Weapon Poison", "Luck potion"]        
        game.fights  = 0
        game.play = 1
        game.boss = 0
        #defining key values
        #runs while the player is alive
        while game.play == 1:
            print ("welcome to the arena!")
            #loads an enemy
            EnemyFought = LoadEnemy(game)
            #tells the game the enemy health, name and type
            enemy.health = EnemyFought[2]
            enemy.name = EnemyFought[0]
            enemy.type = EnemyFought[1]
            #introduce the enemy to the player
            IntroduceEnemy(enemy)
            #start the game
            player, prepared, focused, enemy = PlayGame(player, prepared, focused, enemy)
            time.sleep(1)
            #post-game code
            player, game, enemy = PostGame(player, game, enemy) 
