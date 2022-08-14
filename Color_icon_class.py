

class ColorIcon:

    def __init__(self, player_wn8, player_wr, player_wg_rating, player_server):

        self.wn8 = player_wn8
        self.server = player_server
        self.wr = player_wr
        self.wgRating = player_wg_rating
        
    def colorWN8(self):

        if self.wn8 >= 4000:
            return "‼🟣‼"
        elif (self.wn8 >= 3000) and (self.wn8 < 4000):
            return "🟣"
        elif (self.wn8 >= 2000) and (self.wn8 < 3000):
            return "🔵"
        elif (self.wn8 >= 1200) and (self.wn8 < 2000):
            return "🟢"
        elif (self.wn8 >= 750) and (self.wn8 < 1200):
            return "🟡"
        elif (self.wn8 >= 450) and (self.wn8 < 750):
            return "🟠"
        elif (self.wn8 < 450):
            return "🍅"
    
    def colorWR(self):
        
        if self.wr >= 65:
            return "‼🟣‼"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🟣"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🔵"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🟢"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🟡"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🟠"
        elif (self.wr >= 58) and (self.wr < 65):
            return "🍅"

    def serverIcon(self):

        if self.server == "na":
            return ":flag_us:"
        if self.server == "eu":
            return ":flag_eu:"
        if self.server == "ru":
            return ":flag_ru:"
        if self.server == "asia":
            return ":flag_sg:"
