import Player_class
import Color_icon_class

# make the comparison object able to take in more than 2 players? use *args for this I guess
class Comparison:

    def __init__(self, player1_username, player1_server, player2_username, player2_server):

        self.player1 = Player_class.Player(player1_server, player1_username)
        self.player2 = Player_class.Player(player2_server, player2_username)
        self.colorIcon1 = Color_icon_class.ColorIcon(self.player1.overallAccountWn8, self.player1.playerServer)
        self.colorIcon2 = Color_icon_class.ColorIcon(self.player2.overallAccountWn8, self.player2.playerServer)
    
    def compareOverallStats(self):

#-----------------------------------------------------------------------------------------------

        if self.player1.overallAccountWn8 > self.player2.overallAccountWn8:
            percentDiffWN8 = round(((self.player1.overallAccountWn8 - self.player2.overallAccountWn8)/self.player2.overallAccountWn8) * 100, 2)
            
            percentDiffWN8String = (f"> **{self.player1.username} ({(self.player1.playerServer).upper()} {self.colorIcon1.serverIcon()})** "
            f"has {self.colorIcon1.colorWN8()} **{str(self.player1.overallAccountWn8)}** Overall WN8"
            f" > **{self.player2.username} ({(self.player2.playerServer).upper()} {self.colorIcon2.serverIcon()})** "
            f"has {self.colorIcon2.colorWN8()} **{str(self.player2.overallAccountWn8)}** Overall WN8, there is a "
            f"__{str(percentDiffWN8)}__ percent difference between them!")
        
        elif self.player1.overallAccountWn8 < self.player2.overallAccountWn8:
            percentDiffWN8 = round(((self.player2.overallAccountWn8 - self.player1.overallAccountWn8)/self.player1.overallAccountWn8) * 100, 2)

            percentDiffWN8String = (f"> **{self.player2.username} ({(self.player2.playerServer).upper()})** has **{str(self.player2.overallAccountWn8)}** Overall WN8"
            f" > **{self.player1.username} ({(self.player1.playerServer).upper()})** has **{str(self.player1.overallAccountWn8)}** Overall WN8, there is a "
            f"__{str(percentDiffWN8)}__ percent difference between them!")
        else:
            percentDiffWN8 = 0

#-----------------------------------------------------------------------------------------------

        if self.player1.wgRating > self.player2.wgRating:
            percentDiffWgRating = round(((self.player1.wgRating - self.player2.wgRating)/self.player2.wgRating) * 100, 2)

            percentDiffWgRatingString = (f"> **{self.player1.username} ({(self.player1.playerServer).upper()})** has **{str(self.player1.wgRating)}** WG Rating"
            f" > **{self.player2.username} ({(self.player2.playerServer).upper()})** has **{str(self.player2.wgRating)}** WG Rating, there is a "
            f"__{str(percentDiffWgRating)}__ percent difference between them!")
        
        elif self.player1.wgRating < self.player2.wgRating:
            percentDiffWgRating = round(((self.player2.wgRating - self.player1.wgRating)/self.player1.wgRating) * 100, 2)

            percentDiffWgRatingString = (f"> **{self.player2.username} ({(self.player2.playerServer).upper()})** has **{str(self.player2.wgRating)}** WG Rating"
            f" > **{self.player1.username} ({(self.player1.playerServer).upper()})** has **{str(self.player1.wgRating)}** WG Rating, there is a "
            f"__{str(percentDiffWgRating)}__ percent difference between them!")

        else:
            percentDiffWgRating = 0

#-----------------------------------------------------------------------------------------------

        if self.player1.winRate > self.player2.winRate:
            winrateDiff = round(self.player1.winRate - self.player2.winRate, 2)

            winrateDiffString = (f"> **{self.player1.username} ({(self.player1.playerServer).upper()})** has **{str(self.player1.winRate)}** Overall WR"
            f" > **{self.player2.username} ({(self.player2.playerServer).upper()})** has **{str(self.player2.winRate)}** Overall WR, there is a "
            f"__{str(winrateDiff)}__ percent difference between them!")

        elif self.player1.winRate < self.player2.winRate:
            winrateDiff = round(self.player2.winRate - self.player1.winRate, 2)

            winrateDiffString = (f"> **{self.player2.username} ({(self.player2.playerServer).upper()})** has **{str(self.player2.winRate)}** Overall WR"
            f" > **{self.player1.username} ({(self.player1.playerServer).upper()})** has **{str(self.player1.winRate)}** Overall WR, there is a "
            f"__{str(winrateDiff)}__ percent difference between them!")
        else:
            winrateDiff = 0

#-----------------------------------------------------------------------------------------------

        return percentDiffWN8String + "\n" + winrateDiffString + "\n" + percentDiffWgRatingString


#test = Comparison("waikin_reppinKL", "na", "quickfingers", "eu")
#print(test.compareOverallStats())

  