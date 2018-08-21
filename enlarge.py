#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functions_briaree as fbr

"""
Script pour agrandir les fichiers positions .ascii du graphène
S'appelle comme un éxécutable

"""
infile = str(input('Entrer le nom du fichier a agrandir:\n'))

Pos = fbr.Posinp()
Pos.def_from_file(infile)
outfile = 'out_'+infile.strip('.' + Pos.filetype)

xsize = int(input('Nouvelle taille en x:\n'))
zsize = int(input('Nouvelle taille en z:\n'))

Pos.enlarge_graphene_cell([xsize,zsize])
Pos.create_file(outfile,increment='True')
