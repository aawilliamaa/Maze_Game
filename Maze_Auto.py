from Maze_Class import *
class Auto:
    def __init__(self,player ,auto, method):
        with open("Maze_Commend.json","r") as file:
            control = json.load(file)["player"]["control"]
        self.auto = auto
        self.index = 0
        self.respond = [control["up"][0],control["right"][0],control["down"][0],control["left"][0]]
        self.path_all = [list(player.position)]
        self.method = method
        self.run = -1
        self.path = [list(player.position)]
        self.position = list(player.position)

        self.path_bfs = [Auto_node(list(player.position),[])]
        self.position_bfs = Auto_node(list(player.position),[])
        
    def standard_answer(self, maze: Maze, player: Player):
        self.path = []
        node = maze.end
        while node.parent != None:
            self.path.append(node())
            node = node.parent
        
        l = int(len(self.path))

        for n in maze.path:
            if n() == player.position:
                node = n
                break
            
        joint = self.path[-1]

            
        while node.parent != None:
            self.path.insert(l, node())
            node = node.parent

            if node() in self.path:
                self.path.insert(l,node())
                joint = node()
                break
        
        pop_index = []

        for i in range(len(self.path)):
            if self.path[i] == joint:
                pop_index.append(i)
        if len(pop_index) == 2:
            for i in range(pop_index[1]-pop_index[0]):
                self.path.pop(pop_index[0])
        

        answer = ""
        
        commend = {
            "[0, 1]": self.respond[2],
            "[0, -1]": self.respond[0],
            "[1, 0]":self.respond[1],
            "[-1, 0]":self.respond[3]
        }

        for i in range(1,len(self.path)):
            diff = [self.path[-i-1][0]-self.path[-i][0],self.path[-i-1][1]-self.path[-i][1]]
            if str(diff) in commend:
                answer += commend[str(diff)]

        return answer
    
    def dfs(self, maze: Maze, player: Player):
        if player.position == self.position:
            if self.index == 3:
                self.index = 0
            else:
                self.index += 1
        else:
            self.position = list(player.position)
            if player.position in self.path:
                while self.path[-1] != player.position:
                    self.path.pop(-1)
            else:
                self.path.append(list(player.position))
            
            if self.index == 0:
                self.index = 3
            else:
                self.index -= 1
        return self.respond[self.index]
    
    def bfs(self, maze: Maze, player: Player):
        if player.position not in self.path_all:
            self.path_all.append(list(player.position))
            self.path_bfs.append(Auto_node(player.position,self.position_bfs))
        
        if self.run < 3:
            player.position = list(self.position_bfs())
            self.run += 1
        else:
            self.path_bfs.pop(0)
            player.position = list(self.path_bfs[0]())
            self.position_bfs = self.path_bfs[0]
            self.run = 0
        return self.respond[self.run]