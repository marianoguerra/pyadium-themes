'''a module that contains a class that describes a adium theme'''
import re
import os
import time

class Theme(object):
    '''a class that contains information of a adium theme
    '''

    def __init__(self, path, timefmt):
        '''constructor

        get information from the theme located in path
        '''
        self.path = None
        self.timefmt = timefmt
        self.load_information(path)

    def load_information(self, path):
        '''load the information of the theme on path
        '''
        self.path = path
        self.resources_path = os.path.join(path, 'Contents', 'Resources')
        self.incoming_path = os.path.join(self.resources_path, 'Incoming')
        self.outgoing_path = os.path.join(self.resources_path, 'Outgoing')

        self.content = self.read_file(self.resources_path, 'Content.html')

        self.incoming = self.read_file(self.incoming_path, 'Content.html')
        self.incoming_next = self.read_file(self.incoming_path, 'NextContent.html')

        self.outgoing = self.read_file(self.outgoing_path, 'Content.html')
        self.outgoing_next = self.read_file(self.outgoing_path, 'NextContent.html')

    def format_incoming(self, msg):
        '''return a string containing the template for the incoming message
        with the vars replaced
        '''
        # fallback madness, some repetition but well..
        if not msg.first:
            if self.incoming_next is None:
                if self.incoming is None:
                    template = self.content
                else:
                    template = self.incoming
            else:
                template = self.incoming_next
        elif self.incoming is None:
            template = self.content
        else:
            template = self.incoming

        return self.replace(template, msg)

    def format_outgoing(self, msg):
        '''return a string containing the template for the outgoing message
        with the vars replaced
        '''
        # fallback madness, some repetition but well..
        if not msg.first:
            if self.outgoing_next is None:
                if self.outgoing is None:
                    if self.incoming is None:
                        template = self.content
                    else:
                        template = self.incoming
                else:
                    template = self.outgoing
            else:
                template = self.outgoing_next
        elif self.outgoing is None:
            if self.incoming is None:
                template = self.content
            else:
                template = self.incoming
        else:
            template = self.outgoing

        return self.replace(template, msg)

    def replace(self, template, msg):
        template = template.replace('%sender%', msg.alias)
        template = template.replace('%senderScreenName%', msg.sender)
        template = template.replace('%senderDisplayName%', msg.display_name)
        template = template.replace('%userIconPath%', msg.image_path)
        template = template.replace('%senderStatusIcon%', msg.status_path)
        template = template.replace('%messageDirection%', msg.direction)
        template = template.replace('%message%', msg.message)
        template = template.replace('%time%', time.strftime(self.timefmt))
        template = template.replace('%shortTime%', time.strftime("%H:%M"))
        template = template.replace('%service%', msg.service)
        template = template.replace('%messageClasses%', msg.classes)
        template = template.replace('%status%', msg.status)

        return template.replace('\n', '')

    def replace_header_or_footer(self, template, source, target,
            target_display, source_img, target_img):
        template = template.replace('%chatName%', target)
        template = template.replace('%sourceName%', source)
        template = template.replace('%destinationName%', target)
        template = template.replace('%destinationDisplayName%', target_display)
        template = template.replace('%incomingIconPath%', target_img)
        template = template.replace('%outgoingIconPath%', source_img)
        template = template.replace('%timeOpened%', time.strftime("%H:%M"))
        # TODO: use the format inside the {}
        template = re.sub("%timeOpened{.*?}%", time.strftime("%H:%M"), template)

        return template

    def get_body(self, source, target, target_display, source_img, target_img):
        '''return the template to put as html content
        '''
        template = self.read_file("template.html")
        css_path = "file://" + os.path.join(self.resources_path, "main.css")
        template = template.replace("%@", "file://" + self.path, 1)
        template = template.replace("%@", css_path, 1)
        header = self.read_file(self.resources_path, 'Header.html') or ""
        if header:
            header = self.replace_header_or_footer(header, source, target,
                    target_display, source_img, target_img)
        template = template.replace("%@", header, 1)
        footer = self.read_file(self.resources_path, 'Footer.html') or ""
        if footer:
            footer = self.replace_header_or_footer(header, source, target,
                    target_display, source_img, target_img)
        template = template.replace("%@", footer, 1)

        return template

    def read_file(self, *args):
        '''read file if exists and is readable, return None otherwise
        '''
        path = os.path.join(*args)
        if os.access(path, os.R_OK):
            return file(path).read()

        return None

