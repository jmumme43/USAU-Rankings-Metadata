import csv
import math

games = []
teams = []
filmedGames = []

## OBJECTS ##

class Film:
    
    filmRating = -99.99
    
    def __init__(self, link, team1name, team1score, team2name, team2score, eventName):
        self.link = link
        self.team1name = team1name
        self.team1score = team1score
        self.team2name = team2name
        self.team2score = team2score
        self.eventName = eventName

class Game:
    
    removed = 0
    
    def __init__(self, eventName, divisionName, gameID, team1id, team1name, team1school, team1score, team2id, team2name, team2school, team2score, gameDate):
        self.eventName = eventName
        self.divisionName = divisionName
        self.gameID = gameID
        self.team1id = team1id
        self.team1name = team1name
        self.team1school = team1school
        self.team1score = team1score
        self.team2id = team2id
        self.team2name = team2name
        self.team2school = team2school
        self.team2score = team2score
        self.gameDate = gameDate
        return;

class Rating:
    
    true_weight = 0.00
    
    def __init__(self, game_rating, weight, game):
        self.game_rating = game_rating
        self.weight = weight
        self.game = game
        return;

class Team:
    
    old_rating = 1000.00
    new_rating = 1000.00
    wins = 0
    losses = 0
    total_score_weight = 0.00
    strength_of_schedule = -1000.00
    
    def __init__(self, tName, tID):
        self.tName = tName
        self.tID = tID
        self.gameList = []
        self.filmedList = []
        self.ratingsList = []
        return;
    
    def add_game(self, game):
        self.gameList.append(game)
        return;

    def add_film(self, film):
        self.filmedList.append(film)

## METHODS ##

def findRating(teamID):
    rating = 1000.00
    for team in teams:
        if teamID == team.tID:
            rating = team.new_rating
    return rating;

def printHighestRatedGame(tempName):
    for team in teams:
        if tempName == team.tName:
            highest_rated = -1000.00
            for game in team.gameList:
                highest_rated = max(highest_rated, findRating(game.team2id))
            
            for game in team.gameList:
                if highest_rated == findRating(game.team2id):
                    print("")
                    print("Highest Rated Opponent For %s:" % (team.tName))
                    print("%s: %s %s - %s %s" % (game.eventName, game.team1name, game.team1score, game.team2name, game.team2score))
    return;

def printHighestRatedWin(tempName):
    for team in teams:
        if tempName == team.tName:
            highest_rated = -1000.00
            for game in team.gameList:
                if game.team1score > game.team2score:
                    highest_rated = max(highest_rated, findRating(game.team2id))
            for game in team.gameList:
                if (highest_rated == findRating(game.team2id) and game.team1score > game.team2score):
                    print("")
                    print("Highest Rated Win For %s:" % (team.tName))
                    print("%s: %s %s - %s %s" % (game.eventName, game.team1name, game.team1score, game.team2name, game.team2score))
    return;

def printBestGame(tempName):
    for team in teams:
        if tempName == team.tName:
            best_rating = -1000.00
            best_rating_index = -1
            countthis = 0
            countthat = 0
            for rating in team.ratingsList:
                if rating.game_rating > best_rating:
                    best_rating = rating.game_rating
                    best_rating_index = countthis
                countthis = countthis + 1
            for game in team.gameList:
                if best_rating_index == countthat:
                    print("")
                    print("Best Game For %s:" % (team.tName))
                    print("%s: %s %s - %s %s" % (game.eventName, game.team1name, game.team1score, game.team2name, game.team2score))
                countthat = countthat + 1

def printWorstGame(tempName):
    for team in teams:
        if tempName == team.tName:
            worst_rating = 9999.00
            worst_rating_index = -1
            countthis = 0
            countthat = 0
            for rating in team.ratingsList:
                losing_score = 100
                winning_score = -100
                if rating.game.team1score > rating.game.team2score:
                    winning_score = rating.game.team1score
                    losing_score = rating.game.team2score
                else:
                    winning_score = rating.game.team2score
                    losing_score = rating.game.team1score
                maxpoint = (losing_score * 2) + 1
                if (rating.game_rating < worst_rating) and (winning_score < maxpoint):
                    worst_rating = rating.game_rating
                    worst_rating_index = countthis
                countthis = countthis + 1
            for game in team.gameList:
                if worst_rating_index == countthat:
                    print("")
                    print("Worst Game For %s:" % (team.tName))
                    print("%s: %s %s - %s %s" % (game.eventName, game.team1name, game.team1score, game.team2name, game.team2score))
                countthat = countthat + 1

def findUpsets():
    print("")
    print("Biggest Upsets (Rating)")
    print("")
    for team in teams:
        for game in team.gameList:
            opp_rating = findRating(game.team2id)
            if ((opp_rating + 325.00) < team.new_rating and game.team1score < game.team2score and game.team1score != 0):
                difference = team.new_rating - opp_rating
                print("%s: %s %s - %s %s" % (game.eventName, game.team1name, game.team1score, game.team2name, game.team2score))
    return;

def findBlowouts():
    print("")
    print("Biggest Upsets (Score)")
    print("")
    for team in teams:
        for game in team.gameList:
            opp_rating = findRating(game.team2id)
            if ((game.team1score - game.team2score) > 5 and team.new_rating < (opp_rating - 50.00) and game.team2score != 0):
                print("%s: %s %s - %s %s" % (game.eventName, game.team1name, game.team1score, game.team2name, game.team2score))
    return;

def displayGames(teamName):
    print("")
    print("List of Games for %s" % (teamName))
    print("")
    listToSort = []
    for team in teams:
        if teamName == team.tName:
            listToSort = team.gameList
    printSortedGames(listToSort)
    return;

def printSortedGames(listToBeSorted):
    for i in range(len(listToBeSorted)):
        max_idx = i
        for j in range(i+1, len(listToBeSorted)):
            if listToBeSorted[j].eventName > listToBeSorted[max_idx].eventName:
                max_idx = j
        listToBeSorted[i], listToBeSorted[max_idx] = listToBeSorted[max_idx], listToBeSorted[i]

    for game in listToBeSorted:
        print("%s: %s %s - %s %s" % (game.eventName, game.team1school, game.team1score, game.team2school, game.team2score))
    return;

def updateSoS():
    for team in teams:
        opp_rating_list = []
        for game in team.gameList:
            opp_rating_list.append(findRating(game.team2id))
        opp_rating_sum = 0.00
        for rat in opp_rating_list:
            opp_rating_sum = opp_rating_sum + rat
        team.strength_of_schedule = opp_rating_sum / float(len(opp_rating_list))
    return;

def calculateRatings():
    for team in teams:
        ratings = []
        team.wins = 0
        team.losses = 0
        team.total_score_weight = 0.00
        for game in team.gameList:
            losing_score = 100
            winning_score = -100
            if game.team1score > game.team2score:
                winning_score = game.team1score
                losing_score = game.team2score
                team.wins = team.wins + 1
            else:
                winning_score = game.team2score
                losing_score = game.team1score
                team.losses = team.losses + 1
                
            r_value = losing_score/(winning_score - 1.0)
            temp1 = ((1-r_value)/0.5)
            temp_min = 5.00
            if temp1 < 1.0:
                temp_min = temp1
            else:
                temp_min = 1.0
            numerator1 = 475.0 * math.sin(temp_min * 0.4 * math.pi)
            denominator1 = math.sin(0.4 * math.pi)
            rating_diff = 125.0 + (numerator1/denominator1)
            #print("%s vs %s --> %s" % (game.team1score, game.team2score, rating_diff))

            opp_rating = 1000.00
            for temp in teams:
                if game.team2id == temp.tID:
                    opp_rating = temp.old_rating
                
            game_rating = 1000.00
            if int(game.team1score) > int(game.team2score):
                game_rating = opp_rating + rating_diff
            else:
                game_rating = opp_rating - rating_diff
                
            helper = math.floor((winning_score - 1) / 2)
            max1 = -1000.00
            if losing_score > helper:
                max1 = losing_score
            else:
                max1 = helper
                
            numerator1 = winning_score + max1

            score_weight = 0.0
            if ((numerator1 / 19.0) > 1.0):
                score_weight = 1.0
            else:
                score_weight = math.sqrt(numerator1 / 19.0)

            real_rating = Rating(game_rating, score_weight, game)
            team.total_score_weight = team.total_score_weight + score_weight
                
            #print("%s %s - %s %s --- %s" % (game.team1school, game.team1score, game.team2school, game.team2score, score_weight))
                
            ratings.append(real_rating)
            
        newest_rating = 0.00
        rating_count = 0
        #print("%s: %s" % (team.tName, team.total_score_weight))
        for rating in ratings:
            rating.true_weight = rating.weight / team.total_score_weight
            #print("%s: %s" % (team.tName, rating.true_weight))
        
        for rating in ratings:
            rating_count = rating_count + 1
            newest_rating = newest_rating + (rating.game_rating * rating.true_weight)
        
        team.ratingsList = ratings
        
        team.new_rating = newest_rating

    for team in teams:
        team.old_rating = team.new_rating

    return;

## DATA/MAIN ##

with open('club2019women.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    counter = 0
    for row in readCSV:
        if counter > 0:
            t1score = row[6]
            t2score = row[10]
            if t1score == 'W':
                t1score = 15
            elif (t1score == 'F' or t1score == 'L' or t1score == ''):
                t1score = 0
            if t2score == 'W':
                t2score = 15
            elif (t2score == 'F' or t2score == 'L' or t2score == ''):
                t2score = 0
            
            t1score = int(t1score)
            t2score = int(t2score)
            
            tempGame = Game(row[0], row[1], row[2], row[3], row[4], row[5], t1score, row[7], row[8], row[9], t2score, row[11])
            games.append(tempGame)
        counter = counter + 1

    #create "teams" array and store data
    count = 0
    for game in games:
        count = count + 1

        if not teams:
            tempTeam1 = Team(game.team1name, game.team1id)
            tempTeam1.add_game(game)
            switchedGame = Game(game.eventName, game.divisionName, game.gameID, game.team2id, game.team2name, game.team2school, game.team2score, game.team1id, game.team1name, game.team1school, game.team1score, game.gameDate)
            tempTeam2 = Team(game.team2name, game.team2id)
            tempTeam2.add_game(switchedGame)
            teams.append(tempTeam1)
            teams.append(tempTeam2)
        else:
            found1 = 0
            found2 = 0
            for team in teams:
                if team.tID == game.team1id:
                    team.add_game(game)
                    found1 = 1
                elif team.tID == game.team2id:
                    switchedGame = Game(game.eventName, game.divisionName, game.gameID, game.team2id, game.team2name, game.team2school, game.team2score, game.team1id, game.team1name, game.team1school, game.team1score, game.gameDate)
                    team.add_game(switchedGame)
                    found2 = 1
            if found1 == 0:
                tempTeam1 = Team(game.team1name, game.team1id)
                tempTeam1.add_game(game)
                teams.append(tempTeam1)
                    
            if found2 == 0:
                tempTeam2 = Team(game.team2name, game.team2id)
                switchedGame = Game(game.eventName, game.divisionName, game.gameID, game.team2id, game.team2name, game.team2school, game.team2score, game.team1id, game.team1name, game.team1school, game.team1score, game.gameDate)
                tempTeam2.add_game(switchedGame)
                teams.append(tempTeam2)

    print("")
    print("There are %s games in the list." % (count))
    print("")

    for i in range(70):
        calculateRatings()

    #sort teams by rating (rank the teams for printing)
    for i in range(len(teams)):
        max_idx = i
        for j in range(i+1, len(teams)):
            if teams[j].new_rating > teams[max_idx].new_rating:
                max_idx = j
        teams[i], teams[max_idx] = teams[max_idx], teams[i]

    #print ranked teams
    countee = 0
    for team in teams:
        countee = countee + 1
        print("Rank %s: %s (%s - %s) --- Rating: %s" % (countee, team.tName, team.wins, team.losses, team.new_rating))
    
    '''
        print("")
        print("Teams Ranked by Strength of Schedule:")
        print("")
        
        countee = 0
        for team in teams:
        countee = countee + 1
        print("Rank %s: %s (%s - %s) --- Rating: %s" % (countee, team.tName, team.wins, team.losses, team.strength_of_schedule))
    '''

    findUpsets()

    findBlowouts()

    updateSoS()

    #sort teams by strengh of schedule (rank the teams for printing)
    for i in range(len(teams)):
        max_idx = i
        for j in range(i+1, len(teams)):
            if teams[j].strength_of_schedule > teams[max_idx].strength_of_schedule:
                max_idx = j
        teams[i], teams[max_idx] = teams[max_idx], teams[i]

    #displayGames("Bates College")
    
    with open('2019collegefilmarchive.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        counter = 0
        for row in readCSV:
            tempFilm = Film(row[0], row[1], row[2], row[3], row[4], row[5])
            filmedGames.append(tempFilm)

    
                                    
    #printHighestRatedGame("Streetgang")

    #printHighestRatedWin("Streetgang")

    printBestGame("Pop")

    printWorstGame("Pop")
