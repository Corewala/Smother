import gi
import os
import yaml
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Smother(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title ="Smother")
        Gtk.Window.set_resizable(self, False);
        self.set_border_width(10)

        # get config file
        self.configPath = os.path.join(os.environ['HOME'], ".config/smother.yaml")
        if not os.path.exists(self.configPath):
            os.system("echo \'enabled: false\' > ~/.config/smother.yaml")
        self.config = yaml.safe_load(open(self.configPath, "r+"))

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.add(box)

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
        box.pack_start(stack_switcher, True, True, 0)
        box.pack_start(stack, True, True, 0)

        if self.config["enabled"]:
            self.killbutton.set_sensitive(False)
            self.unkillbutton.set_sensitive(True)
        else:
            self.killbutton.set_sensitive(True)
            self.unkillbutton.set_sensitive(False)

    def on_enable_clicked(self, widget):
        os.system("gksu bash -c \'/usr/bin/ufw default deny incoming \n /usr/bin/ufw default deny outgoing \n sudo ufw allow out on tun0 from any to any\'")
        self.killbutton.set_sensitive(False)
        self.unkillbutton.set_sensitive(True)
        self.config["enabled"] = True
        yaml.safe_dump(self.config, open(self.configPath, "r+"))

    def on_disable_clicked(self, widget):
        os.system("gksu bash -c \'/usr/bin/ufw --force reset \n /usr/bin/ufw enable \n /usr/bin/rm /etc/ufw/*.rules.* \n /usr/bin/ufw default deny incoming \n /usr/bin/ufw default allow outgoing\'")
        self.killbutton.set_sensitive(True)
        self.unkillbutton.set_sensitive(False)
        self.config["enabled"] = False
        yaml.safe_dump(self.config, open(self.configPath, "r+"))

win = Smother()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()