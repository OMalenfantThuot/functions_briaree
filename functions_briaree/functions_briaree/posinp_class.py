from .io_bigdft import read_ascii
import os

class Posinp:
    """
    Classe relative aux fichiers positions
    """
    def __init__(self, filetype='ascii'):
        """
        :param filetype: ascii ou xyz
        """
        self.nat = 0
        self.atompos = []
        self.elements = []
        self.spins = []
        self.cell_dims = []
        self.geocode = ''
        self.coord = 'absolute'
        self.filetype = filetype
        self.units = ''

    def def_from_file(self,infile):
        """
        Définie self à partir d'un fichier déjà existant
        :param infile: nom du fichier à lire
        """
        if self.filetype == 'ascii':
            self.atompos, self.elements, self.spins,self.units, \
                self.geocode, self.coord,self.cell_dims = read_ascii(infile)
            self.nat = len(self.elements)

        elif self.filetype == 'xyz':
            raise Exception('xyz format not yet supported')

        else:
            raise Exception('Format not recognized')

    def translate(self, delx, delz):
        pass

    def add_atom(self,new_coord,new_element,new_spin=0):
        """
        Ajoute un atome au fichier position
        :param new_coord: coordonnées du nouvel atome
        :param new_element: élément du nouvel atome
        :param new_spin: spin du nouvel atome (optionel)
        """
        self.atompos.append(new_coord)
        self.elements.append(new_element)
        self.spins.append(new_spin)
        self.nat += 1

    def remove_atom(self, rank):
        """
        Enlève un atome au fichier position
        :param rank: rang de l'atome dans le fichier
        """
        del self.atompos[rank]
        del self.elements[rank]
        del self.spins[rank]
        self.nat -= 1

    def create_file(self,outfile,increment='True'):
        """
        Crée un fichier position avec les valeurs dans self
        :param outfile: nom du fichier à créer sans l'extension
        :param increment: détermine si le nom du fichier doit être incrémenté
        """
        if increment and os.path.exists(outfile):
            i = 2
            testname = outfile + str(i) + '.' + self.filetype
            while os.path.exists(testname):
                i += 1
                testname = outfile + str(i) + '.' + self.filetype
            outfile = testname
        else:
            outfile = outfile + '.' + self.filetype

        with open(outfile,'w') as f:
            f.write('# BigDFT position file\n')
            f.write(' ' + ' '.join(self.cell_dims[0]) + '\n')
            f.write(' ' + ' '.join(self.cell_dims[1]) + '\n')
            f.write('#keyword: ' + self.units + '\n')
            f.write('#keyword: ' + self.geocode + '\n')
            if self.coord == 'reduced':
                f.write('#keyword: ' + self.coord + '\n')
            for line, data in enumerate(self.atompos):
                for dim in data:
                    f.write('  {:19.17E}'.format(dim))
                f.write(' ' + self.elements[line])
                if self.spins[line] != 0:
                    f.write(' {IGSpin: ' + str(self.spins[line]) + '}')
                f.write('\n')

    def enlarge(self, initsize, finalsize):
        pass