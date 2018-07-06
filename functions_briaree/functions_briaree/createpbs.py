#Fonction pour créer des fichiers de soumission pbs en série
def createpbs(jobname='jobname',walltime=1, nodes=4, executable='bigdft'):

#-----------------------------------------------------------------------#
#jobname:   Nom de la job
#walltime:  Temps demandé pour le calcul (en heures)
#nodes:     Nombre de noeuds demandés pour le calcul
#executable:    executable demandé(bigdft ou neb)
#-----------------------------------------------------------------------#

    #Détermination de l'éxécutable
    if executable.casefold() in ['b','bigdft']:
        executable = 'bigdft'
    elif executable.casefold() in ['n','neb']:
        executable = 'neb'

    #Conversion en string du walltime
    hours = int(walltime)
    minutes = int((walltime - hours) * 60)
    seconds = int((walltime - hours - minutes/60) * 3600)
    walltime = '{:02d}'.format(hours) + ':' + '{:02d}'.format(minutes) + ':' + '{:02d}'.format(seconds)

    #Conversion en string des nodes
    nodes = str(int(nodes))

    #Écriture du fichier
    f = open('pbs','w')
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
    
    if executable == 'bigdft':
        f.write("mpirun /RQexec/olimt/bigDFT_install/github_dir/master/build/install/bin/bigdft")
    elif executable == 'neb':
        f.write("mpirun /RQexec/olimt/bigDFT_install/github_dir/master/build/install/bin/NEB<input.yaml> output.yaml")
