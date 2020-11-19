
import copy
# class TreeEdge:
#     def __init__(self, fatherNode, childNode, action):
#         super(TreeEdge, self).__init__()
#         self.fatherNode = fatherNode
#         self.childNode = childNode
#         self.action = action
#
#         self.N = 0
#         self.Q =

class TreeNode:

    def __init__(self, father, action, prob):
        super(TreeNode, self).__init__()

        self.children = {} # (action, child)

        self.fatherNode = father
        self.action = action

        self.P = prob
        self.N = 0 # visiting times.
        self.V = 0 # average value.
        self.W = 0 # total value.

    def allActions(self):
        return self.children.keys()

    def allChildren(self):
        return self.children.values()

    def PUCT(self, totalN):
        return self.V + 1.0*self.P * (totalN**0.5)/(1+self.N)

    def bestActionByPUCT(self):
        actions = self.allActions()
        totalN = 0
        for action in actions:
            totalN += self.children[action].N

        bestPUCT = -1e9
        bestAction = (-1, -1)
        for action in actions:
            newPUCT = self.children[action].PUCT()
            if newPUCT > bestPUCT:
                bestPUCT = newPUCT
                bestAction = action
        return bestAction

    def isLeaf(self):
        return len(self.children) == 0





class MCTS:
    def __init__(self, eta=1.0, network=None):
        super(MCTS, self).__init__()
        self.root = TreeNode(None, None, 0)
        self.currentRootNode = self.root
        self.eta = eta

    def expand(self, simulator, network):
        """
        reach and expand a leaf.
        :return:
        """
        simulator = copy.deepcopy(simulator) #could I use copy?
        node = self.currentRootNode
        while not node.isLeaf():
            action = node.bestActionByPUCT()
            node = node.children[action]
            simulator.takeAction(action)


        actions = simulator.getAvailableActions()
        actionProbability, z = network.getPolicy_Value(simulator.getCurrentState())
        for action in actions:
            node.children[action] = TreeNode(node, action, actionProbability[action])
        while node != self.currentRootNode:
            node.N += 1
            node.W += 1-z #in logic, 一个点的Q存的是他父亲走这一步的价值
            node.V += node.W/node.N
            z=1-z


    def run(self, numOfIterations, simulator, network):
        for i in range(numOfIterations):
            self.expand(simulator, network)

    def getPolicy(self):
        node = self.currentRootNode
        actions = node.allActions()
        totalN = 0
        for action in actions:
            totalN += node.children[action].N**(1.0/self.eta)
        policy = {}
        for action in actions:
            policy[action] = (node.children[action].N**(1.0/self.eta) ) /totalN
        return policy
