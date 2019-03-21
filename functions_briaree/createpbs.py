# Fonction pour créer des fichiers de soumission pbs en série
def createpbs(jobname="jobname", walltime=1, nodes=4, executable="bigdft"):
    """

    :param jobname: nom de la job dans le système de soumission
    :param walltime: temps de calcul demandé en heures
    :param nodes: nombre de noeuds de calcul demandé
    :param executable: bigdft ou neb
    """
    # Détermination de l'éxécutable
    if executable.casefold() in ["b", "bigdft"]:
        executable = "bigdft"
    elif executable.casefold() in ["n", "neb"]:
        executable = "neb"

    # Conversion en string du walltime
    hours = int(walltime)
    minutes = int((walltime - hours) * 60)
    seconds = int((walltime - hours - minutes / 60) * 3600)
    walltime = (
        "{:02d}".format(hours)
        + ":"
        + "{:02d}".format(minutes)
        + ":"
        + "{:02d}".format(seconds)
    )

    # Conversion en string des nodes
    nodes = str(int(nodes))

    # Écriture du fichier
    with open("pbs", "w") as f:

        text = (
            "#!/bin/bash\n"
            "#PBS -S /bin/bash\n\n"
            "#PBS -N " + jobname + "\n"
            "#PBS -l walltime=" + walltime + "\n"
            "#PBS -l nodes=" + nodes + ":ppn=12\n\n"
            "cd $PBS_O_WORKDIR\n"
            "echo 'Current working directory is `pwd`'\n"
            "echo 'Running on `hostname`'\n"
            "echo 'Starting run at: `date`'\n\n"
            "module load MPI/Gnu/gcc4.9.2/openmpi/1.10.2\n"
            "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/RQexec/olimt/bigDFT_install/github_dir/master/build/install/lib\n\n"
        )

        f.write(text)

        if executable == "bigdft":
            f.write(
                "mpiexec /RQexec/olimt/bigDFT_install/github_dir/master/build/install/bin/bigdft"
            )
        elif executable == "neb":
            f.write(
                "mpiexec /RQexec/olimt/bigDFT_install/github_dir/master/build/install/bin/NEB<input.yaml> output.yaml"
            )
