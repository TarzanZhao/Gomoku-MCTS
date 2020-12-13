import Agent
import Board
import Game
import matplotlib.pyplot as plt
from DataStorage import dataProcessor
import argument
import logger
import os

class Experiment():
    def __init__(self):
        self.args = argument.get_args()
        self.logger = logger.get_logger()
        self.depth = 2

    def getWinScore(self, game, agent):
        win = 0
        for i in range(self.args.numOfEvaluations):
            if game.run() == agent:
                win += 1
        return win / self.args.numOfEvaluations

    def evaluation(self,agent1,agent2, agentFirstOnly = True):
        board = Board.Board(self.args.size, self.args.numberForWin)
        game = Game.Game(agent1, agent2, board)
        Score = {agent1: 0, agent2: 0}
        self.logger.info("First Player Case:")
        for i in range(1, 1 + self.args.numOfEvaluations):
            winner = game.run()
            Score[winner] += 1
            if winner == agent1:
                self.logger.info("The %dth game: Win!" % i)
            else:
                self.logger.info("The %dth game: Lose!" % i)
        if not agentFirstOnly:
            game = Game.Game(agent2, agent1, board)
            self.logger.info("Second Player Case:")
            for i in range(1, 1 + self.args.numOfEvaluations):
                winner = game.run()
                Score[winner] += 1
                if winner == agent1:
                    self.logger.info("The %dth game: Win!" % (i + self.args.numOfEvaluations))
                else:
                    self.logger.info("The %dth game: Lose!" % (i + self.args.numOfEvaluations))
        return Score[agent1]/(2*self.args.numOfEvaluations-self.args.numOfEvaluations*agentFirstOnly)


    def simplePlot(self,X,Y,title,xlabel="x",ylabel='y',color='blue',linestyle='-.'):
        plt.plot(X,Y,color = color,linestyle=linestyle)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(os.path.join(self.args.figure_folder, title+'.png'))
        #plt.show()

    def evaluationWithBaseLine(self,agent, agentFirstOnly = True):
        agent2 = Agent.SearchAgent(depth=self.depth,epsilon=0)
        return self.evaluation(agent,agent2,agentFirstOnly)

    def playWithBaselineInDifferentNumOfIterations(self, model=None, agentFirstOnly = True, start = 100,end = 1600, stride = 100):
        if model is None:
            model = dataProcessor.loadNetwork(self.args)
        self.logger.info("Experiment for influence of different number of tree iterations")
        self.logger.info("baseline: depth 3")
        baseline = Agent.SearchAgent(3,epsilon=0)
        winRate = []

        for iter in range(start,end,stride):
            agent = Agent.IntelligentAgent(iter if iter!=0 else 1,model)
            winRate.append(self.evaluation(agent,baseline, agentFirstOnly))
        return range(start,end,stride), winRate

    def selfplayWithDifferentNumOfIterations(self):
        model = dataProcessor.loadNetwork(self.args)
        winRate = []
        for iter in range(5, 50, 5):
            agent = Agent.IntelligentAgent(iter, model)
            board = Board.Board(self.args.size, self.args.numberForWin)
            game = Game.Game(agent, agent, board)
            winRate.append(self.getWinScore(game, agent))
            self.logger.info("Iterations: %d, WinRate: %.2f" % (iter, winRate[-1]))

        plt.figure()
        plt.xlabel("Number of Iterations per Movem")
        plt.ylabel("Win Rate for First Player")
        plt.title("The must-win-strategy in 6*6 board with 3 in a row is learnable")
        plt.plot(range(5, 50, 5), winRate, color='blue', linestyle='-')
        plt.savefig('figure/6-6 3 must-win-strategy.png')
        plt.show()
