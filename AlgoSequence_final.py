#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:21:34 2019

@author: 3531662   
"""

# =============================================================================
# Importations des bibliothèques
# =============================================================================
import math as m
import numpy as np
import time

# =============================================================================
# Bibliothèques des fonctions
# =============================================================================

#ouverture de fichier
def open_fichier(file):                                 # Retourne les deux chaines du fichier
    fichier = open("Instances_genome/"+file,"r")        # On ouvre le fichier
    Reader = []
    Reader = fichier.read().split("\n")                 # On le lit ligne par ligne
    x=Reader[2].split()                                 # On recupere la ligne 3 (x)
    y=Reader[3].split()                                 # On recupere la ligne 4 (y)
    fichier.close()                                     # On ferme le flux
    return [x,y]


c_ins = 2
c_del = c_ins
c_sub_idem = 0

# Couts normaux
c_sub_comp = 3
c_sub_incomp = 4

# Couts exemple page 12
# c_sub_comp = 1
# c_sub_incomp = 1

def c_sub(a,b):              # Retourne le cout de substitution entre a et b
    if a==b:
        return c_sub_idem    # Deux lettres identiques
    elif (a=='A' and b=='T') or (a=='T' and b=='A') or (a=='G' and b=='C') or (a=='C' and b=='G'):
        return c_sub_comp    # Deux lettres compatibles
    else:
        return c_sub_incomp    # Deux lettres incompatibles

def trace_dist_1(x, y): # Affichage propre de dist_1
    print("DIST_1 sur :\n", "x : ", x, "\n", "y : ", y, "\n", "--->")

    res = dist_1(x, y)
    for i in range (len(x) + 1):
        for j in range (len(y) + 1):
            print(res[1][i][j], end=' ')
        print()
    print()

def trace_sol_1(x, y):  # Affichage propre de sol_1
    print("SOL_1 sur :\n", "x : ", x, "\n", "y : ", y, "\n", "--->")
    D = dist_1(x, y)[1]
    res = sol_1(x, y, D)
    listx = []
    listy = []
    for i in range (len(res)):
        listx.append(res[i][0])
        listy.append(res[i][1])
    print(listx)
    print(listy)
    print()

def calcul_cout(x, y):                      # Retourne C(x,y) (pour verifier que les chaines de sol ont un cout d(x;y)
    cout = 0
    for i in range(len(x)):
        if (x[i] == "_" or y[i] == "_"):
            cout += c_ins
        else:
            cout += c_sub(x[i], y[i])
    return cout


def dist_naif(x,y):
    return dist_naif_rec(x,y,-1,-1,0,m.inf)

def dist_naif_rec(x,y,i,j,c,dist):
    if (len(x)-1)==i and j==(len(y)-1):
        if (c<dist):
            dist = c
    else:
        if (i<len(x)-1) and (j<len(y)-1):
            dist = dist_naif_rec(x,y,i+1,j+1,c+c_sub(x[i+1],y[j+1]),dist)
        if (i<len(x)-1):
            dist = dist_naif_rec(x,y,i+1,j,c+c_del,dist)
        if (j<len(y)-1):
            dist = dist_naif_rec(x,y,i,j+1,c+c_ins,dist)
    return dist

def dist_1(x, y):                       # Retourne d(x, y) et le tableau
    D = []

    for j in range(0,len(x)+1):         # Toutes les cases du tableau a +inf
        D.append([])
        for i in range(0,len(y)+1):
            D[j].append(m.inf)

    D[0][0] = 0
    
    for i in range(1, len(y)+1):        # Couts de la premiere ligne
        D[0][i] = D[0][i-1] + c_ins
        
    for i in range(1, len(x)+1):
        D[i][0] = D[i-1][0] + c_del     # Couts de la premiere colonne

    for i in range(1, len(x)+1):        # D[i][j] = plus petite des 3 valeurs possibles
        for j in range(1, len(y)+1):
            D[i][j] = min(D[i-1][j] + c_del, D[i][j-1] + c_ins, D[i-1][j-1] + c_sub(x[i-1], y[j-1]))

    return [D[len(x)][len(y)],D]

def sol_1(x, y, D):                             # Retourne l'alignement optimal de (x, y)
    i = len(x)                                  # On commence depuis la fin du tableau
    j = len(y)
    liste = []

    while i != 0 or j != 0:                     # Tant qu'on est pas arrive au debut
        val1 = m.inf
        val2 = m.inf
        val3 = m.inf
        if (i-1>=0):                                                            # Si on ne deborde pas sur le haut du tableau
            if (D[i-1][j] + c_del == D[i][j]):                                  # Si la valeur est coherente
                val1 = D[i-1][j]                                                # On recupere la valeur associe a la suppression
            if (j-1>=0 and D[i-1][j-1] + c_sub(x[i-1], y[j-1]) == D[i][j]):     # Si on ne deborde pas sur la gauche du tableau et la valeur est coherente
                val2 = D[i-1][j-1]                                              # On recupere la valeur associe a la substitution
        if (j-1 >= 0 and D[i][j-1] + c_ins == D[i][j]):                         # Si on ne deborde pas sur la gauche du tableau et la valeur est coherente
            val3 = D[i][j-1]                                                    # On recupere la valeur associe a l'insertion
        if min(val1, val2, val3) == val2:       # Substitution l'emporte (On donne la priorité à la substitution si plusieurs min)
            liste.append([x[i-1],y[j-1]])       # On fait la substitution
            i-=1                                # On se deplace d'une ligne vers le haut dans le tableau
            j-=1                                # On se deplace d'une colonne vers la gauche dans le tableau
        elif min(val1, val2, val3) == val1:     # Suppression l'emporte
            liste.append([x[i-1],'_'])          # gap dans ybarre
            i-=1                                # On se deplace d'une ligne vers le haut dans le tableau
        elif min(val1, val2, val3) == val3:     # Insertion l'emporte
            liste.append(['_',y[j-1]])          # gap dans xbarre
            j-=1                                # On se deplace d'une colonne vers la gauche dans le tableau
    liste.reverse()                             # On inverse les chaines obtenues car on a commence depuis la fin
    return liste

# def sol_1v2(x, y, D):         # MEILLEUR OU PAS ?
#     i = len(x)                                                                  # On commence depuis la fin du tableau
#     j = len(y)
#     liste = []
#     while i != 0 or j != 0:                                                     # Tant qu'on est pas arrive au debut
#         val1 = m.inf
#         val2 = m.inf
#         val3 = m.inf
#         if (i-1>=0):                                                            # Si on ne deborde pas sur le haut du tableau
#             if (D[i-1][j] + c_del == D[i][j]):
#                 val1 = D[i-1][j]                                                # On recupere la valeur associe a la suppression
#             if (j-1>=0 and D[i-1][j-1] + c_sub(x[i-1], y[j-1]) == D[i][j]):     # Si on ne deborde pas sur la gauche du tableau
#                 val2 = D[i-1][j-1]                                              # On recupere la valeur associe a la substitution
#         if (j-1 >= 0 and D[i][j-1] + c_ins == D[i][j]):                         # Si on ne deborde pas sur la gauche du tableau
#             val3 = D[i][j-1]                                                    # On recupere la valeur associe a l'insertion
#
#         if min(val1, val2, val3) == val2:                                       # Substitution l'emporte (On donne la priorité à la substitution si plusieurs min)
# #            if len(y)!=0:
# #                if c_sub(x[i-1],y[j-1])!=4:            # Si ce n'est pas une substitution incompatible
#                     liste.append([x[i-1],y[j-1]])       # On fait la substitution
#                     i-=1                                # On se deplace d'une ligne vers le haut dans le tableau
#                     j-=1                                # On se deplace d'une colonne vers la gauche dans le tableau
# #                elif len(x)>len(y):                     # Sinon si x plus grand que y
# #                    liste.append([x[i-1],'_'])          # On fait une suppression, gap dans ybarre
# #                    i-=1                                # On se deplace d'une ligne vers le haut dans le tableau
# #                elif len(x)<=len(y):                    # Sinon si y plus grand que y
# #                    liste.append(['_',y[j-1]])          # On fait une insertion, gap dans xbarre
# #                    j-=1                                # On se deplace d'une colonne vers la gauche dans le tableau
#         elif min(val1, val2, val3) == val1:             # Suppression l'emporte
#             liste.append([x[i-1],'_'])                  # gap dans ybarre
#             i-=1                                        # On se deplace d'une ligne vers le haut dans le tableau
#         elif min(val1, val2, val3) == val3:             # Insertion l'emporte
#             liste.append(['_',y[j-1]])                  # gap dans xbarre
#             j-=1                                        # On se deplace d'une colonne vers la gauche dans le tableau
#     liste.reverse()                                     # On inverse les chaines obtenues car on a commence depuis la fin
#     return liste                                        # On retourne l'alignement de cout minimal

def prog_dyn(x,y):                      # Retourne d(x,y) et l'alignement associe
    rep = dist_1(x,y)                   # On calcule d(x,y) et le tableau associe
    x_sol = []
    y_sol = []
    L = sol_1(x,y,rep[1])               # On recupere l'alignement associe
    for i in range(len(L)):
        x_sol.append(L[i][0])
        y_sol.append(L[i][1])
    return [rep[0],x_sol,y_sol]


def dist_2(x,y):                            # Retourne d(x,y) et la dernier ligne du tableau
    D = [0]                                 # Premiere case à 0
    
    for i in range(1, len(y)+1):            # Premiere ligne d'insertion
        D.append(D[i-1] + c_ins)

    for i in range(1, len(x)+1):
        for j in range(0, len(y)+1):
            if (j==0):                      # Premiere case
                tmp = D[j]                  # On recupere D[j] pour calculer le min a la case suivante
                D[j] = D[j] + c_del         # On affecte la nouvelle valeur de D[j]
            else:                           # Autres cases
                tmp_val = min(D[j] + c_del, D[j-1] + c_ins, tmp + c_sub(x[i-1], y[j-1]))    # Calcul de D[j]
                tmp = D[j]                  # On recupere D[j] pour calculer le min a la case suivante
                D[j] = tmp_val              # On affecte la nouvelle valeur de D[j]
    return [D[-1],D]

#Q21
def mot_gaps(k):                # Retourne un mot constitue de k gaps
    d = []
    for i in range(1, k+1):
        d += ["_"]
    return d

#Q22
def align_lettre_mot(x,y):                  # Retourne l'alignement optimal pour un mot de taille 1 et un mot y non vide
    if len(x)>1:
        print("Condition sur x NOT MET")
    if len(y)==0:
        print("Condition sur y NOT MET")
    return [prog_dyn(x,y)[1], prog_dyn(x, y)[2]]

#Q24
def sol_2(x,y):                                     # Retourne l'alignement optimal de (x,y)
    i=int(len(x)/2)                                 # On veut couper x en son milieu
    if len(x) > 1 and len(y) >= 1:                  # Si |x| > 1 et |y| >= 1
        j = coupure(x, y)                           # On calcule où couper y pour avoir une optimalite a la fin
        R_1 = sol_2(x[0:i], y[0:j])                 # Recursion 1er partie
        R_2 = sol_2(x[i:len(x)],y[j:len(y)])        # Recursion 2eme partie
        R = [R_1[0]+R_2[0],R_1[1]+R_2[1]]           # Fusion des resultats

    else:                                           # Sinon |x| = 1 (car x/2) ou |y| = 0
        if(len(y) == 0):                            # Si |y| = 0
            return[x, mot_gaps(len(x))]
        else:                                       # Sinon |y| != 0  donc |x| = 1
            return [x, align_lettre_mot(x, y)[1]]
    return R

# def sol_2_non_opti(x,y):
#     i=int(len(x)/2)
# #    if (len(x)!=0 and len(y)!=0):
#     if len(x) > 1 and len(y) >= 1:      #J'ai add ca
#         j=coupure(x, y)
# #    else:
# #        if len(x)==0:
# #            return [mot_gaps(len(y)),y]
# #        elif len(y)==0:
# #            return [x,mot_gaps(len(x))]
#
#     if (len(x)<=1 or len(y)<=1):
#         res = prog_dyn(x,y)
# #        print("feuille")
#         return [res[1],res[2]]
#     else:
# #        print("feuille")
#         R_1 = sol_2(x[0:i],y[0:j])
#         R_2 = sol_2(x[i:len(x)],y[j:len(y)])
#         R = [R_1[0]+R_2[0],R_1[1]+R_2[1]]
#     return R



#Q25
def coupure(x, y):                      # Retourne index_coupure, où couper y
    i = int(len(x) / 2)
    index_coupure = len(y)                  # On commence a la derniere colonne

    while (len(x) > i):                     # Tant qu'on n'est pas arrive a la ligne i*
        D1 = dist_2(x, y)[1]                # ligne i
        D2 = dist_2(x[:-1], y)[1]           # ligne i-1

        val1 = m.inf
        val2 = m.inf
        val3 = m.inf
        if (D2[index_coupure] + c_del == D1[index_coupure]):            # Si la valeur est coherente
            val1 = D2[index_coupure]                                    # On recupere la valeur associe a la suppression
        if (index_coupure - 1 >= 0):                                    # Si on ne deborde pas sur la gauche du tableau
            if(D2[index_coupure - 1] + c_sub(x[-1], y[index_coupure - 1]) == D1[index_coupure]):    # Si la valeur est coherente
                val2 = D2[index_coupure - 1]                            # On recupere la valeur associe a la substitution
            if (D1[index_coupure - 1] + c_ins == D1[index_coupure]):    # Si la valeur est coherente
                val3 = D1[index_coupure - 1]                            # On recupere la valeur associe a l'insertion

        if min(val1, val2, val3) != val1:           # Si ce n'est pas une suppression
            index_coupure -= 1                      # On s'est deplace d'une colonne vers la gauche

        if min(val1, val2, val3) != val3:           # Si ce n'est pas une insertion
            x = x[:-1]                              # On s'est deplace d'une ligne vers le haut

    return index_coupure

def coupure_non_opti(x, y):
    i = int(len(x)/2)
    D = dist_1(x, y)
    L = sol_1(x,y,D[1])
    cpt_L = 0
    cpt_ligne = 0
    cpt_colonne = 0
    
    while(cpt_ligne != i):
        if(L[cpt_L][0] == '_'):     # Une insertion
            cpt_colonne+=1
            cpt_L+=1
        elif(L[cpt_L][1] == '_'):   # Une suppression
            cpt_ligne+=1
            cpt_L+=1
        else:                       # Une substitution
            cpt_colonne+=1
            cpt_ligne+=1
            cpt_L+=1
    return cpt_colonne
    

# =============================================================================
#Tests
# =============================================================================

# TEST DIST_1 et SOL_1
print("TEST DIST_1 ET SOL_1\n")

print("Exemple page 13\n")
x = ['A', 'T', 'T', 'G', 'T', 'A']
y = ['A', 'T', 'C', 'T', 'T', 'A']
trace_dist_1(x, y)
trace_sol_1(x, y)

# print("Fichier au choix")
# adn_7 = open_fichier("Inst_0001000_7.adn")
# x = adn_7[0]
# y = adn_7[1]
# trace_dist_1(x, y)
# trace_sol_1(x, y)
# x_sol = prog_dyn(x, y)[1]
# y_sol = prog_dyn(x, y)[2]
# print("calcul_cout : ", calcul_cout(x_sol, y_sol))

# print("Exemple page 12 COUT A MODIFIER !! --> cf ligne 39")
# x = ['A', 'G', 'T', 'A', 'C', 'G', 'C', 'A']
# y = ['T', 'A', 'T', 'G', 'C']
# #x = ['A', 'G', 'T', 'A']
# #y = ['T', 'A']
# trace_dist_1(x, y)
# trace_sol_1(x, y)

print("FIN TEST DIST_1 SOL_1\n")
# FIN TEST DIST_1 SOL_1



# TEST COUPURE
print("TEST COUPURE\n")

x = ['A', 'G', 'T', 'A', 'C', 'G', 'C', 'A']
y = ['T', 'A', 'T', 'G', 'C']

# x = ['A', 'G', 'T', 'A']
# y = ['T', 'A']

# x = ['T', 'A']
# y = ['T', 'A']

# x = ['C', 'G', 'C', 'A']
# y = ['T', 'G', 'C']

# x = ['A', 'T', 'T', 'G', 'T', 'A']
# y = ['A', 'T', 'C', 'T', 'T', 'A']

print("Test de coupure_non_opti : ", coupure_non_opti(x, y))
print("Test de coupure : ", coupure(x, y))

print("FIN TEST COUPURE\n")
# FIN TEST COUPURE



# TEST SOL_2
print("TEST SOL_2\n")

x = ['A', 'G', 'T', 'A', 'C', 'G', 'C', 'A']
y = ['T', 'A', 'T', 'G', 'C']

trace_sol_1(x, y)
print(sol_2(x,y))

print("FIN TEST SOL_2\n")
# FIN TEST SOL_2










# adn_7 = open_fichier("Inst_0001000_7.adn")
#
# x = adn_7[0]
# y = adn_7[1]
# start = time.time()
# res_pd = prog_dyn(x,y)
# print(time.time()-start)
#
# start = time.time()
# res_sol2 = sol_2(x,y)
# print(time.time()-start)
#
# print(" prog dn = sol2 ?",res_pd[1]==res_sol2[0])
# print(res_pd[2]==res_sol2[1])
#
# print([res_pd[1],res_pd[2]])
# print(res_sol2)
# print(res_pd[0])
#
# print(calcul_cout(res_pd[1],res_pd[2]))
# print(calcul_cout(res_sol2[0],res_sol2[1]))









#Question 4
#|x|=15 et |y|=10
#n_x=15
#m_y=10
#
#sum=0
#for i in range(1,m_y+1):
#    sum += ((m.factorial(n_x+1))/(m.factorial(i)*m.factorial(m_y-i)*m.factorial(n_x+i-m_y)))
#print(sum)

#Question 4
#|x|=15 et |y|=10
#import
#n_x=15
#m_y=10
#import scipy.special as ss
#sum=0
#for i in range(1,m_y+1):
#    sum+= ss.binom(n_x+i,i)*ss.binom(n_x,n_x+i-m_y)
#print(sum)



#Question 2)
# adn_7 = open_fichier("Inst_0000010_44.adn")
# x = adn_7[0]
# y = adn_7[1]
#start = time.time()
#print(dist_naif(x, y))
#print(time.time()-start)
##x = ['A', 'T', 'T', 'G', 'T', 'A']
##y = ['A', 'T', 'C', 'T', 'T', 'A']
##y = ['A', 'T', 'C', 'T', 'T', 'A']
#
#start = time.time()
#print(dist_naif(x, y))
#print(time.time()-start)
#
#start = time.time()
# dist_1(x, y)
#print(time.time()-start)
# trace_dist_1(x, y)

#start = time.time()
#print(dist_2(x,y))
#print(time.time()-start)


#start = time.time()
#dist = dist_1(x, y)
#print(time.time()-start)
#for i in range (len(dist[1][1])):
#    for j in range (len(dist[1][i])):
#        print(dist[1][i][j], end=' ')
#    print()
#
#start = time.time()
#print(sol_1(x, y, dist[1]))
#print(time.time()-start)



#print(mot_gaps(5))
#print(align_lettre_mot(['G', 'T', 'C', 'T', 'T', 'C'],['A']))










#---------- Question 30 ----------
#L = ["Inst_0000010_7" ,
#     "Inst_0000010_8" ,
#     "Inst_0000010_44" ,
#     "Inst_0000012_13" ,
#     "Inst_0000012_32" ,
#     "Inst_0000012_56" ,
#     "Inst_0000013_45" ,
#     "Inst_0000013_56" ,
#     "Inst_0000013_89" ,
#     "Inst_0000014_7" ,
#     "Inst_0000014_23" ,
#     "Inst_0000014_83" ,
#     "Inst_0000015_2" ,
#     "Inst_0000015_4" ,
#     "Inst_0000015_76" ,
#     "Inst_0000020_8" ,
#     "Inst_0000020_17" ,
#     "Inst_0001000_23" ,
#     "Inst_0002000_3" ,
#     "Inst_0002000_8" ,
#     "Inst_0002000_44"]
#
# def open_fichier_q_30(file):
#     fichier = open("Q_30/"+file+".adn","r")
#     Reader = []
#     Reader = fichier.read().split("\n")
#     x=Reader[2].split()
#     y=Reader[3].split()
#     fichier.close()
#     return [x,y]
#
# RES = []
# for stuff in L:
#    adn = open_fichier_q_30(stuff)
#    x,y = adn[0],adn[1]
#    RES.append(dist_2(x,y)[0]-(len(x)-len(y))*c_del)
#print(RES)


"""

---------- TACHE A ----------
adn_7 = open_fichier("Inst_0000010_44.adn")
print(dist_naif(adn_7 [0],adn_7 [1]))
10

adn_7 = open_fichier("Inst_0000010_7.adn")
print(dist_naif(adn_7 [0],adn_7 [1]))def prog_dyn(x,y)
8

adn_7 = open_fichier("Inst_0000010_8.adn")
print(dist_naif(adn_7 [0],adn_7 [1]))
2
    
Inst_0000012_32 : 13.088070631027222 secondes
taille 12 / 9

Inst_0000012_32 36.46426343917847 secondes 
taille 12 / 10
on ajoute G à la fin de y

Inst_0000012_56 : 41.71873879432678 secondes
taille 11 / 11
on supprime la dernière lettre dans x

Inst_0000012_56 : 90.03461003303528 secondes
taille 12 / 11

18588 3531662   20   0   17368   9264   5720 R  99,7   0,1   0:07.05 python3   
0.1% de mémoire utilisée, mémoire total
15946,5 MiB au total
Donc l'éxécution pour Inst_0000012_32, utilise environ 15,9465MiB
"""


"""
---------- TACHE B ----------
*tests sur plsrs instances
adn_7 = open_fichier("Inst_0000010_44.adn")
print(prog_dyn(adn_7 [0],adn_7 [1]))


adn_7 = open_fichier("Inst_0000010_7.adn")
print(prog_dyn(adn_7 [0],adn_7 [1]))


adn_7 = open_fichier("Inst_0000010_8.adn")
print(prog_dyn(adn_7 [0],adn_7 [1]))


*courbe CPU

*top sur grande taille
Inst_0015000_30
au total environ 28000 lettres
60.1% de mémoire utilisée soit 9820818.396 KiB
Mémoire totale : 16340796 KiB soit 15,5837974548 GiB
~154 secondes

Inst_0020000_5
au total environ 37000 lettres
92.4% de mémoire utilisée soit 15098895.504 KiB soit 14.3994288 GiB
Mémoire totale : 16340796 KiB soit 15,5837974548 GiB
crash
"""






"""
---------- TACHE C ----------, idem que tache B
adn_7 = open_fichier("Inst_0000010_44.adn")
print(dist_2(adn_7 [0],adn_7 [1]))


adn_7 = open_fichier("Inst_0000010_7.adn")
print(dist_2(adn_7 [0],adn_7 [1]))


adn_7 = open_fichier("Inst_0000010_8.adn")
print(dist_2(adn_7 [0],adn_7 [1]))


    DIST_2
Inst_0000012_32 : 6.961822509765625e-05 secondes
taille 12 / 9

Inst_0000012_56 : 0.0001049041748046875 secondes
taille 12 / 11

Inst_0015000_30.adn : 107.99493622779846 secondes
taille 15000 / 13360



*top sur grande taille
Inst_0015000_30
au total environ 28000 lettres
1% de mémoire utilisée soit 163407.96 KiB
Mémoire totale : 16340796 KiB soit 15,5837974548 GiB
115.61878108978271 secondes

Inst_0020000_5
au total environ 37000 lettres
1% de mémoire utilisée soit 163407.96 KiB
Mémoire totale : 16340796 KiB soit 15,5837974548 GiB
203.42932891845703 secondes
"""


"""
---------- TACHE D ----------

* voir supra
* a faire
* 
"""

# =============================================================================
# 
# =============================================================================
