#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:21:34 2019

Mini-Projet d'Algorithmique : Alignement de Séquences
"""

# =============================================================================
# Importations des bibliothèques
# =============================================================================
import math as m
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
    tab = res[1]
    cout = res[0]
    for i in range (len(x) + 1):
        for j in range (len(y) + 1):
            print(tab[i][j], end=' ')
        print()
    print("d(x_barre, y_barre) = ", cout)
    print()

def trace_dist_2(x, y): # Affichage propre de dist_12
    print("DIST_2 sur :\n", "x : ", x, "\n", "y : ", y, "\n", "--->")

    res = dist_2(x, y)
    tab = res[1]
    cout = res[0]
    for i in range (len(y) + 1):
        print(tab[i], end=' ')
    print()
    print("d(x_barre, y_barre) = ", cout)
    print()

def trace_sol_1(x, y):  # Affichage propre de sol_1
    print("SOL_1 sur :\n", "x : ", x, "\n", "y : ", y, "\n", "--->")
    D = dist_1(x, y)[1]
    res = sol_1(x, y, D)
    x_barre = []
    y_barre = []
    for i in range (len(res)):
        x_barre.append(res[i][0])
        y_barre.append(res[i][1])
    print(x_barre)
    print(y_barre)
    print()


def trace_sol_2(x, y):  # Affichage propre de sol_2
    print("SOL_2 sur :\n", "x : ", x, "\n", "y : ", y, "\n", "--->")
    res = sol_2(x, y)
    x_barre = res[0]
    y_barre = res[1]
    print(x_barre)
    print(y_barre)
    print()

def trace_calcul_cout(x, y):  # Affichage propre de calcul_cout
    print("calcul_cout sur :\n", "x : ", x, "\n", "y : ", y, "\n", "--->")
    res = sol_2(x, y)
    x_barre = res[0]
    y_barre = res[0]
    print("Cout de a chaine retourne par SOL_2(x, y) : ", calcul_cout(x_barre, y_barre))
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
        val_del = m.inf
        val_sub = m.inf
        val_ins = m.inf
        if (i-1>=0):                                                            # Si on ne deborde pas sur le haut du tableau
            if (D[i-1][j] + c_del == D[i][j]):                                  # Si la valeur est coherente
                val_del = D[i-1][j]                                                # On recupere la valeur associe a la suppression
            if (j-1>=0 and D[i-1][j-1] + c_sub(x[i-1], y[j-1]) == D[i][j]):     # Si on ne deborde pas sur la gauche du tableau et la valeur est coherente
                val_sub = D[i-1][j-1]                                              # On recupere la valeur associe a la substitution
        if (j-1 >= 0 and D[i][j-1] + c_ins == D[i][j]):                         # Si on ne deborde pas sur la gauche du tableau et la valeur est coherente
            val_ins = D[i][j-1]                                                    # On recupere la valeur associe a l'insertion
        if min(val_del, val_sub, val_ins) == val_sub:       # Substitution l'emporte (On donne la priorité à la substitution si plusieurs min)
            liste.append([x[i-1],y[j-1]])       # On fait la substitution
            i-=1                                # On se deplace d'une ligne vers le haut dans le tableau
            j-=1                                # On se deplace d'une colonne vers la gauche dans le tableau
        elif min(val_del, val_sub, val_ins) == val_del:     # Suppression l'emporte
            liste.append([x[i-1],'_'])          # gap dans ybarre
            i-=1                                # On se deplace d'une ligne vers le haut dans le tableau
        elif min(val_del, val_sub, val_ins) == val_ins:     # Insertion l'emporte
            liste.append(['_',y[j-1]])          # gap dans xbarre
            j-=1                                # On se deplace d'une colonne vers la gauche dans le tableau
    liste.reverse()                             # On inverse les chaines obtenues car on a commence depuis la fin
    return liste

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
            return align_lettre_mot(x, y)
    return R

def sol_2_non_opti(x,y):                # Utilisation de PROG_DYN au lieu de mot_gaps et align_lettre_mot
    i=int(len(x)/2)
    if len(x) > 1 and len(y) >= 1:
        j=coupure(x, y)
    if (len(x)<=1 or len(y)<=1):
        res = prog_dyn(x,y)
        return [res[1],res[2]]
    else:
        R_1 = sol_2(x[0:i],y[0:j])
        R_2 = sol_2(x[i:len(x)],y[j:len(y)])
        R = [R_1[0]+R_2[0],R_1[1]+R_2[1]]
    return R



#Q25
def coupure(x, y):                                # Retourne index_coupure, où couper y
    x_cp = x.copy()                               # Pour eviter tout problemes de manipulations
    y_cp = y.copy()
    i = int(len(x) / 2)
    index_coupure = len(y_cp)                     # On commence a la derniere colonne

    while (len(x_cp) > i):                        # Tant qu'on n'est pas arrive a la ligne i*
        D1 = dist_2(x_cp, y_cp)[1]                # ligne i
        D2 = dist_2(x_cp[:-1], y_cp)[1]           # ligne i-1

        val_del = m.inf
        val_sub = m.inf
        val_ins = m.inf
        
        index_antifail = index_coupure            # Sert a verifier si index_coupure a change a la fin
        x_antifail = x_cp.copy()                  # Sert a verifier si x_cp a change a la fin
        
        if (D2[index_coupure] + c_del == D1[index_coupure]):               # Si la valeur est coherente
            val_del = D2[index_coupure]                                    # On recupere la valeur associe a la suppression
        if (index_coupure - 1 >= 0):                                       # Si on ne deborde pas sur la gauche du tableau
            if(D2[index_coupure - 1] + c_sub(x_cp[-1], y_cp[index_coupure - 1]) == D1[index_coupure]):    # Si la valeur est coherente
                val_sub = D2[index_coupure - 1]                            # On recupere la valeur associe a la substitution
            if (D1[index_coupure - 1] + c_ins == D1[index_coupure]):       # Si la valeur est coherente
                val_ins = D1[index_coupure - 1]                            # On recupere la valeur associe a l'insertion

        if min(val_del, val_sub, val_ins) != val_del:                      # Si ce n'est pas une suppression
            index_coupure -= 1                                             # On s'est deplace d'une colonne vers la gauche

        if min(val_del, val_sub, val_ins) != val_ins:                      # Si ce n'est pas une insertion
            x_cp = x_cp[:-1]                                               # On s'est deplace d'une ligne vers le haut
        
        if (index_antifail==index_coupure) and (x_antifail==x_cp):         # Cas ou min(val_del, val_sub, val_ins) = val_del = v_ins
            x_cp = x_cp[:-1]                                               # On force une suppression
        
    return index_coupure

def coupure_non_opti(x, y):             # Utilisation de DIST_1 au lieu de DIST_2
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

# TEST DIST_1, DIST_2, SOL_1, SOL_2
print("TEST DIST_1, DIST_2, SOL_1, SOL_2\n")

print("Exemple page 13\n")
x = ['A', 'T', 'T', 'G', 'T', 'A']
y = ['A', 'T', 'C', 'T', 'T', 'A']
trace_dist_1(x, y)
trace_dist_2(x, y)
trace_calcul_cout(x, y)
trace_sol_1(x, y)
trace_sol_2(x, y)

# print("Fichier au choix")
# adn_7 = open_fichier("Inst_0001000_7.adn")
# x = adn_7[0]
# y = adn_7[1]
# trace_dist_1(x, y)
# trace_dist_2(x, y)
# trace_calcul_cout(x, y)
# trace_sol_1(x, y)
# trace_sol_2(x, y)


print("Exemple page 12")
c_sub_comp = 1          # Couts particuliers pour cet exemple
c_sub_incomp = 1
x = ['A', 'G', 'T', 'A', 'C', 'G', 'C', 'A']
y = ['T', 'A', 'T', 'G', 'C']
#x = ['A', 'G', 'T', 'A']
#y = ['T', 'A']
trace_dist_1(x, y)
trace_dist_2(x, y)
trace_calcul_cout(x, y)
trace_sol_1(x, y)
trace_sol_2(x, y)
c_sub_comp = 3      # Remet les couts normaux
c_sub_incomp = 4

print("FIN TEST DIST_1, DIST_2, SOL_1, SOL_2\n")
# FIN TEST DIST_1, DIST_2, SOL_1, SOL_2



# TEST COUPURE
print("TEST COUPURE\n")

print("Exemple page 12")
c_sub_comp = 1          # Couts particuliers pour cet exemple
c_sub_incomp = 1
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

c_sub_comp = 3      # Remet les couts normaux
c_sub_incomp = 4

print("FIN TEST COUPURE\n")
# FIN TEST COUPURE


#---------- Question 4 ----------
##|x|=15 et |y|=10
print("---------- Question 4 ----------")
n_x=15
m_y=10
import scipy.special as ss
sum=0
for i in range(1,m_y+1):
   sum+= ss.binom(n_x+i,i)*ss.binom(n_x,n_x+i-m_y)
print(sum)



#---------- Question 29 ----------
print("---------- Question 29 ----------")
L = ["Inst_0000010_7.adn" ,
    "Inst_0000010_8.adn" ,
    "Inst_0000010_44.adn" ,
    "Inst_0000012_13.adn" ,
    "Inst_0000012_32.adn" ,
    "Inst_0000012_56.adn" ,
    "Inst_0000013_45.adn" ,
    "Inst_0000013_56.adn" ,
    "Inst_0000013_89.adn" ,
    "Inst_0000014_7.adn" ,
    "Inst_0000014_23.adn" ,
    "Inst_0000014_83.adn" ,
    "Inst_0000015_2.adn" ,
    "Inst_0000015_4.adn" ,
    "Inst_0000015_76.adn" ,
    "Inst_0000020_8.adn" ,
    "Inst_0000020_17.adn" ,
    "Inst_0000020_32.adn",
    "Inst_0000050_3.adn",
    "Inst_0000050_9.adn",
    "Inst_0000050_77.adn",
    "Inst_0000100_3.adn",
    "Inst_0000100_7.adn",
    "Inst_0000100_44.adn",
    "Inst_0000500_3.adn"]
#    ,
#    "Inst_0000500_8.adn",
#    "Inst_0000500_88.adn",
#    "Inst_0001000_2.adn",
#    "Inst_0001000_7.adn",
#    "Inst_0001000_23.adn" ,
#    "Inst_0002000_3.adn" ,
#    "Inst_0002000_8.adn" ,
#    "Inst_0002000_44.adn",
#    "Inst_0003000_1.adn",
#    "Inst_0003000_10.adn",
#    "Inst_0003000_25.adn",
#    "Inst_0003000_45.adn",
#    "Inst_0005000_4.adn",
#    "Inst_0005000_32.adn",
#    "Inst_0005000_33.adn",
#    "Inst_0008000_32.adn",
#    "Inst_0008000_54.adn",
#    "Inst_0008000_98.adn",
#    "Inst_0010000_7.adn",
#    "Inst_0010000_8.adn",
#    "Inst_0010000_50.adn",
#    "Inst_0015000_3.adn",
#    "Inst_0015000_20.adn",
#    "Inst_0015000_30.adn",
#    "Inst_0020000_5.adn",
#    "Inst_0020000_64.adn",
#    "Inst_0020000_77.adn",
#    "Inst_0050000_6.adn",
#    "Inst_0050000_63.adn",
#    "Inst_0050000_88.adn",
#    "Inst_0100000_3.adn",
#    "Inst_0100000_11.adn",
#    "Inst_0100000_76.adn"]

RES_29 = []
for stuff in L:
   print(stuff)
   adn = open_fichier(stuff)
   x,y = adn[0],adn[1]
   start = time.time()
   prog_dyn(x,y)
   res_1 = time.time()-start
   print("\t", "Temps pour PROG_DYN : ", res_1)
   start = time.time()
   sol_2(x,y)
   res_2 = time.time()-start
   print("\t", "Temps pour SOL_2 : ", res_2)
   if res_1!=0:
       print("Rapport SOL_2 / PROG_DYN : ", res_2/res_1)
       RES_29.append(res_2/res_1)
   print("\n_____________________________\n")


# ---------- Question 30 ----------
print("---------- Question 30 ----------")
L = ["Inst_0000010_7" ,
    "Inst_0000010_8" ,
    "Inst_0000010_44" ,
    "Inst_0000012_13" ,
    "Inst_0000012_32" ,
    "Inst_0000012_56" ,
    "Inst_0000013_45" ,
    "Inst_0000013_56" ,
    "Inst_0000013_89" ,
    "Inst_0000014_7" ,
    "Inst_0000014_23" ,
    "Inst_0000014_83" ,
    "Inst_0000015_2" ,
    "Inst_0000015_4" ,
    "Inst_0000015_76" ,
    "Inst_0000020_8" ,
    "Inst_0000020_17" ,
    "Inst_0001000_23" ,
    "Inst_0002000_3" ,
    "Inst_0002000_8" ,
    "Inst_0002000_44"]

def open_fichier_q_30(file):
   fichier = open("Q_30/"+file+".adn","r")
   Reader = []
   Reader = fichier.read().split("\n")
   x=Reader[2].split()
   y=Reader[3].split()
   fichier.close()
   return [x,y]
RES = []
for stuff in L:
   adn = open_fichier_q_30(stuff)
   x,y = adn[0],adn[1]
   RES.append(dist_2(x,y)[0] - (len(x) - len(y)) * c_del)
print(RES)


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
tests sur plusieurs instances
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

*top sur grande taille en temps raisonnable 
Inst_0000500_3
au total environ 1000 lettres
1% de mémoire utilisée soit 163407.96 KiB
Mémoire totale : 16340796 KiB soit 15,5837974548 GiB

"""

# =============================================================================
# Courbes pour les differentes tâches
# =============================================================================
import matplotlib.pyplot as plt

x_axis = [10, 10, 10, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 20, 20, 20, 50, 50, 50, 100, 500, 1000, 2000, 3000, 5000, 8000, 10000]

y_PROG_DYN = []
y_DIST_1 = []
y_DIST_2 = []
y_SOL_2 = []


L = ["Inst_0000010_7.adn" ,
     "Inst_0000010_8.adn" ,
     "Inst_0000010_44.adn" ,
     "Inst_0000012_13.adn" ,
     "Inst_0000012_32.adn" ,
     "Inst_0000012_56.adn" ,
     "Inst_0000013_45.adn" ,
     "Inst_0000013_56.adn" ,
     "Inst_0000013_89.adn" ,
     "Inst_0000014_7.adn" ,
     "Inst_0000014_23.adn" ,
     "Inst_0000014_83.adn" ,
     "Inst_0000015_2.adn" ,
     "Inst_0000015_4.adn" ,
     "Inst_0000015_76.adn" ,
     "Inst_0000020_8.adn" ,
     "Inst_0000020_17.adn" ,
     "Inst_0000020_32.adn",
     "Inst_0000050_3.adn",
     "Inst_0000050_9.adn",
     "Inst_0000050_77.adn",
     "Inst_0000100_3.adn",
     "Inst_0000500_3.adn",
     "Inst_0001000_2.adn",
     "Inst_0002000_3.adn" ,
     "Inst_0003000_1.adn",
     "Inst_0005000_4.adn",
     "Inst_0008000_32.adn",
     "Inst_0010000_7.adn"]

stop_2 = False
for stuff in L:
    print(stuff)
    adn = open_fichier(stuff)
    x,y = adn[0],adn[1]

    start = time.time()
    prog_dyn(x,y)
    res_1 = time.time()-start
    y_PROG_DYN.append(res_1)
    print("\t",res_1)

    start = time.time()
    dist_2(x,y)
    res_3 = time.time()-start
    y_DIST_2.append(res_3)
    print("\t",res_3)

    start = time.time()
    dist_1(x,y)
    res_2 = time.time()-start
    y_DIST_1.append(res_2)
    print("\t",res_2)
    
    if stuff=="Inst_0000500_8.adn":         #à partir de Inst_0001000.. cela prend énormement de temps
        stop_2=True
    if stop_2:
        y_SOL_2.append(0)
        continue

    start = time.time()
    sol_2(x,y)
    res_2 = time.time()-start
    y_SOL_2.append(res_2)
    print("\t",res_2)

    print("\n_____________________________\n")


y_DIST_1 = [0.0, 0.0009987354278564453, 0.0, 0.0, 0.0, 0.0, 0.0009987354278564453, 0.0, 0.0, 0.0010089874267578125, 0.0009975433349609375, 0.0, 0.0, 0.0009758472442626953, 0.0010063648223876953, 0.000997781753540039, 0.0009987354278564453, 0.0, 0.002991199493408203, 0.004984855651855469, 0.003987312316894531, 0.021941661834716797, 0.26429152488708496, 1.2037787437438965, 4.613658428192139, 9.85163688659668, 26.640774250030518, 70.02363181114197, 111.80734896659851]
y_DIST_2 = [0.0, 0.000993967056274414, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009860992431640625, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.000997304916381836, 0.0, 0.0010082721710205078, 0.0029921531677246094, 0.00299072265625, 0.002992391586303711, 0.009971857070922852, 0.21941590309143066, 0.8497278690338135, 3.8118045330047607, 7.734331130981445, 20.058324813842773, 54.99260115623474, 81.61770153045654]
y_PROG_DYN =[0.0, 0.0, 0.0009853839874267578, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0009982585906982422, 0.0, 0.0009982585906982422, 0.0, 0.000997781753540039, 0.0009980201721191406, 0.0, 0.0, 0.0, 0.0, 0.001995086669921875, 0.002997159957885742, 0.0029916763305664062, 0.01097726821899414, 0.3061795234680176, 1.195802927017212, 4.929823875427246, 9.970312356948853, 27.570246696472168, 70.21383380889893, 110.4910933971405] 
y_SOL_2 = [0.0010178089141845703, 0.0010280609130859375, 0.0009872913360595703, 0.000997781753540039, 0.001993417739868164, 0.0009634494781494141, 0.001963376998901367, 0.0019927024841308594, 0.0020246505737304688, 0.0020253658294677734, 0.0019941329956054688, 0.002939939498901367, 0.0029914379119873047, 0.003988742828369141, 0.0029611587524414062, 0.006929636001586914, 0.006978750228881836, 0.006529569625854492, 0.08278012275695801, 0.10072040557861328, 0.10967206954956055, 0.7639968395233154, 96.54092025756836, 960.276718378067, 0, 0, 0, 0, 0]

plt.figure(1)
plt.plot(x_axis, y_PROG_DYN, label="PROG_DYN")
plt.title("Consommation CPU")
plt.xlabel("Taille du mot x")
plt.ylabel("Temps (s)")
plt.legend()
plt.show()

plt.figure(2)
plt.plot(x_axis, y_DIST_2, label = "DIST_2")
plt.title("Consommation CPU")
plt.xlabel("Taille du mot x")
plt.ylabel("Temps (s)")
plt.legend()
plt.show()

plt.figure(3)
plt.plot(x_axis, y_SOL_2, label = "SOL_2")
plt.title("Consommation CPU")
plt.xlabel("Taille du mot x")
plt.ylabel("Temps (s)")
plt.legend()
plt.show()

plt.figure(4)
plt.plot(x_axis, y_DIST_1, label = "DIST_1")
plt.title("Consommation CPU")
plt.xlabel("Taille du mot x")
plt.ylabel("Temps (s)")
plt.legend()
plt.show()

plt.figure(5)
plt.plot(x_axis, y_PROG_DYN, label="PROG_DYN")
plt.plot(x_axis, y_DIST_2, label = "DIST_2")
plt.plot(x_axis, y_SOL_2, label = "SOL_2")
plt.plot(x_axis, y_DIST_1, label = "DIST_1")
plt.title("Consommation CPU")
plt.xlabel("Taille du mot x")
plt.ylabel("Temps (s)")
plt.legend()
plt.show()
