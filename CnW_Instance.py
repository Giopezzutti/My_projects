#%%
from audioop import reverse
from operator import index
import numpy as np
import pandas as pd
import matplotlib as plt
import scipy as sc
from sklearn.metrics import euclidean_distances
from sqlalchemy import true
from ClarknWrightFunctions import *
import time

#%%
sheets_position1 = [0,1,2,3,4,5,6,7]
sheets_position2 = [0,1]
demand_distancias = [[0,7,5,7,6,7,4],[0,3,4,5,4,4,4,2,6,4]]
excel_file = ['COORDENADAS.xlsx','DISTANCIAS.xlsx']
num_of_routes1 = [5,8,2,2,20,6,3,2]
max_cap1 = [100,35,160,160,200,18,18,25]
max_cap2 = 18
num_of_routes2 = 2

#%%
for doc in excel_file:
    if doc == 'COORDENADAS.xlsx':
        for sheet in sheets_position1:
            df = pd.read_excel(doc,sheet)
            dist = node_distance('euclidean',df)
            dem = df['DEM'].to_numpy()
            st = time.time()
            R, Q, D, total_distance = ClarknWright(max_cap1[sheet],dist,num_of_routes1[sheet],dem,df)
            et = time.time()
            pt = et - st
            print(f'Total distance {sheet+1}: {total_distance} \n Processing time (seg): {pt}')
    else:
        for sheet in sheets_position2:
            df = pd.read_excel(doc,sheet)
            dist = node_distance('distance',df)
            dem = demand_distancias[sheet]
            st = time.time()
            R, Q, D, total_distance = ClarknWright(max_cap2,dist,num_of_routes2,dem,df)
            et = time.time()
            pt = et - st
            print(f'Total distance {sheet+9}: {total_distance} \n Processing time (seg): {pt}')



