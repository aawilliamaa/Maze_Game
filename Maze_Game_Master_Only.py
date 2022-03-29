import json
import time
from Maze_Class import *
from Maze_Auto import *
from Maze_Pages import *
#==================================================================================================
animation = False   # 是否開啟迷宮生成動畫
tick = 0   # 自動迷宮演算法的延遲，讓玩家可以慢慢看解法
#==================================================================================================
with open("Maze_Commend.json",encoding="utf-8") as file:
    data = json.load(file)
    difficulty_dic = data["main"]["difficulty"]
    control_dic = data["player"]["control"]
    commend = data["main"]["commend"]
#==================================================================================================
def Show_maze(maze: Maze, player: Player, tick: float, show_maze = True):
    """
    更新並將玩家顯示在迷宮上
    
    Args:
        maze (maze): 迷宮
        player (player): 玩家資訊
        tick(float): tick  
        show_maze (bool, optional): 若為 True，則不顯示迷霧；若為False，則顯示迷霧. Defaults to True.
    """
    time_start = time.time()
    x = player.position[0]
    y = player.position[1]
    maze.maze[player.tp[1]][player.tp[0]] = player.symbol["tp"]     # 在迷宮上設定tp符號
    maze.maze[maze.start()[1]][maze.start()[0]] = maze.symbol["start"]
    maze.maze[y][x] = player.symbol["player"]   # 在迷宮上設定玩家符號
    maze.mist[player.tp[1]][player.tp[0]] = player.symbol["tp"]     # 在迷宮上設定tp符號
    maze.mist[maze.start()[1]][maze.start()[0]] = maze.symbol["start"]
    maze.mist[y][x] = player.symbol["player"]   # 在迷宮上設定玩家符號
    
    # 將玩家附近的迷霧打開
    if x == 0 and y == 1 :
        maze.mist[y][x] = maze.maze[y][x]
        maze.mist[y][x + 1] = maze.maze[y][x + 1]
        maze.mist[y + 1][x] = maze.maze[y + 1][x]
        maze.mist[y - 1][x] = maze.maze[y - 1][x]
    elif x == maze.width - 1 and y == maze.height - 2:
        maze.mist[y][x] = maze.maze[y][x]
        maze.mist[y][x - 1] = maze.maze[y][x - 1]
        maze.mist[y + 1][x] = maze.maze[y + 1][x]
        maze.mist[y - 1][x] = maze.maze[y - 1][x]
    else:
        maze.mist[y][x] = maze.maze[y][x]
        maze.mist[y][x + 1] = maze.maze[y][x + 1]
        maze.mist[y][x - 1] = maze.maze[y][x - 1]
        maze.mist[y + 1][x] = maze.maze[y + 1][x]
        maze.mist[y - 1][x] = maze.maze[y - 1][x]
        
    maze.draw(show = show_maze)     # 畫出迷宮
    maze.maze[player.tp[1]][player.tp[0]] = maze.symbol["background"]     #將迷宮上的tp符號清除
    maze.maze[y][x] = maze.symbol["background"]   # 將迷宮上的玩家符號清除
    maze.mist[player.tp[1]][player.tp[0]] = maze.symbol["background"]     #將迷宮上的tp符號清除
    maze.mist[y][x] = maze.symbol["background"]   # 將迷宮上的玩家符號清除
    
    # 讓每次都有休息到tick
    time_end = time.time()
    time_cost = time_end - time_start
    if time_cost < tick:
        time.sleep(tick - time_cost)

def Update(maze: Maze , player: Player):
    """
    更新迷宮，但是不顯示

    Args:
        maze (maze): 迷宮資訊
        player (player): 玩家資訊
    """
    x = player.position[0]
    y = player.position[1]
    maze.maze[player.tp[1]][player.tp[0]] = player.symbol["tp"]     # 在迷宮上設定tp符號
    maze.maze[y][x] = player.symbol["player"]   # 在迷宮上設定玩家符號
    
    maze.mist[y][x] = maze.maze[y][x]
    maze.mist[y][x + 1] = maze.maze[y][x + 1]
    maze.mist[y][x - 1] = maze.maze[y][x - 1]
    maze.mist[y + 1][x] = maze.maze[y + 1][x]
    maze.mist[y - 1][x] = maze.maze[y - 1][x]
        
    maze.maze[player.tp[1]][player.tp[0]] = maze.symbol["background"]    #將迷宮上的tp符號清除
    maze.maze[y][x] = maze.symbol["background"]   # 將迷宮上的玩家符號清除

def maze_game(difficulty: str):
    
    m = Maze(difficulty)
    m.create(animation = animation)
    
    if difficulty in ["hheelloo", "hheelloohheelloo"]: 
        show_maze = False
    else:
        show_maze = True
        
    player = Player(position = m.start())

    Show_maze(m, player,0, show_maze = show_maze)     # 顯示迷宮

    # time_start = time.time()
    
    win = False
    quit = False
    
    input(">>>Press Any Button to Start")
    Show_maze(m, player,0, show_maze = show_maze)
    time_start = time.time()
    
    auto = Auto(player, False, "Standard")
    
    while True:
        

        if auto.auto == False:
            respond = input(">>>")
        elif auto.method == "BFS":
            respond = auto.bfs(m, player)
        elif auto.method == "DFS":
            respond = auto.dfs(m, player)
        elif auto.method == "Standard":
            respond = auto.standard_answer(m, player)

        
            
        if respond in commend["quit"]:  
            break
        elif respond in commend["reset"]:
            # 將迷宮上原本玩家位置的符號清除
            m.maze[player.position[1]][player.position[0]] = m.symbol["background"]
            m.mist[player.position[1]][player.position[0]] = m.symbol["background"]
            player.position = list(m.position["start"])     # 將玩家位置改成迷宮起點位置
            Show_maze(m, player,0, show_maze = show_maze)
            print("Back to The Starting Position")
        elif respond in commend["set"]:
            # 將迷宮上原本tp位置的符號清除
            m.maze[player.tp[1]][player.tp[0]] = m.symbol["background"]
            m.mist[player.tp[1]][player.tp[0]] = m.symbol["background"]
            player.tp = list(player.position)   # 將tp位置設定成玩家目前位置
            Show_maze(m, player,0, show_maze = show_maze)
            print("Set the Teleport Position")
        elif respond in commend["tp"]:
            # 將迷宮上原本玩家位置的符號清除
            m.maze[player.tp[1]][player.tp[0]] = m.symbol["background"]
            m.mist[player.tp[1]][player.tp[0]] = m.symbol["background"]           
            player.position = list(player.tp)
            Show_maze(m, player,0, show_maze = show_maze)
            print("Teleport")
        elif respond in commend["mist"]:
            show_maze = not show_maze
            Show_maze(m, player,0,show_maze = show_maze)
        elif respond in commend["auto"]:
            auto = Auto(player, True, auto.method)
            Show_maze(m, player,0, show_maze = show_maze)
        elif respond in commend["bfs"]:
            auto.method = "BFS"
            Show_maze(m, player,0, show_maze = show_maze)
            print("auto.method =",auto.method)
        elif respond in commend["dfs"]:
            auto.method = "DFS"
            Show_maze(m, player,0, show_maze = show_maze)
            print("auto.method =",auto.method)
        elif respond in commend["answer"]:
            auto.method = "Standard"
            Show_maze(m, player,0, show_maze = show_maze)
            print("auto.method =",auto.method)
        elif respond == "":
            Show_maze(m, player,0, show_maze = show_maze)
        
        else:
            for char in respond:
                player.move(char, m)
                if auto.auto == True:
                    if auto.method == "BFS":
                        for position in auto.path_bfs:
                            m.maze[position()[1]][position()[0]] = player.symbol["player"]
                            m.mist[position()[1]][position()[0]] = player.symbol["player"]
                            
                        Show_maze(m, player,tick, show_maze = show_maze)
                        for position in auto.path_bfs:
                            m.maze[position()[1]][position()[0]] = m.symbol["background"] 
                            m.mist[position()[1]][position()[0]] = m.symbol["background"] 
                    elif auto.method == "DFS":
                        for position in auto.path:
                            m.maze[position[1]][position[0]] = player.symbol["player"]
                            m.mist[position[1]][position[0]] = player.symbol["player"]
                        Show_maze(m, player,tick, show_maze = show_maze)  
                        for position in auto.path:
                            m.maze[position[1]][position[0]] = m.symbol["background"] 
                            m.mist[position[1]][position[0]] = m.symbol["background"]  
                    elif auto.method == "Standard":
                        Show_maze(m, player,tick, show_maze = show_maze)        
                else:
                    Show_maze(m, player,0, show_maze = show_maze)
                if player.position == m.position["end"]:
                    win = True
                    break
                
        
        if win == True:
            time_end = time.time()
            break
        elif quit:
            break
    
    if win == True:
        while True:
            if auto.auto == True:
                if auto.method == "Standard":
                    m.maze[m.start()[1]][m.start()[0]] = m.symbol["start"]
                    m.maze[m.end()[1]][m.end()[0]] = m.symbol["end"]
                    m.maze[auto.path[-1][1]][auto.path[-1][0]] = player.symbol["tp"]
                    auto.path.pop(0)
                    auto.path.pop(-1)
                    for position in auto.path:
                        m.maze[position[1]][position[0]] = player.symbol["player"]
                        m.mist[position[1]][position[0]] = player.symbol["player"]

                elif auto.method == "BFS":
                    m.maze[m.start()[1]][m.start()[0]] = m.symbol["start"]
                    m.maze[m.end()[1]][m.end()[0]] = m.symbol["end"]

                    path = [auto.path_bfs[0]]
                    while path[-1].parent != []:
                        path.append(path[-1].parent)

                
                    for position in path:
                        m.maze[position()[1]][position()[0]] = player.symbol["player"]
                        m.mist[position()[1]][position()[0]] = player.symbol["player"]

                    m.maze[auto.path_all[0][1]][auto.path_all[0][0]] = player.symbol["tp"]

                elif auto.method == "DFS":
                    m.maze[m.start()[1]][m.start()[0]] = m.symbol["start"]
                    m.maze[m.end()[1]][m.end()[0]] = m.symbol["end"]
                    m.maze[auto.path[0][1]][auto.path[0][0]] = player.symbol["tp"]
                    auto.path.pop(0)
                    for position in auto.path:
                        m.maze[position[1]][position[0]] = player.symbol["player"]
                        m.mist[position[1]][position[0]] = player.symbol["player"]
                m.draw(True)
            else:
                Show_maze(m, player,0, show_maze = True)
            
            
            print(f"You Win!!!!!!! Time Cost: {round(100 * (time_end - time_start)) / 100} s")
            i = input("要離開或是重新開始？(esc/again)")
            i = i.lower()
            if  i == "esc":
                game = False
                break
            elif i == "again":
                game = True
                break
    else:
        while True:
            Show_maze(m, player,0, show_maze = True)
            print("Thank You For Your Playing!")
            i = input("要離開或是重新開始？(esc/again)")
            i = i.lower()
            if  i == "esc":
                game = False
                break
            elif i == "again":
                game = True
                break
    win = False  
    return game       
def main():
    game_loop = True
    while game_loop:
        difficulty = Pages(difficulty_dic, control_dic, data).difficulty
        if difficulty == False:  # 如果在 pages 頁面直接離開
            break
        else:
            game_loop = maze_game(difficulty)
        
    print('感謝您的遊玩！')

if __name__ == "__main__":
    main()