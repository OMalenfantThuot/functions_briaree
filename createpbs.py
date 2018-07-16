#!/usr/bin/env python3

#----------------------------------------------------------#
#Version executable de la fonctione pbs.create()
#----------------------------------------------------------#


#Informations entrees par l'utilisateur
jobname  =   input('Enter job name:\n')
walltime =   input("Enter job length (in hours):\n")+":00:00"
nodes    =   input("Enter number of required nodes:\n")
while 1:
    type = input("Enter the executable (bigdft or NEB):\n")
    if type.casefold() in ['b','bigdft']:
        type = 'bigdft'
        break
    elif type.casefold() in ['n','neb']:
        type = 'neb'
        break
    else:
        print('This executable is not recognized.')

#Ecriture du fichier
with open('pbs','w') as f:
    f.write("#!/bin/bash\n")
    f.write("#PBS -S /bin/bash\n\n")
    
    f.write("#PBS -N " + jobname + "\n")
    f.write("#PBS -l walltime=" + walltime + "\n")
    f.write("#PBS -l nodes=" + nodes + ":ppn=12\n\n")
    
    f.write("cd $PBS_O_WORKDIR\n")
    f.write("echo 'Current working directory is `pwd`'\n")
    f.write("echo 'Running on `hostname`'\n")
    f.write("echo 'Starting run at: `date`'\n\n")
    
    f.write("module load MPI/Gnu/gcc4.9.2/openmpi/1.10.2\n")
    f.write("export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/RQexec/olimt/bigDFT_install/github_dir/master/build/install/lib\n\n")
    
    if type == 'bigdft':
        f.write("mpirun /RQexec/olimt/bigDFT_install/github_dir/master/build/install/bin/bigdft")
    elif type == 'neb':
        f.write("mpirun /RQexec/olimt/bigDFT_install/github_dir/master/build/install/bin/NEB<input.yaml> output.yaml")
