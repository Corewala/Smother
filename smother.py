import gi
import os
from gi.repository import Gtk
gi.require_version('Gtk', '3.0')

class Smother(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title ="Smother")
        Gtk.Window.set_resizable(self, False);
        self.set_border_width(10)

        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        self.killbutton = Gtk.Button(label ="Enable Killswitch")
        self.killbutton.connect("clicked", self.on_enable_clicked)
        stack.add_titled(self.killbutton, "kill", "Enable")

        self.unkillbutton = Gtk.Button(label ="Disable Killswitch")
        self.unkillbutton.connect("clicked", self.on_disable_clicked)
        stack.add_titled(self.unkillbutton, "unkill", "Disable")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

    def on_enable_clicked(self, widget):
        os.system("gksu bash -c \'/usr/bin/ufw default deny incoming \n /usr/bin/ufw default deny outgoing \n sudo ufw allow out on tun0 from any to any\'")

    def on_disable_clicked(self, widget):
        os.system("gksu bash -c \'/usr/bin/ufw --force reset \n /usr/bin/ufw enable \n /usr/bin/rm /etc/ufw/*.rules.* \n /usr/bin/ufw default deny incoming \n /usr/bin/ufw default allow outgoing\'")

win = Smother()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()