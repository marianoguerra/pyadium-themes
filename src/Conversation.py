'''an example on how to use the library'''

import os
import gtk
gtk.gdk.threads_init()
import sys
import webkit

import AdiumTheme
import AdiumThemes
import Message

class Conversation(gtk.Window):

    def __init__(self, theme, source, target, target_display, source_img,
            target_img):
        gtk.Window.__init__(self)
        self.set_title('adium themes')
        self.set_default_size(640, 480)
        self.set_border_width(4)

        self.theme = theme
        self.last_incoming = None

        vbox = gtk.VBox(homogeneous=False)
        vbox.set_spacing(4)

        self.view = webkit.WebView()
        body = theme.get_body(source, target, target_display, source_img,
                target_img)
        self.view.load_string(body,
                "text/html", "utf-8", "file://" + theme.path)
        scroll = gtk.ScrolledWindow()
        scroll.add(self.view)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)

        vbox.pack_start(scroll, True, True)

        in_text = Account(self.add_message, True, "marianoguerra@emesene.org",
                "wariano", "Mariano Guerra", "../../../../extras/user.png",
                "../../../../extras/online.png", "online", "LOL")
        vbox.pack_start(gtk.Label("incoming"), False)
        vbox.pack_start(in_text, False)

        out_text = Account(self.add_message, False, "dx@emesene.org",
                "dx", "XD", "../../../../extras/user1.png", "../../../../extras/busy.png",
                "busy", "w00t")
        vbox.pack_start(gtk.Label("outcoming"), False)
        vbox.pack_start(out_text, False)

        vbox.show_all()

        self.add(vbox)
        self.connect('destroy', lambda *args: sys.exit(0))

    def add_message(self, msg):
        '''add a message to the conversation'''

        if msg.incoming:
            if self.last_incoming is None:
                self.last_incoming = False

            msg.first = not self.last_incoming
            html = self.theme.format_incoming(msg)
            self.last_incoming = True
        else:
            if self.last_incoming is None:
                self.last_incoming = True

            msg.first = self.last_incoming
            html = self.theme.format_outgoing(msg)
            self.last_incoming = False

        if msg.first:
            function = "appendMessage('" + html + "')"
        else:
            function = "appendNextMessage('" + html + "')"

        self.view.execute_script(function)
        self.view.execute_script("scrollToBottom()")

class Account(gtk.VBox):
    '''a class that represents an account widget to chat
    '''

    def __init__(self, callback, local, account, display_name, alias,
            image_path, status_path, status, message):
        gtk.VBox.__init__(self)
        self.local = local
        self.callback = callback
        table = gtk.Table(7, 2, True)

        row = -1

        row += 1
        table.attach(gtk.Label('account'), 0, 1, row, row + 1)
        self.account = gtk.Entry()
        self.account.set_text(account)
        table.attach(self.account, 1, 2, row, row + 1)

        row += 1
        table.attach(gtk.Label('display'), 0, 1, row, row + 1)
        self.display = gtk.Entry()
        self.display.set_text(display_name)
        table.attach(self.display, 1, 2, row, row + 1)

        row += 1
        table.attach(gtk.Label('alias'), 0, 1, row, row + 1)
        self.alias = gtk.Entry()
        self.alias.set_text(alias)
        table.attach(self.alias, 1, 2, row, row + 1)

        row += 1
        table.attach(gtk.Label('image path'), 0, 1, row, row + 1)
        self.image_path = gtk.Entry()
        self.image_path.set_text(image_path)
        table.attach(self.image_path, 1, 2, row, row + 1)

        row += 1
        table.attach(gtk.Label('status path'), 0, 1, row, row + 1)
        self.status_path = gtk.Entry()
        self.status_path.set_text(status_path)
        table.attach(self.status_path, 1, 2, row, row + 1)

        row += 1
        table.attach(gtk.Label('status'), 0, 1, row, row + 1)
        self.status = gtk.Entry()
        self.status.set_text(status)
        table.attach(self.status, 1, 2, row, row + 1)

        row += 1
        table.attach(gtk.Label('message'), 0, 1, row, row + 1)
        self.message = gtk.Entry()
        self.message.set_text(message)
        table.attach(self.message, 1, 2, row, row + 1)

        button = gtk.Button(stock=gtk.STOCK_OK)
        button.connect('clicked', self._on_button_click)
        row += 1
        table.attach(button, 1, 2, row, row + 1)

        table.show_all()
        self.pack_start(table)


    def _on_button_click(self, button):
        account = self.account.get_text()
        display = self.display.get_text()
        alias = self.alias.get_text()
        image_path = self.image_path.get_text()
        status_path = self.status_path.get_text()
        status = self.status.get_text()
        msg = self.message.get_text()

        message = Message.Message(not self.local, True, account, display,
                alias, image_path, status_path, msg, status)
        self.callback(message)

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    themes_path = os.path.join(dir_path, "../test/themes")

    themes = AdiumThemes.get_instance()
    themes.add_themes_path(themes_path)

    for (index, path) in enumerate(themes.list()):
        print index, path

    option = int(raw_input("option: "))
    path = themes.list()[option]

    status, theme = themes.get(path)

    if not status:
        print theme
        sys.exit(-1)

    gtk.gdk.threads_init()
    conv = Conversation(theme, "wariano@emesene.org", "dx@emesene.org", "XD",
        "../../../../extras/user.png", "../../../../extras/user1.png")
    conv.show()

    gtk.main()
