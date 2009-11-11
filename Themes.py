'''a module to handle themes'''
import Theme

__instance = None

def get_instance():
    '''singleton for Themes class
    '''
    global __instance

    if __instance is None:
        __instance = Themes()

    return __instance


class Themes(object):
    '''a class to handle adium themes
    '''

    def __init__(self):
        '''constructor'''

        # the paths to look for themes
        self.paths = []

   def add_themes_path(self, path):
       '''add a path to look for themes

       returns True if the path was added, False otherwise (the path doesn't
       exists or it isn't a directory)
       '''

       if path not in self.paths and os.path.isdir(path):
           self.paths.append(path)
           return True

       return False

   def list(self):
       '''return a list of all the available themes
       '''
       pass

   def get(self, theme):
       '''return a Theme object instance
       '''
       pass

   def validate(self, theme):
       '''validate a Theme object
       '''
       pass

