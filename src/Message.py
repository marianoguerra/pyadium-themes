'''a module that contains a class that represents a message
'''

class Message(object):
    '''a class that represents a message to be used by the adium themes
    '''

    def __init__(self, incoming, first, sender, display_name, alias, image_path,
            status_path, message, status, service='MSN', classes='',
            direction='ltr'):
        '''constructor, see http://trac.adium.im/wiki/CreatingMessageStyles for more information of the values
        '''
        self.incoming       = incoming
        self.first          = first
        self.sender         = sender
        self.display_name   = display_name
        self.alias          = alias
        self.image_path     = image_path
        self.status_path    = status_path
        self.message        = message
        self.status         = status
        self.service        = service
        self.classes        = classes
        self.direction      = direction
