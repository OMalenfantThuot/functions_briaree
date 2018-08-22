import os
import sys 
import readline
import glob

class TabCompleter(object):
    """ 
    A tab completer
    Adapted from https://gist.github.com/iamatypeofwalrus/5637895
    """

    def pathCompleter(self,text,state):
        """ 
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line   = readline.get_line_buffer().split()
        return [x for x in glob.glob(text+'*')][state]

#A ajouter dans un script pour l'utilisation:
#t = fbr.TabCompleter()
#readline.set_completer_delims('\t')
#readline.parse_and_bind("tab: complete") 
#readline.set_completer(t.pathCompleter)
