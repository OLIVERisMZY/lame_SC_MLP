from __future__ import print_function
import copy
import tensorflow as tf
import numpy as np
import random
import xlrd
import pandas as pd
import math
import csv
class  replay_data_analyzer():
    def __init__(self,path,race):
       self.race=race   #敌人种族
       self.path=path
       self.original_data=self.get_original_data(self.path)


#从xlsx中得到原始数据========================================
    def get_original_data(self,path):
       data = xlrd.open_workbook(path)
       table = data.sheet_by_index(0)
       nrows = table.nrows
       ncols = table.ncols
       return table


    # 得到实全场比赛敌方数据=======================================
    def get_whole_match_enemy_info(self):
        table=self.original_data
        latest = table.nrows
        enemy_rt_info=\
            {
             "Protoss Zealot":0,
             "Protoss Dragoon":0,
             "Protoss Nexus": 0,
             "Protoss Probe": 0,
             "Protoss Robotics Facility": 0,
             "Protoss Observatory": 0,
             "Protoss Assimilator": 0,
             "Protoss Gateway": 0,
             "Protoss Forge": 0,
             "Protoss Observer": 0,
             "Protoss Photon": 0,
             "Protoss Cybernetics Core":0,
             }
        name =\
            {
             "Protoss Zealot":[],
             "Protoss Dragoon":[],
             "Protoss Nexus": [],
             "Protoss Probe": [],
             "Protoss Robotics Facility": [],
             "Protoss Observatory": [],
             "Protoss Assimilator": [],
             "Protoss Gateway": [],
             "Protoss Forge": [],
             "Protoss Observer": [],
             "Protoss Photon": [],
             "Protoss Cybernetics Core":[],
             }
        enemy_information=[]
        for i in range(latest):
            for key in enemy_rt_info.keys():

                if (key==table.cell(i, 4).value and table.cell(i, 2).value=="Discovered"):
                    if table.cell(i,3) not in name[key]:
                        name[key].append(table.cell(i,3))
                        enemy_rt_info[key]+=1
                elif(key==table.cell(i, 4).value and table.cell(i, 2).value=="Destoryed"):
                    if table.cell(i,3)  in name[key]:
                        name[key].remove(table.cell(i, 3))
                    enemy_rt_info[key] -= 1
                if enemy_rt_info[key]<0:
                    enemy_rt_info[key]=0
            enemy_information.append(enemy_rt_info)
        return enemy_information
    # 得到实全场比赛我方数据=======================================
    def get_whole_match_self_info(self):
            table = self.original_data
            latest=table.nrows
            self_rt_info = \
                {
                    "frame":0,
                    "Mineral": 50,
                    "Gas": 0,
                    "Supply Used": 4,
                    "Supply Total": 10,
                    "Terran Comsat Station": 0,
                    "Terran Missile Turret": 0,
                    "Terran Bunker": 0,
                    "Terran Engineering Bay": 0,
                    "Terran Command Center": 1,
                    "Terran SCV": 4,
                    "Terran Marine": 0,
                    "Terran Medic": 0,
                    "Terran Refinery": 0,
                    "Terran Siege Tank Tank Mode": 0,
                    "Terran Vulture": 0,
                    "Terran Goliath": 0,
                    "Terran Firebat": 0,
                    "Terran Supply Depot": 0,
                    "Terran Barracks": 0,
                    "Terran Factory": 0,
                    "Terran Academy": 0,
                    "Terran Machine Shop": 0,
                    "Terran Starport": 0,
                }
            self_mineral_info = \
                {
                    "Terran Comsat Station": 50,
                    "Terran Missile Turret":75,
                    "Terran Bunker": 100,
                    "Terran Engineering Bay": 150,
                    "Terran Command Center": 400,
                    "Terran SCV": 50,
                    "Terran Marine": 50,
                    "Terran Medic": 50,
                    "Terran Siege Tank Tank Mode": 150,
                    "Terran Vulture": 75,
                    "Terran Goliath": 100,
                    "Terran Firebat": 50,
                    "Terran Refinery": 100,
                    "Terran Supply Depot": 100,
                    "Terran Barracks": 150,
                    "Terran Factory": 200,
                    "Terran Academy": 150,
                    "Terran Machine Shop": 50,
                    "Terran Starport": 150,
                }
            self_supply_info = \
                {
                    "Terran Comsat Station": 0,
                    "Terran Missile Turret": 0,
                    "Terran Bunker": 0,
                    "Terran Engineering Bay": 0,
                    "Terran Command Center": 0,
                    "Terran SCV": 1,
                    "Terran Marine": 1,
                    "Terran Medic": 1,
                    "Terran Siege Tank Tank Mode": 2,
                    "Terran Vulture": 2,
                    "Terran Goliath": 2,
                    "Terran Firebat": 1,
                    "Terran Refinery": 0,
                    "Terran Supply Depot": 0,
                    "Terran Barracks": 0,
                    "Terran Factory": 0,
                    "Terran Academy": 0,
                    "Terran Machine Shop": 0,
                    "Terran Starport": 0,
                }
            self_gain_supply_info = \
                {
                    "Terran Comsat Station": 0,
                    "Terran Missile Turret": 0,
                    "Terran Bunker": 0,
                    "Terran Engineering Bay": 0,
                    "Terran Command Center": 10,
                    "Terran SCV": 0,
                    "Terran Marine": 0,
                    "Terran Medic": 0,
                    "Terran Siege Tank Tank Mode": 0,
                    "Terran Vulture": 0,
                    "Terran Goliath": 0,
                    "Terran Firebat": 0,
                    "Terran Refinery": 0,
                    "Terran Supply Depot": 8,
                    "Terran Barracks": 0,
                    "Terran Factory": 0,
                    "Terran Academy": 0,
                    "Terran Machine Shop": 0,
                    "Terran Starport": 0,
                }
            self_gas_info = \
                {
                    "Terran Comsat Station": 50,
                    "Terran Missile Turret": 0,
                    "Terran Bunker": 0,
                    "Terran Engineering Bay": 0,
                    "Terran Command Center": 0,
                    "Terran SCV": 0,
                    "Terran Marine": 0,
                    "Terran Medic": 25,
                    "Terran Siege Tank Tank Mode": 100,
                    "Terran Vulture": 0,
                    "Terran Refinery": 0,
                    "Terran Goliath": 75,
                    "Terran Firebat": 25,
                    "Terran Supply Depot": 0,
                    "Terran Barracks": 0,
                    "Terran Factory": 100,
                    "Terran Academy": 0,
                    "Terran Machine Shop": 50,
                    "Terran Starport": 100,
                }
            enemy_rt_info = \
                {
                    "Protoss Zealot": 0,
                    "Protoss Dragoon": 0,
                    "Protoss Nexus": 0,
                    "Protoss Probe": 0,
                    "Protoss Robotics Facility": 0,
                    "Protoss Observatory": 0,
                    "Protoss Assimilator": 0,
                    "Protoss Gateway": 0,
                    "Protoss Forge": 0,
                    "Protoss Observer": 0,
                    "Protoss Photon": 0,
                    "Protoss Cybernetics Core": 0,
                }
            name = \
                {
                    "Protoss Zealot": [],
                    "Protoss Dragoon": [],
                    "Protoss Nexus": [],
                    "Protoss Probe": [],
                    "Protoss Robotics Facility": [],
                    "Protoss Observatory": [],
                    "Protoss Assimilator": [],
                    "Protoss Gateway": [],
                    "Protoss Forge": [],
                    "Protoss Observer": [],
                    "Protoss Photon": [],
                    "Protoss Cybernetics Core": [],
                }
            total_information=[]
            for i in range(0,latest):
                #我方===============================================
                for key in self_rt_info.keys():
                    #建造建筑以及单位=================
                   if (key==table.cell(i, 4).value) \
                           and (table.cell(i, 2).value=="Created" or(table.cell(i, 2).value=="Morph" and key=='Terran Refinery') )\
                           and (table.cell(i, 0).value!=0):
                    self_rt_info[key]+=1
                    self_rt_info["Mineral"] -= self_mineral_info[key]
                    self_rt_info["Gas"] -= self_gas_info[key]
                    self_rt_info["Supply Used"] += self_supply_info[key]
                    self_rt_info["Supply Total"] += self_gain_supply_info[key]
                   if (key==table.cell(i, 4).value or table.cell(i, 4)=="Terran Siege Tank Siege Mode") and (table.cell(i, 2).value=="Destroyed"):
                       self_rt_info[key]-=1
                       self_rt_info["Supply Used"] -= self_supply_info[key]
                       self_rt_info["Supply Total"] -= self_gain_supply_info[key]
                if (self_rt_info["Terran Refinery"] == 0):
                    self_rt_info["Mineral"] += 0.05 * self_rt_info["Terran SCV"] * (
                                table.cell(i, 0).value - table.cell(i - 1, 0).value)
                elif (self_rt_info["Terran Refinery"] <=2):
                    self_rt_info["Mineral"] += 0.05 * (self_rt_info["Terran SCV"] - 3) * (
                                table.cell(i, 0).value - table.cell(i - 1, 0).value)
                elif (self_rt_info["Terran Refinery"] > 3):
                    self_rt_info["Mineral"] += 0.05 * (self_rt_info["Terran SCV"] - 9) * (
                                table.cell(i, 0).value - table.cell(i - 1, 0).value)
                if (self_rt_info["Terran Refinery"] == 1):
                    self_rt_info["Gas"] += 0.07 * 3 * (table.cell(i, 0).value - table.cell(i - 1, 0).value)
                elif (self_rt_info["Terran Refinery"] <= 2):
                     self_rt_info["Gas"] += 0.07 * 6 * (table.cell(i, 0).value - table.cell(i - 1, 0).value)
                elif (self_rt_info["Terran Refinery"] > 3):
                    self_rt_info["Gas"] += 0.07 * 9 * (table.cell(i, 0).value - table.cell(i - 1, 0).value)
                self_rt_info["Gas"]=int(self_rt_info["Gas"])
                self_rt_info["Mineral"]=int(self_rt_info["Mineral"])
                self_rt_info['frame'] =table.cell(i,0).value
                # 敌方===============================================
                for key in enemy_rt_info.keys():
                    if (key == table.cell(i, 4).value and table.cell(i, 2).value == "Discovered"):
                        if table.cell(i, 3) not in name[key]:
                            name[key].append(table.cell(i, 3))
                            enemy_rt_info[key] += 1
                    elif (key == table.cell(i, 4).value and table.cell(i, 2).value == "Destoryed"):
                        if table.cell(i, 3) in name[key]:
                            name[key].remove(table.cell(i, 3))
                        enemy_rt_info[key] -= 1

                enemy_rt_info['label'] = table.cell(i, 4).value
                mid={}
                mid.update(self_rt_info)
                mid.update(enemy_rt_info)
                total_information.append(mid)


            return total_information

    def get_input(self):
        build_name = \
            [
                "frame",
                "Mineral",
                "Gas",
                "Supply Used",
                "Supply Total",
                "Terran Comsat Station",
                "Terran Missile Turret",
                "Terran Bunker",
                "Terran Engineering Bay",
                "Terran Command Center",
                "Terran SCV",
                "Terran Marine",
                "Terran Medic",
                "Terran Refinery",
                "Terran Siege Tank Tank Mode",
                "Terran Vulture",
                "Terran Goliath",
                "Terran Firebat",
                "Terran Supply Depot",
                "Terran Barracks",
                "Terran Factory",
                "Terran Academy",
                "Terran Machine Shop",
                "Terran Starport"
            ]
        label_name={
                    "Terran Comsat Station": 1,
                    "Terran Missile Turret": 2,
                    "Terran Bunker": 3,
                    "Terran Engineering Bay": 4,
                    "Terran Command Center": 5,
                    "Terran SCV": 6,
                    "Terran Marine": 7,
                    "Terran Medic": 8,
                    "Terran Refinery": 9,
                    "Terran Siege Tank Tank Mode": 10,
                    "Terran Vulture": 11,
                    "Terran Goliath": 12,
                    "Terran Firebat": 13,
                    "Terran Supply Depot": 14,
                    "Terran Barracks": 15,
                    "Terran Factory": 16,
                    "Terran Academy": 17,
                    "Terran Machine Shop": 18,
                    "Terran Starport": 19,
                }
        table = self.original_data
        latest =table.nrows
        input=[]
        total=self.get_whole_match_self_info()
        print(str(table.nrows)+'+'+str(np.shape(total)))

        for i in range(0,latest):

             if ((table.cell(i, 2).value=="Created" )and (total[i]['label'] in build_name)) :
                total[i]['label']=label_name[total[i]['label']]
                ga=list(total[i].values())
                input.append(ga)
        return input


for i in range(101,201):
   data=[]
   path = 'E:/new_ai/replay/replay ('+str(i)+').xls'
   e = replay_data_analyzer(path, "Protoss")
   my_df = pd.DataFrame(e.get_input())
   my_df.to_csv('input'+str(i)+'.csv', index=False, header=False)

