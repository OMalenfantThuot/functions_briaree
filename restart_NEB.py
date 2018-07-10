#!/usr/bin/env python3

# Script pour relancer les calculs NEB
# Prépare les fichiers dans ../jobname_restart/
# Peut s'appeler comme un executable

import functions_briaree as fbr
import os
from pathlib import Path
import shutil
import re

old_files = os.listdir(os.getcwd())

jobname = str(Path().resolve()).split('/')[-1]
new_path = fbr.createFolder('../'+jobname+'_restart',increment=True)

for file in old_files:
    if file in ['input.yaml','default.yaml','pbs'] or file.startswith('psppar'):
        shutil.copy(file,new_path+'/'+file)

    elif file.startswith('data-neb'):
        image_num = int(re.findall('\d+',file)[0])
        num = []
        data_files = os.listdir(file)
        for name in data_files:
            if name.startswith('posout'):
                num.append(int(re.findall('\d+',name)[0]))
        shutil.copy(file+'/posout_{:04d}.ascii'.format(max(num)),new_path+'/posinp{:d}.ascii'.format(image_num))
