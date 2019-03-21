import math
import matplotlib.pyplot as plt
import numpy as np

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

def plot_hex(b,**kwargs):
    r = b/math.sqrt(3)
    hex1 = [-r/2,-r,-r/2, r/2,r,r/2,-r/2]
    hex2 = [ b/2, 0,-b/2,-b/2,0,b/2, b/2]
    plt.plot(hex1,hex2,**kwargs)
    plt.axis('equal')
    return

def plot_rec(x,y,**kwargs):
    rec1 = [x/2, x/2, -x/2, -x/2, x/2]
    rec2 = [y/2, -y/2, -y/2, y/2, y/2]
    plt.plot(rec1,rec2,**kwargs)
    plt.axis('equal')
    return

def sin_interpolate(ener1, ener2, time):
    a = (ener2  - ener1)/2
    h = (time[-1] + time[0])/2
    b = np.pi / (time[-1] - time[0])
    c = (ener1 + ener2)/2
    return a * np.sin(b * (time - h)) + c
