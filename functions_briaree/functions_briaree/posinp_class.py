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
                self.geocode, self.coord,self.cell_dims = read_ascii(infile)
            self.nat = len(self.elements)

        elif self.filetype == 'xyz':
            raise Exception('xyz format not yet supported')

        else:
            raise Exception('format not recognized')

#    def translate(self, delx, delz):

    def add_atom(self,new_coord,new_element,new_spin=0):
        #coord : list with the new coordinates

        self.atompos.append(new_coord)
        self.elements.append(new_element)
        self.spins.append(new_spin)
        self.nat += 1
        

    def remove_atom(self,coord):
        #coord: rank of the atom to be removed

        del self.atompos[coord]
        del self.elements[coord]
        del self.spins[coord]
        self.nat -= 1

#    def create(self):

#    def enlarge(self, initsize, finalsize):
