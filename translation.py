#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functions_briaree as fbr

"""
Script pour translater les fichiers positions .ascii
S'appelle comme un éxécutable

"""
infile = str(input('Entrer le nom du fichier à translater:\n'))

Pos = fbr.Posinp()
Pos.def_from_file(infile)
outfile = 'out_'+infile.strip('.' + Pos.filetype)

delx = float(input('Translation en x (' + Pos.units + '):\n'))
delz = float(input('Translation en z (' + Pos.units + '):\n'))

Pos.translate(delx,0,delz)
Pos.create_file(outfile,increment='True')
