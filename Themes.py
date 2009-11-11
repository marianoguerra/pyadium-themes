'''a module to handle themes'''
import os

import Theme

DIRECTORY, FILE = range(2)

REQUIRED_FILES = [
        {'name': 'Contents', 'type': DIRECTORY, 'childs': [
            {'name': 'Info.plist', 'type': FILE},
            {'name': 'Resources', 'type': DIRECTORY, 'childs': [
                {'name': 'main.css', 'type': FILE},
                {'name': 'Status.html', 'type': FILE},
                {'name': 'Incoming', 'type': DIRECTORY, 'childs': [
                    {'name': 'Content.html', 'type': FILE},
                ]}
            ]}
        ]}]

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

    def validate(self, theme_path):
        '''validate a Theme directory structure
        '''

        if not os.path.isdir(theme_path):
            return False, "%s is not a directoy" % (theme_path,)

        return self.validate_structure(theme_path, REQUIRED_FILES)

    def validate_structure(self, base_path, structure):
        '''validate the required files and directories from base_path
        '''

        for item in structure:
            name = os.path.join(base_path, item['name'])

            if item['type'] == FILE:
                if not os.path.isfile(name):
                    return False, "%s is not a file" % (name, )
                if not os.access(name, os.R_OK):
                    return False, "%s is not readable" % (name, )
            elif item['type'] == DIRECTORY:
                if not os.path.isdir(name):
                    return False, "%s is not a directory" % (name, )

                return self.validate_structure(name, item['childs'])

        return True, "ok"

if __name__ == '__main__':
    themes = get_instance()
    print themes.validate("themes/renkoo.AdiumMessageStyle")
    print themes.validate("themes/renkooNaked.AdiumMessageStyle")
    print themes.validate("themes/Modern Bubbling.AdiumMessageStyle")
    print themes.validate("invalid themes/renkoo.AdiumMessageStyle")
    print themes.validate("invalid themes/renkooNaked.AdiumMessageStyle")
    print themes.validate("invalid themes/Modern Bubbling.AdiumMessageStyle")
    print themes.validate("invalid themes/nonexistent.AdiumMessageStyle")