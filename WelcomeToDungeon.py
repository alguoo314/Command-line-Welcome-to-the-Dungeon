# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the game "Welcome to the dungeon"
"""

import os
import random

"""
    Necessary items
"""
allEquipment = (("Polymorph: \t\t\t\t Replace one Monster you draw with the next Monster from the deck (once per Dungeon).",
                    "Demonic Pact: \t\t\t Defeat the Demon and the next Monster.", 
                    "Holy Grail: \t\t\t\t Defeat Monsters with even-numbered strength.", 
                    "Omnipotence: \t\t\t\t If all the Monsters in the Dungeon are different, you win the round.", 
                    "Wall of Fire: \t\t\t HP + 6",
                    "Bracelet of Protection: \t HP + 3"), 
                 ("Torch: \t\t\t Defeat Monsters with strength 3 or less.",
                    "Dragon Spear: \t Defeat the Dragon.", 
                    "Holy Grail: \t\t Defeat Monsters with even-numbered strength.", 
                    "Vorpal Sword: \t Defeat one Monster that you choose before entering the Dungeon.", 
                    "Plate Armor: \t\t HP + 5",
                    "Knight Shield: \t HP + 3"), 
                 ("Invisibility Cloak: \t Defeat Monsters with strength 6 or more.",
                    "Ring of Power: \t\t Defeat Monsters with strength 2 or less. Add their total strength to your HP.", 
                    "Healing Potion: \t\t When you die, come back to life with your Adventurer's HP (once per Dungeon).", 
                    "Vorpal Sword: \t\t Defeat one Monster that you choose before entering the Dungeon.", 
                    "Mithril Armor: \t\t HP + 5",
                    "Buckler: \t\t\t\t HP + 3"), 
                 ("Torch: \t\t\t Defeat Monsters with strength 3 or less.",
                    "War Hammer: \t\t Defeat Golems.", 
                    "Healing Potion: \t When you die, come back to life with your Adventurer's HP (once per Dungeon).", 
                    "Fire Axe: \t\t Defeat one Monster after you draw it (once per Dungeon).", 
                    "Chainmail: \t\t HP + 4",
                    "Leather Shield: \t HP + 3"))

""" 
    A function for a round of game
"""
def gameRound(numPlayers, playerNames, winning, failure, 
              lastAdventurer, allEquipment):
    
    # Charactor choice
    print("Character List:")
    print("0: Random Character from below")
    print("1: Mage")
    print("2: Warrior")
    print("3: Rogue")
    print("4: Barbarian")
    character = -1
    while (character < 0) or (character > 4):
        character = intInput("Please choose the character for this round: ", 0, 4) 
    
    if character == 0:
        character = random.randint(1, 4)
    
    charNames = ("Mage", "Warrior", "Rogue", "Barbarian")
    
    print("Your character is " + charNames[character - 1] + ".")
    print()
    
    # Create and initiate monster list
    monsterNames = ("Goblin", "Goblin", "Skeleton", "Skeleton", "Orc", "Orc", 
                    "Vampire", "Vampire", "Golem", "Golem", "Lich", "Demon", "Dragon")
    monsterStrength = (1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 9)
    
    monsterPile = list(range(len(monsterStrength)))
    random.shuffle(monsterPile)
    
    # Initialize character, equipment, dungeon, and skip
    equipment = list(range(6))
    dungeon = []
    skip = []
    for i in range(numPlayers):
        skip.append(1)
    
    # Bidding Stage
    tally = ""
    counter = lastAdventurer % numPlayers
    while sum(skip) > 1:
        print("_____________________________________________________________________________")
        print("Tally of progress:")
        print(tally)
        
        inGameLine = ""
        for i in range(numPlayers):
            if skip[i] > 0:
                inGameLine += "Player " + str(i + 1) + ": " + playerNames[i] + ", "
                
        inGameLine = inGameLine[:-2]        
        inGameLine += " are still in this round."
        print(inGameLine)
        print()
        
        currPlayer = counter % numPlayers
        if skip[currPlayer] == 0:
            input("Player " + str(currPlayer + 1) + ": " + playerNames[currPlayer] + " has withdrawn from this round. Press Enter to continue.")
            continue
        scoreBoard(winning, failure, playerNames)
        HP = charStatus(character, equipment, allEquipment)
        
        print("_____________________________________________________________________________")
        print() 
        
        print("Player " + str(currPlayer + 1) + ": " + playerNames[currPlayer] + "'s turn")
        print()
        print("There are a total of %d Monsters in the Dungeon." % len(dungeon))
        if len(monsterPile) > 0:
            print("1 --- Draw a Monster from the pile: %d Monsters remaining from the pile." % len(monsterPile))
            print("2 --- Withdraw from and no longer participate in this round.")
            
            userIn = intInput("Please enter your choice: ", 1, 2) 
        else:
            print("Cannot draw Monsters from the pile: No Monster remaining. You must withdraw from this round.")
            userIn = 2
        
        if userIn == 2:
            skip[currPlayer] -= 1
            input("You choose to withdraw from this round. Press Enter to continue.")
            tally += "> " + (playerNames[currPlayer] + " withdrew from this round. \n")
        elif userIn == 1:
            print()
            drawCard = monsterPile.pop(0)
            print("!: You have drawn " + monsterNames[drawCard] + " --- Strength " + str(monsterStrength[drawCard]) + " from the list.")
            print() 
            
            if len(equipment) > 0:
                print("Enter -1 if you would like to send the Monster to the Dungeon.")
                print("Or enter the corresponding index before the equipment to remove it with the Monster.")
                
                userIn1 = intInput("Please enter your choice: ", -1, len(equipment) - 1) 
                
            else:
                print("You must send the Monster to the Dungeon: No equipment remaining.")
                
                userIn1 = -1
                
            if userIn1 == -1:
                dungeon.insert(0, drawCard)
                input("You choose to send a Monster to the Dungeon. Press Enter to continue.")
                tally += "> " + (playerNames[currPlayer] + " sent a Monster to the Dungeon. \n")
            else:
                removal = equipment.pop(userIn1)
                nameEquipment = equipName(character, removal)
                input("You choose to remove " + nameEquipment + ". Press Enter to continue.")
                tally += "> " + (playerNames[currPlayer] + " removed " + nameEquipment + ". \n")
        
        counter += 1
        os.system('cls')  
        
    print("_____________________________________________________________________________")    
    print()
    print("End of Bidding Stage")
    
    print()
    
    # Decide the adventurer
    adventurer = counter % numPlayers
    print("Player " + str(adventurer + 1) + ": " + playerNames[adventurer] + " is the adventurer of this round.")
    print()
    scoreBoard(winning, failure, playerNames)
    
    # Print last equipment status
    charStatus(character, equipment, allEquipment)       
    
    # List Monster names
    monsterNameList = ("Goblin", "Skeleton", "Orc", "Vampire", "Golem", "Lich", "Demon", "Dragon")
    
    # Initialize the battle
    roundResult = 0
    if character == 1:
        polymorph = False
        demonPact = -1
        omnipotenceMonsters = dungeon   
        
        if 0 in equipment: 
            polymorph = True
        if 1 in equipment:
            demonPact = 0

    elif character == 2:
        vorpal = 'None'
        
        if 3 in equipment: 
            print("!: Vorpal Sword --- You can choose a monster to defeat for this round.")
            monsterList()
            userIn2 = intInput("Please enter the index of the monster you would like to defeat: ", 0, 7) 
            vorpal = monsterNameList[userIn2]
            print("!: Vorpal Sword --- You choose to defeat the %s for this round. \n" % vorpal)
            
    elif character == 3:
        vorpal = 'None'
        healing = False
        
        if 3 in equipment: 
            print("!: Vorpal Sword --- You can choose a monster to defeat for this round.")
            monsterList()
            userIn2 = intInput("Please enter the index of the monster you would like to defeat: ", 0, 7) 
            vorpal = monsterNameList[userIn2]
            print("!: Vorpal Sword --- You choose to defeat the %s for this round. \n" % vorpal)
        if 2 in equipment:
            healing = True
            
    elif character == 4:
        healing = False
        fireAxe = False
        
        if 2 in equipment:
            healing = True
            
        if 3 in equipment:
            fireAxe = True 
    
    for m in range(len(dungeon)):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("X: Dungeon %d/%d --- %s with Strength %d." % (m + 1, len(dungeon), monsterNames[dungeon[m]], monsterStrength[dungeon[m]]))
        if character == 1: # If a Mage
            result = battle(1, equipment, monsterStrength[dungeon[m]], monsterNames[dungeon[m]], demonPact = demonPact, polymorph = polymorph)
            if result[1]: # Check to see if Polymorph is performed
                polymorph = False
                if len(monsterPile) == 0: # Cannot Polymorph if there are no new Monsters
                    print("!: Polymorph --- There are no more Monsters in the pile.")
                    newDraw = dungeon[m]
                else: 
                    newDraw = monsterPile.pop(0)
                    print("!: Polymorph --- You find a new Monster.")
                    print("X: Dungeon %d --- %s with Strength %d." % (m + 1, monsterNames[newDraw], monsterStrength[newDraw]))
                result = battle(1, equipment, monsterStrength[newDraw], monsterNames[dungeon[m]], demonPact = demonPact, polymorph = polymorph)
                omnipotenceMonsters.pop(m)
                omnipotenceMonsters.insert(m, newDraw)
                    
            demonPact = result[3]
            polymorph = result[2]
            
            # Computing HP
            dHP = result[0]
            print("+: Current HP --- %d - (%d) = %d" % (HP, dHP, HP - dHP))
            HP = HP - dHP
            input("Press Enter to continue.")
            
            if HP <= 0:
                if 3 in equipment:
                    currInd = m
                    print("!: You are out of HP. Checking for Omnipotence.")
                    omnipotence = checkOmnipotence(omnipotenceMonsters, monsterNames, polymorph, monsterPile, currInd)
                    if omnipotence[0]:
                        print("!: Omnipotence --- Success. All the Monsters in the Dungeon are different.")
                        print("^_^: You win this round. ")
                        input("Press Enter to continue. ")
                        roundResult = 1
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print()
                        return(adventurer, roundResult)
                    else:
                        print("!: Omnipotence --- Failed. You have repeated %s." % omnipotence[1])
                        print("*_*: You fail this round. ")
                        input("Press Enter to continue. ")
                        roundResult = -1
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print()
                        return(adventurer, roundResult)
                else:
                    print("!: You are out of HP. ")
                    print("*_*: You fail this round. ")
                    input("Press Enter to continue.")
                    roundResult = -1
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print()
                    return(adventurer, roundResult)
        
        elif character == 2: # If a Warrior
            result = battle(2, equipment, monsterStrength[dungeon[m]], monsterNames[dungeon[m]], vorpal = vorpal)    
            
            # Computing HP
            dHP = result[0]
            print("+: Current HP --- %d - (%d) = %d" % (HP, dHP, HP - dHP))
            HP = HP - dHP
            input("Press Enter to continue.")
            
            if HP <= 0:
                print("!: You are out of HP. ")
                print("*_*: You fail this round. ")
                input("Press Enter to continue.")
                roundResult = -1
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print()
                return(adventurer, roundResult)
        
        elif character == 3: # If a Rogue
            result = battle(3, equipment, monsterStrength[dungeon[m]], monsterNames[dungeon[m]], vorpal = vorpal)    
            
            # Computing HP
            dHP = result[0]
            print("+: Current HP --- %d - (%d) = %d" % (HP, dHP, HP - dHP))
            HP = HP - dHP
            input("Press Enter to continue.")
            
            if HP <= 0:
                if healing:
                    print("!: Healing Potion --- You are revived to 3 HP.")
                    print()
                    HP = 3
                    healing = False
                    print("+: Current HP --- %d" % HP)
                    input("Press Enter to continue.")
                    
                else: 
                    print("!: You are out of HP. ")
                    print("*_*: You fail this round. ")
                    input("Press Enter to continue.")
                    roundResult = -1
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print()
                    return(adventurer, roundResult)
                
        elif character == 4: # If a Barbarian
            result = battle(4, equipment, monsterStrength[dungeon[m]], monsterNames[dungeon[m]], fireAxe = fireAxe)
            fireAxe = result[4]
            
            # Computing HP
            dHP = result[0]
            print("+: Current HP --- %d - (%d) = %d" % (HP, dHP, HP - dHP))
            HP = HP - dHP
            input("Press Enter to continue.")
            
            if HP <= 0:
                if healing:
                    print("!: Healing Potion --- You are revived to 4 HP.")
                    print()
                    HP = 4
                    healing = False
                    print("+: Current HP --- %d" % HP)
                    input("Press Enter to continue.")
                    
                else: 
                    print("!: You are out of HP. ")
                    print("*_*: You fail this round. ")
                    input("Press Enter to continue.")
                    roundResult = -1
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print()
                    return(adventurer, roundResult)
            
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()

            
    print("!: You have defeated all Monsters in the Dungeon.")
    print("^_^: You win this round. ")
    input("Press Enter to continue. ")   
    roundResult = 1
    
    return (adventurer, roundResult)

""" 
    A function for collect user input for integers
"""
def intInput(quest, lowBound, upperBound):
    failReq = True
    compList = list(range(lowBound, upperBound + 1))
    for i in range(len(compList)):
        compList[i] = str(compList[i])
        
    while failReq:
        userIn = input("> " + quest)
        userIn.strip()
        for i in range(len(compList)):
            if compList[i] == userIn:
                failReq = False
                return int(userIn)
        print("Error: Please try again.\n")

"""
    A function for determining HP outcome after combating every Monster.
"""
def battle(character, equipment, monsterStrength, monsterName, demonPact = -1, polymorph = False, vorpal = 'None', fireAxe = False):
    # Assume polymorphed is not used in this round
    polymorphed = False
    
    if character == 1: # If a Mage
        # Assess Polymorph
        if polymorph: 
            print("?: Polymorph --- Would you like to replace the Monster with the next Monster from the deck?")
            print("1 --- Yes.")
            print("2 --- No.")
            userIn3 = intInput("Please enter your choice: ", 1, 2) 

            if userIn3 == 1:
                polymorphed = True
                polymorph = False
                print("!: You choose to use polymorph.")
                print()
                return (0, polymorphed, polymorph, demonPact, fireAxe)
            
        # Assess Demonic Pact
        if demonPact > 0:
            demonPact = -1
            print("!: Demonic Pact --- Defeat the Monster after Demon.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        if (monsterStrength == 7) and (demonPact == 0):
            demonPact = 1
            print("!: Demonic Pact --- Defeat the Demon.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess Holy Grail
        if (2 in equipment) and (monsterStrength % 2 == 0):
            print("!: Holy Grail --- Defeat a Monster with even-numbered strength.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Other situations
        print("!: You do not have the equipment to defeat the Monster. You lose %d HP." % monsterStrength)
        print()
        return (monsterStrength, polymorphed, polymorph, demonPact, fireAxe)
    
    elif character == 2: # If a Warrior
        # Assess Torch
        if (0 in equipment) and (monsterStrength <= 3):
            print("!: Torch --- Defeat a Monster with strength 3 or less.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess Dragon Spear
        if (1 in equipment) and (monsterName == 'Dragon'):
            print("!: Dragon Spear --- Defeat the Dragon.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess Holy Grail
        if (2 in equipment) and (monsterStrength % 2 == 0):
            print("!: Holy Grail --- Defeat a Monster with even-numbered strength.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess Vorpal Sword
        if monsterName == vorpal:
            print("!: Vorpal Sword [%s] --- Defeat the %s as you wish." % (vorpal, vorpal))
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Other situations
        print("!: You do not have the equipment to defeat the Monster. You lose %d HP." % monsterStrength)
        print()
        return (monsterStrength, polymorphed, polymorph, demonPact, fireAxe)
    
    elif character == 3: # If a Rogue
        # Assess Invisibility Cloak
        if (0 in equipment) and (monsterStrength >= 6):
            print("!: Invisibility Cloak --- Defeat a Monster with strength 6 or more.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess Ring of Power
        if (1 in equipment) and (monsterStrength <= 2):
            print("!: Ring of Power --- Defeat a Monster with strength 2 or less and return their strength to you.")
            print()
            return (-monsterStrength, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess Vorpal Sword
        if monsterName == vorpal:
            print("!: Vorpal Sword [%s] --- Defeat the %s as you wish." % (vorpal, vorpal))
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Other situations
        print("!: You do not have the equipment to defeat the Monster. You lose %d HP." % monsterStrength)
        print()
        return (monsterStrength, polymorphed, polymorph, demonPact, fireAxe)
        
    elif character == 4:
        # Assess Torch
        if (0 in equipment) and (monsterStrength <= 3):
            print("!: Torch --- Defeat a Monster with strength 3 or less.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Assess War Hammer
        if (1 in equipment) and (monsterName == 'Golem'):
            print("!: War Hammer --- Defeat the Golem.")
            print()
            return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        if fireAxe:
            print("!: Fire Axe --- Would you like to defeat the Monster unharmed?")
            print("1 --- Yes.")
            print("2 --- No.")
            userIn5 = intInput("Please enter your choice: ", 1, 2)
            if userIn5 == 1:
                fireAxe = False
                print("!: Fire Axe --- You have defeated the Monster unharmed.")
                print()
                return (0, polymorphed, polymorph, demonPact, fireAxe)
        
        # Other situations
        print("!: You do not have the equipment to defeat the Monster. You lose %d HP." % monsterStrength)
        print()
        return (monsterStrength, polymorphed, polymorph, demonPact, fireAxe)

"""
    A function for checking whether Omnipotence holds
"""
def checkOmnipotence(omnipotenceMonsters, monsterNames, polymorph, monsterPile, currInd):
    nameList = []
    determine = True
    repetitor = ''
    if polymorph and (len(monsterPile) == 0):
        print("!: Polymorph --- There are no more Monsters in the pile.")
        polymorph = False
    
    for m in range(len(omnipotenceMonsters)):
        currMonster = monsterNames[omnipotenceMonsters[m]]
        print("X: Dungeon Monster %d/%d: %s" % (m + 1, len(omnipotenceMonsters), currMonster))
        if polymorph and (m > currInd):
            print("?: Polymorph --- Would you like to replace the Monster with the next Monster from the deck?")
            print("1 --- Yes.")
            print("2 --- No.")
            userIn3 = intInput("Please enter your choice: ", 1, 2)
            if userIn3 == 1:
                currMonster = monsterNames[monsterPile.pop(0)]
                print("!: Polymorph --- You find a new Monster.")
                print("X: Dungeon Monster %d/%d: %s" % (m + 1, len(omnipotenceMonsters), currMonster))
                polymorph = False
            
        
        if currMonster in nameList: # See repetitions
            determine = False
            repetitor = monsterNames[omnipotenceMonsters[m]]
            
        
        nameList.append(monsterNames[omnipotenceMonsters[m]])
    
    return (determine, repetitor)
"""
    A function for listing all different monsters
"""
def monsterList():
    monsterNames = ("Goblin:", "Skeleton:", "Orc:", "Vampire:", "Golem:", "Lich:", "Demon:", "Dragon:")
    monsterStrength = (1, 2, 3, 4, 5, 6, 7, 9)
    for i in range(len(monsterStrength)):
        print(str(i) + " --- " + monsterNames[i] + "\t Strength " + str(monsterStrength[i]))
    print()

""" 
    A function for extracting the name of the equipment
"""
def equipName(character, index):
    nameLine = allEquipment[character - 1][index]
    nameLine = nameLine.split(':')[0]
    return nameLine
    
"""
    A function for showing character status
"""
def charStatus(character, equipment, allEquipment):
    if character == 1:
        print("Character: Mage")
        
        # Calculating total HP
        HP = 2
        if 4 in equipment: # Check HP with "Wall of Fire"
            HP += 6
        if 5 in equipment: # Check HP with "Bracelet of Protection"
            HP += 3 
        print("Total HP: %d" % HP)
        print("Equipment left:")
        equipmentList = allEquipment[0]
        for i in range(len(equipment)):
            print(str(i) + " --- " + equipmentList[equipment[i]])
    elif character == 2:
        print("Character: Warrior")
        
        # Calculating total HP
        HP = 3
        if 4 in equipment: # Check HP with "Wall of Fire"
            HP += 5
        if 5 in equipment: # Check HP with "Bracelet of Protection"
            HP += 3 
        print("Total HP: %d" % HP)
        print("Equipment left:")
        equipmentList = allEquipment[1]
        for i in range(len(equipment)):
            print(str(i) + " --- " + equipmentList[equipment[i]])
    elif character == 3:
        print("Character: Rogue")
        
        # Calculating total HP
        HP = 3
        if 4 in equipment: # Check HP with "Wall of Fire"
            HP += 5
        if 5 in equipment: # Check HP with "Bracelet of Protection"
            HP += 3 
        print("Total HP: %d" % HP)
        print("Equipment left:")
        equipmentList = allEquipment[2]
        for i in range(len(equipment)):
            print(str(i) + " --- " + equipmentList[equipment[i]])        
    elif character == 4:
        print("Character: Barbarian")
        
        # Calculating total HP
        HP = 4
        if 4 in equipment: # Check HP with "Wall of Fire"
            HP += 4
        if 5 in equipment: # Check HP with "Bracelet of Protection"
            HP += 3 
        print("Total HP: %d" % HP)
        print("Equipment left:")
        equipmentList = allEquipment[3]
        for i in range(len(equipment)):
            print(str(i) + " --- " + equipmentList[equipment[i]])      
            
    print()
            
    return HP
    
"""
    A function for showing the winning and losing rounds for each player
"""
def scoreBoard(winning, failure, playerNames):
    playerLine = "Player \t\t"
    nameLine = ""
    winLine = "Success \t"
    failLine = "Failure \t"
    for i in range(len(winning)):
        playerLine += ("\t" + str(i + 1) + "\t")
        winLine += ("\t" + str(winning[i]) + "\t")
        failLine += ("\t" + str(failure[i]) + "\t")
    
    for i in range(len(playerNames)):
        nameLine += ("Player " + str(i + 1) + " --- " + playerNames[i] + "     ")
    
    print("Scoreboard:")    
    print(nameLine)
    print()
    print(playerLine)
    print(winLine)
    print(failLine)
    print()
        
"""
    Main function for execution
"""
def main():
    
    # Obtain player numbers and names and initialize scoreboard
    numPlayers = intInput("Please enter the number of total players (no less than 2 but no more than 4): ", 2, 4)
    playerNames = []
    winning = []
    failure = []
    for i in range(numPlayers):
        name = input("Please enter the name of player " + str(i + 1) + ": ")
        playerNames.append(name)
        winning.append(0)
        failure.append(0)
    
    # Start the rounds round
    roundNum = 1
    lastAdventurer = 0
    while True:
        print("_____________________________________________________________________________")
        print("Round %d" % roundNum)
            
        roundResult = gameRound(numPlayers, playerNames, winning, 
                                failure, lastAdventurer, allEquipment)
        roundNum += 1
        
        lastAdventurer = roundResult[0]
        
        if roundResult[1] > 0: # If the adventurer won
            winning[roundResult[0]] += 1 
        elif roundResult[1] < 0: # If the adventurer failed
            failure[roundResult[0]] += 1
            if failure[roundResult[0]] >= 2: # If the player failed for no less than 2 times
                outPlayer = playerNames.pop(roundResult[0])
                numPlayers -= 1
                print("T_T: Sorry --- %s has lost this game by failed 2 adventures!" % outPlayer)
                print("The remaining players continue to participate in the next round.")
                
                input("Press Enter to continue.")
        else:
            print("ERROR: Round Result!")
            
        # Check winning status 
        
        if 2 in winning: # Win for 2 successes
            winner = winning.index(2)
            print("\\^o^/: Congratulations --- %s is the final winner by winning 2 adventures!" % playerNames[winner])
            input("Press Enter to continue.")
            break
        
        if len(playerNames) <= 1: # Win for surviving
            print("\\^o^/: Congratulations --- %s is the final winner by surviving through all these adventures!" % playerNames[0])
            input("Press Enter to continue.")
            break    
        
    print("Finished!")
    return

os.system('cls')    
main()
