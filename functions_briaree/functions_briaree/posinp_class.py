from .io_bigdft import read_ascii
import os
import numpy as np

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
            raise NameError('Format not recognized')

        if self.geocode=='surface':
            self.check_periodicity()

    def check_periodicity(self):
        if self.geocode == 'surface':
            for atom in self.atompos:
                if atom[0] >= self.cell_dims[0]:
                    atom[0] = atom[0]%self.cell_dims[0]
                elif atom[0] < 0:
                    atom[0] = self.cell_dims[0] + atom[0]
                if atom[2] >= self.cell_dims[5]:
                    atom[2] = atom[2]%self.cell_dims[5]
                elif atom[2] < 0:
                    atom[2] = self.cell_dims[5] + atom[2]
        elif self.geocode == 'periodic' or self.geocode == 'freeBC':
            raise Exception('Geocode not yet implemented.')
        else:
            raise NameError('Geocode not recognized.')
                

    def translate(self, del_x, del_y, del_z):
        """
        Translation des positions atomiques
        :param del_x: translation en x
        :param del_y: translation en y
        :param del_z: translation en z
        """
        for atom in self.atompos:
            atom[0] += del_x
            atom[1] += del_y
            atom[2] += del_z
        self.check_periodicity()

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
        Enleve un atome au fichier position
        :param rank: rang de l'atome dans le fichier
        """
        del self.atompos[rank]
        del self.elements[rank]
        del self.spins[rank]
        self.nat -= 1

    def create_file(self,outfile,increment='False'):
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
            for i in range(3):
                f.write('{:> 19.17E}'.format(self.cell_dims[i]))
            f.write('\n')
            for i in range(3,6):
                f.write('{:> 19.17E}'.format(self.cell_dims[i]))
            f.write('\n')
            f.write('#keyword: ' + self.units + '\n')
            f.write('#keyword: ' + self.geocode + '\n')
            if self.coord == 'reduced':
                f.write('#keyword: ' + self.coord + '\n')
            for line, data in enumerate(self.atompos):
                for dim in data:
                    f.write(' {:> 20.17E}'.format(dim))
                f.write(' ' + self.elements[line])
                if self.spins[line] != 0:
                    f.write(' {IGSpin: ' + str(self.spins[line]) + '}')
                f.write('\n')

    def generate_graphene(self, xsize, zsize, units = None):
        """
        Génère les variables relatives à une cellule de graphène parfait
        :param xsize: nombre de cellules primitives dans la direction x
        :param zsize: nombre de cellules primitives dans la direction z
        :param units: unités (optionel si déjà définis)
        """
        self.geocode = 'surface'
        self.cell_dims = []
        self.elements = []
        self.spins = []
        if units:
            self.units = units
        elif self.units:
            pass
        else:
            raise NameError('Units are not defined.')
        self.generate_graphene_cell_dims(xsize,zsize)
        self.atompos = self.generate_graphene_positions(xsize,zsize)
        self.elements = ['C']*self.nat
        self.spins = [0]*self.nat

    def generate_graphene_cell_dims(self,xsize,zsize):
        if self.units in ['atomicd0','atomic','bohr','bohrd0']:
            basex = 4.6627
            basez = 8.0762
        elif self.units in ['angstroem', 'angstroemd0']:
            basex = 2.4673
            basez = 4.2737
        else:
            raise NameError('Units not recognized.')
        self.cell_dims = [xsize*basex, 0, 40, 0, 0, zsize*basez]

    def generate_graphene_positions(self,xsize,zsize):
        """
        génère les positions pour le graphène parfait
        :param xsize: nombre de cellules primitives dans la direction x
        :param zsize: nombre de cellules primitives dans la direction z
        """
        self.nat = 4*xsize*zsize
        x_reduced_pos = []
        z_reduced_pos = []
        for zi in range(zsize):
            for xi in range(xsize):
                x_reduced_pos.append( float(xi) / xsize)
                z_reduced_pos.append( float(zi) / zsize)
            for xi in range(xsize):
                x_reduced_pos.append( float(xi)/xsize)
                z_reduced_pos.append( (float(zi) + (1./3)) / zsize)
            for xi in range(xsize):
                x_reduced_pos.append( (float(xi) + (1./2)) / xsize)
                z_reduced_pos.append( (float(zi) + (1./2)) / zsize)
            for xi in range(xsize):
                x_reduced_pos.append( (float(xi) + (1./2)) / xsize)
                z_reduced_pos.append( (float(zi) + (5./6)) / zsize)
        x_pos = np.array(x_reduced_pos) * self.cell_dims[0]
        z_pos = np.array(z_reduced_pos) * self.cell_dims[5]
        atompos = []
        for at in range(self.nat):
            atompos.append([x_pos[at],20.,z_pos[at]])
        return atompos

    def enlarge_graphene_cell(self, finalsize):
        """
        méthode pour agrandir les cellules de graphène à partir d'une cellule plus petite
        :param finalsize: liste, taille en unités de cellules primitives [x,z]
        """
        if not (isinstance(finalsize[0],int) and isinstance(finalsize[1],int)):
           raise TypeError('Cell sizes should be integers (in primitive cell units).')
        if self.coord == 'reduced':
            raise ValueError('Reduced coordinates are not implemented.')#
        initsize = self.determine_graphene_size()
        if not (finalsize[0] >= initsize[0] and finalsize[1] >= initsize[1]):
            raise ValueError('Final size must be larger than initial size.')

        deltax_down = int( np.ceil ( (finalsize[0] - initsize[0] ) / 2))
        deltax_up   = int( np.floor( (finalsize[0] - initsize[0] ) / 2))
        deltaz_left = int( np.ceil ( (finalsize[1] - initsize[1] ) / 2))
        deltaz_right= int( np.floor( (finalsize[1] - initsize[1] ) / 2))

        self.translate(0.3,0,0.3)
        self.generate_graphene_cell_dims(finalsize[0], finalsize[1])
        self.translate(-self.atompos[0][0] + (deltax_down/finalsize[0]) * self.cell_dims[0],
                       0, -self.atompos[0][2] + (deltaz_left/finalsize[1]) * self.cell_dims[5])
        new_positions = self.generate_graphene_positions(finalsize[0],finalsize[1])
        
        for i,position in enumerate(new_positions):
            if (position[0] < deltax_down / finalsize[0] * self.cell_dims[0] or
                position[0] >= (finalsize[0] - deltax_up) / finalsize[0] * self.cell_dims[0] or
                position[2] < deltaz_left / finalsize[1] * self.cell_dims[5] or
                position[2] >= (finalsize[1] - deltaz_right) / finalsize[1] * self.cell_dims[5]):
                self.atompos.append(position)
                self.elements.append('C')
                self.spins.append(0)
            else:
                pass
        self.nat = len(self.atompos)

    def determine_graphene_size(self):
        if self.units in ['atomicd0','atomic','bohr','bohrd0']:
            x_size = int(round(self.cell_dims[0]/4.6627))
            z_size = int(round(self.cell_dims[5]/8.0762))
        elif self.units in ['angstroem','angstroemd0']:
            x_size = int(round(self.cell_dims[0]/2.4673))
            z_size = int(round(self.cell_dims[5]/8.0762))
        else:
            raise NameError('Units not recognized.')
        return [x_size,z_size]
