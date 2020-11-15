import gi
import os
from gi.repository import gtk


class Smother(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, title ="Smother")
        gtk.Window.set_resizable(self, False);
        self.set_border_width(10)

        vbox = gtk.Box(orientation = gtk.Orientation.VERTICAL, spacing = 20)
        self.add(vbox)

        stack = gtk.Stack()
        stack.set_transition_type(gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        self.killbutton = gtk.Button(label ="Enable Killswitch")
        self.killbutton.connect("clicked", self.on_enable_clicked)
        stack.add_titled(self.killbutton, "kill", "Enable")

        self.unkillbutton = gtk.Button(label ="Disable Killswitch")
        self.unkillbutton.connect("clicked", self.on_disable_clicked)
        stack.add_titled(self.unkillbutton, "unkill", "Disable")

        stack_switcher = gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

    def on_enable_clicked(self, widget):
        os.system("gksu bash -c \'/usr/bin/ufw default deny incoming \n /usr/bin/ufw default deny outgoing \n sudo ufw allow out on tun0 from any to any\'")

    def on_disable_clicked(self, widget):
        os.system("gksu bash -c \'/usr/bin/ufw --force reset \n /usr/bin/ufw enable \n /usr/bin/rm /etc/ufw/*.rules.* \n /usr/bin/ufw default deny incoming \n /usr/bin/ufw default allow outgoing\'")

win = Smother()
win.connect("destroy", gtk.main_quit)
win.show_all()
gtk.main()