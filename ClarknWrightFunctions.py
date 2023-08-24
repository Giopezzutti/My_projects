#%%
from audioop import reverse
from operator import index
import numpy as np
import pandas as pd
import scipy as sc
from sklearn.metrics import euclidean_distances
from sqlalchemy import true

#%%
def node_distance(type, df):
    if type == 'euclidean':
        posvec = df[['X','Y']]
        dist = euclidean_distances(posvec)
        return dist
    elif type == 'distance':
        dist = df.to_numpy()
        return dist



#%%
def savings(dist):
    '''This function reads a distance matrix between nodes 
    and outputs an descending array 
    of the savings of inserting a node into the route'''
    saving = []
    for i in range(1,len(dist)-1):
        for j in range(i+1,len(dist)):
            saving.append((i+1,j+1,dist[i,0]+dist[j,0]-dist[i,j]))
    dtype = [('i', int), ('j', int), ('s', float)]
    sv = np.flip(np.sort(np.array(saving, dtype=dtype), order='s'))
    return sv

#%%
def route_array_generator(k):
    '''This function generates an array with k dimensions'''
    R = []
    Q = []
    D = []
    for i in range(k):
        R.append([])
        Q.append(i-i)
        D.append(i-i)
    return R, Q, D

#%%
def find_in_route(i,j,R,k):
    '''Esta función busca los nodos i y j en el arreglo de las rutas y regresa
    dos arreglos con la posicion de estos nodos en las rutas o regresa arreglos vacios
    en el caso de que los nodos no se encuentren en ninguna ruta'''
    ri = []
    rj = []
    for t in range(k):
        if R[t]:
            for num in R[t]:
                if num == i:
                    ri.append(t), ri.append(R[t].index(i))
                elif num == j:
                    rj.append(t), rj.append(R[t].index(j))
    return ri, rj

#%%
def node_list(df):
    nodes = []
    for i in range(1,len(df)):
        nodes.append(i+1)
    return nodes

#%%
def ClarknWright(maxQ,dist,k,demand,df):
    nodos = node_list(df)
    R, Q, D = route_array_generator(k)
    sv = savings(dist)
    while nodos and sv.size != 0:
        i = sv[0][0]
        j = sv[0][1]
        ri, rj = find_in_route(i,j,R,k)
        if not(ri) and not(rj): 
            '''Si ningun nodo esta asignado a alguna ruta, 
            se le asigna a cualquier ruta vacia.'''
            if demand[i-1] + demand[j-1] <= maxQ:
                for t in range(k):
                    if not(R[t]):
                        R[t].append(i), R[t].append(j)
                        Q[t] = demand[i-1] + demand[j-1]
                        D[t] += dist[i-1, j-1]
                        nodos.pop(nodos.index(i))
                        nodos.pop(nodos.index(j))
                        break
        elif ri and not(rj):
            '''Si el nodo i esta asignado a una ruta pero no el nodo j
            se busca si se puede agregar el nodo j a la ruta'''
            if (ri[1] == 0 or ri[1] == len(R[ri[0]])-1) and (Q[ri[0]] + demand[j-1] <= maxQ):
                
                if ri[1] == 0:
                    R[ri[0]].insert(0,j)
                    Q[ri[0]] += demand[j-1]
                    D[ri[0]] += dist[i-1, j-1]
                    nodos.pop(nodos.index(j))
                     
                elif ri[1] == len(R[ri[0]])-1:
                    R[ri[0]].append(j)
                    Q[ri[0]] += demand[j-1]
                    D[ri[0]] += dist[i-1, j-1]
                    nodos.pop(nodos.index(j))
#            else:
#                for t in range(k):
#                    if not R[t]:
#                        R[t].append(j)
#                        Q[t] += demand[j-1] 
#                        nodos.pop(nodos.index(j))
#                        break

        elif not(ri) and rj:
            '''Si el nodo j esta asignado a una ruta pero no el nodo i
            se busca si se puede agregar el nodo i a la ruta'''
            if (rj[1] == 0 or rj[1] == len(R[rj[0]])-1) and Q[rj[0]] + demand[i-1] <= maxQ:

                if rj[1] == 0:
                    R[rj[0]].insert(0,i)
                    Q[rj[0]] += demand[i-1] 
                    D[rj[0]] += dist[i-1, j-1]
                    nodos.pop(nodos.index(i))   
                elif rj[1] == len(R[rj[0]])-1:
                    R[rj[0]].append(i)
                    Q[rj[0]] += demand[i-1]
                    D[rj[0]] += dist[i-1, j-1]
                    nodos.pop(nodos.index(i))
#            else:
#                for t in range(k):
#                    if not R[t]:
#                        R[t].append(i)
#                        Q[t] += demand[i-1]
#                        nodos.pop(nodos.index(i))
#                        break
        
        elif ri and rj:
            '''Si los dos nodos estan asignados a distintas rutas,
            se verifica si se pueden combinar las rutas'''
            if ri[0] != rj[0]:
                if ((ri[1] == 0 or ri[1] == len(R[ri[0]])-1) and ((rj[1] == 0 or rj[1] == len(R[rj[0]])-1))) and Q[ri[0]] + Q[rj[0]] <= maxQ:
                    Q[ri[0]] += Q[rj[0]]
                    if ri[1] == 0:
                        R[ri[0]] = R[rj[0]] + R[ri[0]]  
                        D[ri[0]] += dist[i-1, j-1] + D[rj[0]]
                           
                    else:
                        R[ri[0]] = R[ri[0]] + R[rj[0]] 
                        D[ri[0]] += dist[i-1, j-1] + D[rj[0]]
                        
                    R[rj[0]].clear()
                    Q[rj[0]] = 0
                    D[rj[0]] = 0 

        sv = np.delete(sv,0)
        
    total_distance = 0
    if not(nodos):
        for ii in range(k):
            f = R[ii][0]-1
            l = R[ii][-1]-1
            D[ii] += dist[0,f] + dist[0,l]
            R[ii].append(1)
            R[ii].insert(0,1)
            total_distance += D[ii]
    else:
       total_distance = 'No se encontro solución mediante el algoritmo de Clark and Wright'
    return R, Q, D, total_distance