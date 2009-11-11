'''a module that contains a class that describes a adium theme'''

class Theme(object):
    '''a class that contains information of a adium theme
    '''

    def __init__(self, path):
        '''constructor

        get information from the theme located in path
        '''
        self.path = None
        self.load_information(path)

    def load_information(self, path):
        '''load the information of the theme on path
        '''
        self.path = path
        # TODO: finish
