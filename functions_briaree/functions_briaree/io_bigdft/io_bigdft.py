import numpy as np
import math
import matplotlib.pyplot as plt


def read_ascii(filename):
#Fonction pour lire les fichiers positions .ascii de BigDFT
#data_pos: contient les positions des atomes
#data_at: contient les types atomiques

    data_pos = []
    data_at = []
    data_spin = []
    coord = 'absolute'

    with open(filename,'r') as f:

        for line in f:
            l = line.split()

            if (not line[0] == '#') and (len(l) > 3):
                data_pos.append([float(l[0]),float(l[1]),float(l[2])])
                data_at.append(l[3])
                if len(l) == 4:
                    data_spin.append(0)
                elif len(l) == 6:
                    data_spin.append(int(l[5][0]))
                else:
                    raise Exception('A line is not recognized:\n'+line)

            elif l[0] == '#keyword:':
                if l[1] in ['atomicd0','atomic','bohr','bohrd0','angstroem','angstroemd0']:
                    units = l[1]
                elif l[1] in ['surface','periodic','freeBC']:
                    geocode = l[1]
                elif l[1] == 'reduced':
                    coord = 'reduced'
                else:
                    raise Exception('Keyword not recognized')

    return data_pos,data_at,data_spin,units,geocode,coord
            
    
    

def first_BZ_rec(x,y,bx,by):
#Cette fonction vérifie si un point est à l'intérieur de
#la première zone de brillouin rectangulaire.
#x,y : coordonnées du point à  vérifier
#bx,by : norme des vecteurs bx et by
    if (-bx/2 < x <= bx/2) & (-by/2 < y <= by/2):
        return True
    else:
        return False
        

def first_BZ_hex(x,y,b):
#Cette fonction vérifie si un point est à l'intérieur de
#la première zone de brillouin hexagonale définie par les
#vecteurs réciproques de norme b.
#x,y : coordonnées du point à  vérifier
#b : norme des vecteurs b
    if (x > 0) & (y >= 0):
        theta = math.atan(y/x)
    elif (x < 0):
        theta = math.pi + math.atan(y/x)
    elif (x > 0) & (y < 0):
        theta = 2*math.pi + math.atan(y/x)
    elif (x == 0):
        if y >= 0: theta = math.pi/2
        if y < 0: theta = (3./2)*math.pi
    theta = (theta % (math.pi/3)) - math.pi/6
    l = np.around(np.sqrt(x**2+y**2), decimals = 7)
    lim = np.around(b/(2.*math.cos(theta)), decimals = 7)
    #Retourne un permier true si le point est à l'intérieur
    #Le second est seulement vrai si le point est exactement à la frontière
    if l == lim:
        return True, True
    if l < lim:
        return True, False
    if l > lim:
        return False, False

def plot_hex(b,color='k',label=''):
    r = b/math.sqrt(3)
    hex1 = [-r/2,-r,-r/2, r/2,r,r/2,-r/2]
    hex2 = [ b/2, 0,-b/2,-b/2,0,b/2, b/2]
    plt.plot(hex1,hex2,color=color,label=label)
    plt.axis('equal')
    return

def plot_rec(x,y,color='g',label=''):
    rec1 = [x/2, x/2, -x/2, -x/2, x/2]
    rec2 = [y/2, -y/2, -y/2, y/2, y/2]
    plt.plot(rec1,rec2,color=color,label=label)
    plt.axis('equal')
    return
