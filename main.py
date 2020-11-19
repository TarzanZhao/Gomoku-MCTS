import argparse
import Agent
import PolicyValueFn
import Board
import Game
import torch
import torch.nn


def main():
    # Training setting
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-batch-size', type=int, default=15000)
    parser.add_argument('--channels', type=int, default=4)
    parser.add_argument('--size', type=int, default=8)
    parser.add_argument('--numOfIterations', type=int, default=20)
    parser.add_argument('--numberForWin', type=int, default=4)
    parser.add_argument('--device',type=str,default='cpu')
    parser.add_argument('--lr', type=float, default=0.0001)
    parser.add_argument('--epochs', type=int, default=1000)
    parser.add_argument('--show-size', type=int, default=15000)
    parser.add_argument('--std', type=float, default=0.01)
    parser.add_argument('--show', type=int, default=0)
    parser.add_argument('--seed', type=int, default=1)
    args = parser.parse_args()

    args.device = ('cuda' if torch.cuda.is_available() else 'cpu')
    model = PolicyValueFn.PolicyValueFn(args).to(args.device)
    agent1 = Agent.SelfplayAgent(args.numOfIterations, model, "selfPlay.txt")
    b = Board.Board(args.size, args.numberForWin)
    g = Game.Game(agent0=agent1, agent1=agent1, simulator=b)
    for i in range(1, args.epochs + 1):
        print("epoch %d" % i)
        g.run()
        if i % 5 == 0:
            agent1.saveData()


if __name__ == '__main__':
    main()
