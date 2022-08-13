import Player_class

# make the comparison object able to take in more than 2 players? use *args for this I guess
class Comparison:

    def __init__(self, player1_username, player1_server, player2_username, player2_server):

        self.player1 = Player_class.Player(player1_server, player1_username)
        self.player2 = Player_class.Player(player2_server, player2_username)
    
    def compareOverallStats(self):
        
        if self.player1.overallAccountWn8 > self.player2.overallAccountWn8:
            percentDiffWN8 = round(((self.player1.overallAccountWn8 - self.player2.overallAccountWn8)/self.player2.overallAccountWn8) * 100, 2)
            
            percentDiffWN8String = self.player1.username + " has a higher overall wn8 of " + str(self.player1.overallAccountWn8) + \
            " while " + self.player2.username + " has a lower overall wn8 of " + str(self.player2.overallAccountWn8) + ", there is a " + \
            str(percentDiffWN8) + " percent difference between them!"
        
        elif self.player1.overallAccountWn8 < self.player2.overallAccountWn8:
            percentDiffWN8 = round(((self.player2.overallAccountWn8 - self.player1.overallAccountWn8)/self.player1.overallAccountWn8) * 100, 2)

            percentDiffWN8String = self.player2.username + " has a higher overall wn8 of " + str(self.player2.overallAccountWn8) + \
            " while " + self.player1.username + " has a lower overall wn8 of " + str(self.player1.overallAccountWn8) + ", there is a " + \
            str(percentDiffWN8) + " percent difference between them!"
        else:
            percentDiffWN8 = 0

        if self.player1.wgRating > self.player2.wgRating:
            percentDiffWgRating = round(((self.player1.wgRating - self.player2.wgRating)/self.player2.wgRating) * 100, 2)

            percentDiffWgRatingString = self.player1.username + " has a higher WG rating of " + str(self.player1.wgRating) + \
            " while " + self.player2.username + " has a lower WG rating of " + str(self.player2.wgRating) + ", there is a " + \
            str(percentDiffWgRating) + " percent difference between them!"
        
        elif self.player1.wgRating < self.player2.wgRating:
            percentDiffWgRating = round(((self.player2.wgRating - self.player1.wgRating)/self.player1.wgRating) * 100, 2)

            percentDiffWgRatingString = self.player2.username + " has a higher WG rating of " + str(self.player2.wgRating) + \
            " while " + self.player1.username + " has a lower WG rating of " + str(self.player1.wgRating) + ", there is a " + \
            str(percentDiffWgRating) + " percent difference between them!"

        else:
            percentDiffWgRating = 0

        if self.player1.winRate > self.player2.winRate:
            winrateDiff = round(self.player1.winRate - self.player2.winRate, 2)

            winrateDiffString = self.player1.username + " has a higher winrate of " + str(self.player1.winRate) + \
            " while " + self.player2.username + " has a lower winrate of " + str(self.player2.winRate) + ", there is a " + \
            str(winrateDiff) + " percent difference between them!"

        elif self.player1.winRate < self.player2.winRate:
            winrateDiff = round(self.player2.winRate - self.player1.winRate, 2)

            winrateDiffString = self.player2.username + " has a higher winrate of " + str(self.player2.winRate) + \
            " while " + self.player1.username + " has a lower winrate of " + str(self.player1.winRate) + ", there is a " + \
            str(winrateDiff) + " percent difference between them!"
        else:
            winrateDiff = 0

        return percentDiffWN8String + "\n" + percentDiffWgRatingString + "\n" + winrateDiffString


#test = Comparison("waikin_reppinKL", "na", "quickfingers", "eu")
#print(test.compareOverallStats())

  