from serverHandler import Handler


class Logger:

    def __init__(self):
        self.handler = Handler()

<<<<<<< HEAD
    def post_score(self,game,score,opt1="n/a",opt2="n/a",opt3="n/a"):
=======
    def post_score(self, game, score, opt1="n/a", opt2="n/a", opt3="n/a"):
>>>>>>> c3467e82b22876056a3cc4c155f06a4a4e7c1486
        #Poster score til game
        #Returnerer liste af scores til game
        scores = self.handler.update(game, score, opt1, opt2, opt3)
        templist = []
        for s in scores:
            if s["Game"] == str(game):
                templist.append(s)

        return templist
<<<<<<< HEAD

=======
>>>>>>> c3467e82b22876056a3cc4c155f06a4a4e7c1486

    def get_scores(self, game):
        #Poster score til game
        #Returnerer liste af scores til game
        scores = self.handler.update("get", 0, "n/a", "n/a", "n/a")
        templist = []
        for s in scores:
            if s["Game"] == str(game):
                templist.append(s)

        return templist
