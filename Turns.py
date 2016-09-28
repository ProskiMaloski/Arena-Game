import time
import random

def playerattack(player, prepared, focused, enemy ):
    #This is the function where the logic behind player attacks takes place
    print("")
    crit = 0
    accuracy = 80
    #Here we set up the initial critical chance and accuracy; these are local to this function
    time.sleep(1)
    print("You swing your sword!")
    hitchance = random.randint(1, 100)
    #This is the chance of the player hitting the enemy. The value must be below the value of accuracy to successfully damage the enemy

    #dealing with preparing
    if prepared == 1:
        hitchance = hitchance - player.prepcount*10
        prepared = 0
        player.prepcount = 0
        #The preparing mechanic affects the likelihood of a hit. The chance gets reset upon an attack

    critchance = random.randint(1, 100)
    #Setting a chance to land a critical hit

    if player.item == "Luck potion":
        critchance = critchance - 74
        if critchance == 0 or critchance < 0:
            critchance = 1
            #using a luck potion increases the chance of landing a critical hit by 75%; to do this I just reduce the critchance by 74. This gives it a higher chance of being below 5.
        player.item = ""
        print("")
        print("Luck potion was successful!")

    time.sleep(1)
    #paces out the game, so that the user isnt flooded with information
    
    #asking what type of attack
    if hitchance > accuracy:
        miss = True
    else:
        miss = False
    #Just asking if the player missed the attack or not

    if (hitchance < accuracy or hitchance == accuracy) and hitchance > 49:  #high chance of hit
        glance = True #This is the attack that does the least damage.
        solid = False #This does a medium amount of damage
        special = False #This is a heavy blow; does the most damage
    elif hitchance < 50 and hitchance > 5: #highest chance of hit
        solid = True
        special = False
        glance = False
    elif hitchance < 6: #lowest chance of hit
        special = True
        glance = False
        solid = False
    
    #decides if the attack is critical crit
    if critchance > 0 and critchance < 6:
        crit = True
    else:
        crit = False
    
    #main attack phase
    if miss == False:
        if glance == True:
            damage = random.randint(1, 5) #randomly decides how much damage is dealt based on the accuracy of the attack
        elif solid == True:
            damage = random.randint(6, 10)
        elif special == True:
            damage = random.randint(11, 15) #change these if quick kills are needed FOR TESTING

        #This is an effect added by items; if there is a damage modifier, then its applied to the total damage and reset
        if player.DamMod != 0:  
            print("The weapon is poisoned!")
            damage = damage + player.DamMod
            player.DamMod = 0

        #Text to inform the player on what type of attack they landed
        if glance == True:
            print("You hit the enemy with a glancing blow!")
        elif solid == True:
            print ("You hit the enemy with a solid attack!")
        elif special == True:
            print("You land a lucky blow!")

        #an effect added by items; a damage multiplier
        if focused == 1: 
            damage = damage * player.focus
            player.focus = 1
            focused = 0

        #the damage is made in a priority order; first defined by accuracy, then damage modifiers are added, then its affected by focus, and finally critical hits
        if crit == True:
            print ("It was a critical hit!")
            damage = damage**2
        
        #this is where the damage is applied to the enemy, with text informing the user upon how much damage they've done and the remaining damage needed./
        print ("You dealt "+str(damage)+" damage!")
        enemy.health = enemy.health - float(damage)
        if enemy.health < 0:
            enemy.health = 0
        print ("The enemy has "+str(enemy.health)+" health left!")
    else:
        print ("You miss your attack!")
    return player, prepared, focused, enemy 

#this function controls the enemy attack phase
def enemyattack(player, enemy):
    print("")
    crit = 0
    accuracy = 70
    time.sleep(1)
    #defining the starting variables
    
    if enemy.type == 0:
        print("The enemy swings their weapon!")
    elif enemy.type == 1:
        print ("The enemy swipes at you!")
    #controlling what the game prints when the enemy attacks, based on it's type
    
    hitchance = random.randint(0, 100)
    critchance = random.randint(0, 100)
    #randomly making the chance of hitting the enemy, and the chance of a crit
    
    #logic behind whether enemy crit is true or false
    if critchance < 5:
        crit = 1
    else:
        crit = 0

    #the main block as to whether to enemy hits you or not
    time.sleep(1)
    if hitchance < accuracy or hitchance == accuracy:
        #how much damage is dealt
        damage = random.randint(1,10)
        if crit == 1:
            damage = damage*1.5
        print ("The enemy hit you!")
        if crit == 1:
            print ("It was a critical hit!")
        print ("They dealt "+str(damage)+" damage!")
        player.health = player.health - damage
        if player.health < 0:
            player.health = 0
        print ("You have "+str(player.health)+" health left!")
    else:
        print ("They miss their attack!")
    return player

#the area where the player selects what they want to do on their turn
def turnmenu(player, prepared, focused, enemy):
    #x is here so that the turn menu is always running while the enemy hasnt made a correct choice
    x = True
    while x == True:
        #asking the player what they want to do
        print("")
        print("This turn you can:\n1) Attack\n2) Prepare\n3) Focus\n4) Use an item")
        act = str(input("Which would you like to do?  "))
        if act.isdigit():
            act = int(act)
        #attack the enemy
        if act == 1:
            player, prepared, focused, enemy  = playerattack(player, prepared, focused, enemy )
            x = False
            return player, prepared, focused, enemy
        
        #prepare for the next attack; increase accuracy
        elif act == 2:
            time.sleep(1)
            print ("")
            print ("You prepare for your next attack! You feel more accurate!")
            player.prepcount = player.prepcount + 1
            time.sleep(1)
            print ("")
            print ("Your next attack will be "+str(10*player.prepcount)+"% more accurate!")
            prepared = 1
            x = False
            return player, prepared, focused, enemy 
        
        #focus on the next attack; increase damage
        elif act == 3:
            time.sleep(1)
            print("")
            print ("You focus on your next attack! You feel more powerful!")
            player.focus = player.focus + 0.5
            time.sleep(1)
            print("")
            print ("Your next attack will be "+str(player.focus)+"x more powerful!")
            focused = 1
            x = False
            return player, prepared, focused, enemy
        
        #select an item to use
        elif act == 4:
            player, ItemUsed = itemselect(player)
            if ItemUsed:
                x = False
                return player, prepared, focused, enemy
            elif not ItemUsed:
                x = True
        else:
            print ("That is not a valid option try again")
        
def itemselect(player):
    #telling the player their items
    time.sleep(1)
    print("")
    print ("Your items are:")    
    #iterates through the item list, telling the player all of the items
    for x in range (len(player.itemlist)):
        print (str(x)+")"+player.itemlist[x])

    print("Which item would you like to use? Type Q to cancel: ")
    selection = "a"
    #makes selection "a" so that the loop can start
    #if the player types Q, it breaks ther loop
    while not selection.isdigit() and selection != "Q":
        selection = str(input())
        if not selection.isdigit():
            if selection == "Q":
                print("OK, returning to the turn menu")
            else:
                print("That is not a correct input, please retry.")
    #asks if they actually chose an item
    if selection.isdigit():
        selection = int(selection)
        for x in range (len(player.itemlist)):
            #if the item has an immediate effect, it is used here
            if selection == x:
                player.item = player.itemlist[x]
                print ("You have selected "+player.itemlist[x])
                player.itemlist.remove(player.itemlist[x])

                if player.item == "Health potion":
                    player.health = player.health + 10
                    if player.health > 50:
                        player.health = 50
                    time.sleep(1)
                    print("")
                    print("You now have "+str(player.health)+" Health!")
                    player.item = ""

                elif player.item == "Weapon Poison":
                    player.DamMod += 8
                    print("")
                    print("You have applied a deadly coat of poison to your weapon!")
                    player.item = ""
        ItemUsed = True
    else:
        ItemUsed = False
    return player, Itemused
