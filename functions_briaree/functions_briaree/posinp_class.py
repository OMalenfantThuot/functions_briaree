#-------------------------------------------------------#
#Classe pour les fichiers de position .ascii
#-------------------------------------------------------#

from .io_bigdft import read_ascii

class posinp:

    def __init__(self, filetype='ascii'):
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

        if self.filetype == 'ascii':
            self.atompos, self.elements, self.spins,self.units, \
                self.geocode, self.coord = read_ascii(infile)
            self.nat = len(self.elements)

        elif self.filetype == 'xyz':
            raise Exception('xyz format not yet supported')

        else:
            raise Exception('format not recognized')
