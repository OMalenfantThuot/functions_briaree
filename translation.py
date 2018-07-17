#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Script pour translater les fichiers positions .ascii
import numpy as np
import io_bigdft as io

infile = str(input('Entrer le nom du fichier à translater:\n'))
outfile = 'out_'+infile
data_pos, data_at = io.read_ascii(infile)

delx = float(input('Translation en x (unités atomiques):\n'))
delz = float(input('Translation en z (unités atomiques):\n'))

data_pos[:,0] += delx
data_pos[:,2] += delz

with open(infile,'r') as f:
    with open(outfile,'w') as g:
        g.write(f.readline())
        cell = f.readline()+f.readline()
        g.write(cell)
        cell = np.array(cell.split())
        while 1:
            line = f.readline()
            if line[0] == '#':
                g.write(line)
                continue
            else:
                break
        
        Nat = len(data_at)
        for i in range(Nat):
            g.write('%18.15f'%(data_pos[i,0])+"\t"+'%18.15f'%(data_pos[i,1])+"\t"+'%18.15f'%(data_pos[i,2])+"\t"+str(data_at[i])+"\n")
