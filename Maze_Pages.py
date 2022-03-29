from Maze_Class import Clear
import json

class Pages:
    """
    畫出主頁面
    
    Attributes:
        difficulty_dic: 困難度對應之輸入指令
            key: "easy", "normal", "hard", "hheelloo", "hheelloohheelloo"
        control(dict): 控制遊戲的指令
            key: "up", "down", "left", "right"
        difficulty(str): 目前選擇的難度
    Methods:
        跳轉頁面
        menu(respond: str)->None: 跳至 menu 頁面
        Setting(respond: str)->None: 跳至 Setting 頁面
        Setting_Delete(respond: str)->None: 跳至 Setting Delete 頁面
        Setting_Delete_Select(respond: str)->None: 跳至 Setting Delete Select 頁面
        Setting_Add(respond: str)->None: 跳至 Setting Add 頁面
        Setting_Add_Select(respond: str)->None: 跳至 Setting Add Select 頁面
        
        顯示頁面
        display_menu()->None: 顯示 menu 頁面
        display_Setting()->None: 顯示 display_Setting 頁面
        display_Setting_Delete()->None: 顯示 display_Setting_Delete_Select 頁面
        display_Setting_Delete_Select(dic: str)->None: 顯示 display_Setting_Delete_Select 頁面
        display_Setting_Add()->None: 顯示 menu 頁面
        display_Setting_Add_Select(dic: str, error: bool)->None: 顯示 display_Setting_Add_Select 頁面
        
    """
    def __init__(self, difficulty_dic, control_dic, data):
        self.difficulty_dic = difficulty_dic
        self.control = control_dic
        self.data = data
        self.difficulty = self.menu("")
    def menu(self,respond): 
        """
        menu頁面
        
        previous page : 
            respond == 'x' -> exit 
        next page : 
            respond == 's' -> Setting page
            respond in all_difficulty_commends -> start "maze game"
            
        return -> str or bool
            如果沒有離開，就回傳難度（str）；如果離開，就回傳False
        """
        error = False   # 紀錄使否跳錯誤訊息
        all_difficulty_commends = []
        # 取出難度字典裡的所有值
        for c in self.difficulty_dic.values():
            for c1 in c:
                all_difficulty_commends.append(c1)
        
        while True:
            respond = ""
            self.display_menu(error) 
            respond = input(">>>")
            respond = respond.lower()
            
            if respond == "x":  # 離開
                return False
            elif respond == "s":
                error = False   # 進入設定後，就重置錯誤訊息的輸出
                self.Setting(respond)# 跳轉至 Setting 頁面
            elif respond in all_difficulty_commends:
                # 從字典difficulty的value，尋找對應的key
                for difficulty_keys, difficulty_value in self.difficulty_dic.items():
                    if respond in difficulty_value :
                        print("your difficulty is", difficulty_keys,end ='\n\n')
                        break
                print("loading")
                if  self.control['up'] != [] and  \
                    self.control['down'] != [] and\
                    self.control['left'] != [] and\
                    self.control['right'] != [] :
                    return(difficulty_keys)
                else:
                    error = True

    def Setting(self,respond):
        """
        Setting頁面
        
        previous page : 
            respond == 'b' -> "mune" page 
        next page : 
            respond == 'd' -> "Setting\delete" page
            respond == 'a' -> "Setting\add" page
            
        return -> None
        """       
        while True:
            respond = ""
            self.display_Setting()  # 印出畫面
            respond = input(">>>")  # 讀取輸入
            respond = respond.lower()   # 將輸入一律變小寫
            if respond == "b":  # 若輸入為“b”
                break   # 跳出此迴圈，並回到上一頁面（主畫面menu）
            elif respond == "d":    # 若輸入為“d”
                self.Setting_Delete(respond)    # 跳至 Setting_Delete 頁面
            elif respond == "a":    # 若輸入為“a”
                self.Setting_Add(respond)   # 跳至 Setting_Add 頁面

    def Setting_Delete(self,respond):
        """
        Setting_Delete 頁面
        previous page : 
            respond == 'b' -> "Setting" page 
        next page : 
            respond == in ["u","d","l","r"] -> "Setting\delete\Select" page
        """       
        
        while True:      # Setting_Delete
            respond = ""

            self.display_Setting_Delete()

            respond = input(">>>")
            respond = respond.lower()

            if respond == "b":
                break
            elif respond in ["u","d","l","r"]:
                if respond == "u":
                    dic = "up"
                elif respond == "d":
                    dic = "down"
                elif respond == "l": 
                    dic = "left"
                elif respond == "r":
                    dic = "right"
                self.Setting_Delete_Select(respond,dic)    # 跳轉至 Setting_Delete_Select 頁面
        
    def Setting_Delete_Select(self,respond,dic):
        """
        Setting Delete Select 
        previous page : 
            respond == 'b' -> "Setting_Delete" page 
        next page : 
            None
        """       
        
        while True:    
            respond = ""
            self.display_Setting_Delete_Select(dic)
            respond = input(">>>")
            respond = respond.lower()
            
            if respond == "b":
                break
            elif respond in self.control[dic]:
                self.control[dic].remove(respond)
                with open("Maze_Commend.json","w") as file:
                    json.dump(self.data,file)
        
    def Setting_Add(self,respond):
        """
        previous page : 
            respond == 'b' -> "Setting" page 
        next page : 
            respond n ["u","d","l","r"] -> "Setting\add\select" page
        """       
        while True:     # Add a Key
            respond = ""
            self.display_Setting_Add()

            respond = input(">>>")
            respond = respond.lower()
            if respond == "b":
                break
            elif respond in ["u","d","l","r"]:
                if respond == "u":
                    dic = "up"   # dic 意思 dicrection 
                elif respond == "d":
                    dic = "down"
                elif respond == "l": 
                    dic = "left"
                elif respond == "r":
                    dic = "right"
                self.Setting_Add_Select(respond,dic)

    def Setting_Add_Select(self,respond,dic):
        """
        previous page : 
            respond == 'b' -> "Setting" page 
        next page : 
            None
        """       
        error = False
        while True:
            respond = ""
            self.display_Setting_Add_Select(dic, error) # error 是否跳錯誤訊息（操作按鍵只能為一個字元）
            respond = input(">>>")
            respond = respond.lower()
            
            if respond == "b":
                break
            elif len(respond) != 1:
                error = True
            elif respond not in self.control[dic]:  # Add
                error = False
                self.control[dic].append(respond)
                self.data["player"]["control"][dic] = self.control[dic]
                with open("Maze_Commend.json","w") as file:
                    json.dump(self.data,file)


    def display_menu(self, error):
        Clear()
        print("MAZE GAME!!")
        print("\tSelect a Difficulty:")
        print("\t\tEasy:(e)")
        print("\t\tNormal:(n)")
        print("\t\tHard:(h)")
        print()
        print("\tSetting:(s)")
        print()
        print("\tType \"e\" to Easy Mode")
        print("\tType \"n\" to Normal Mode")
        print("\tType \"h\" to Hard Mode")
        print("\tType \"s\" to Setting")
        print("\tType \"x\" to Exit")
        if error:
            print("\n\t有操控按鍵沒有設定，無法開始遊戲")
            print('\t請按 "s" 進行按鍵設定')

    def display_Setting(self):
        Clear()
        print("Setting:")
        print("\tControl Buttons:")
        print(f"\t\tUp: {self.control['up']}")
        print(f"\t\tDown: {self.control['down']}")
        print(f"\t\tLeft: {self.control['left']}")
        print(f"\t\tRight: {self.control['right']}")
        print()
        print("\tType \"d\" to Delete a Key")
        print("\tType \"a\" to Add a Key")
        print()
        print("\tType \"b\" to Go Back")

    def display_Setting_Delete(self):
        Clear()
        print("Setting:")
        print("\tType \"u\" to Select Commend \"Up\"")
        print("\tType \"d\" to Select Commend \"Down\"")
        print("\tType \"l\" to Select Commend \"Left\"")
        print("\tType \"r\" to Select Commend \"Right\"")
        print()
        print("\tType \"b\" to Go Back")

    def display_Setting_Delete_Select(self,dic):
        Clear()
        print("Setting:")
        print(f"\t{dic} : {self.control[dic]}")
        print(f"\tType a Letter in List {self.control[dic]} to Delete")
        print()
        print("\tType \"b\" to Go Back")

    def display_Setting_Add(self):
        Clear()
        print("Setting:")
        print("\tType \"u\" to Select Commend \"Up\"")
        print("\tType \"d\" to Select Commend \"Down\"")
        print("\tType \"l\" to Select Commend \"Left\"")
        print("\tType \"r\" to Select Commend \"Right\"")
        print()
        print("\tType \"b\" to Go Back")

    def display_Setting_Add_Select(self,dic, error):
        Clear()  
        print("Setting:")
        print(f"\t{dic} : {self.control[dic]}")
        print(f"\tType a Letter to Add a New Key")
        print()
        print("\tType \"b\" to Go Back")
        if error:
            print("\t遊玩控制按鍵只能為一個字元")
