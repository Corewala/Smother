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
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.add(box)
        # get config file and resolve missing arguments
        self.configPath = os.path.join(os.environ['HOME'], ".config/smother.yaml")
        if not os.path.exists(self.configPath):
            os.system("echo \'enabled: false \nreconnecting: false \nport: 0\' > ~/.config/smother.yaml")
        self.config = yaml.safe_load(open(self.configPath, "r+"))
        if len(self.config) != 3:
            os.system("rm ~/.config/smother.yaml \n echo \'enabled: false \nport: 0\' > ~/.config/smother.yaml")
            self.config = yaml.safe_load(open(self.configPath, "r+"))
        # create stack switcher
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        # create buttons
        self.killbutton = Gtk.Button(label = "Enable Killswitch")
        self.killbutton.connect("clicked", self.on_enable_clicked)
        stack.add_titled(self.killbutton, "kill", "Enable")
        self.unkillbutton = Gtk.Button(label = "Disable Killswitch")
        self.unkillbutton.connect("clicked", self.on_disable_clicked)
        stack.add_titled(self.unkillbutton, "unkill", "Disable")
        # create settings area
        settings = Gtk.Expander(label = "Settings")
        self.switchtable = Gtk.Table(1, 2, False)
        self.switchlabel = Gtk.Label(label = "Allow reconnecting")
        self.reconnectingswitch = Gtk.Switch()
        self.reconnectingswitch.connect("state_set", self.on_reconnecting_changed)
        self.switchtable.attach(self.switchlabel, 0, 1, 0, 1)
        self.switchtable.attach(self.reconnectingswitch, 1, 2, 0, 1)
        self.port = Gtk.SpinButton()
        self.port.set_range(0, 65535)
        self.port.set_increments(1, 2)
        self.applybutton = Gtk.Button(label = "Apply")
        self.applybutton.connect("clicked", self.on_port_apply)
        self.settingsbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 10)
        self.settingsbox.add(self.switchtable)
        self.settingsbox.add(self.port)
        self.settingsbox.add(self.applybutton)
        settings.add(self.settingsbox)
        # create stack switcher
        switcher = Gtk.StackSwitcher()
        switcher.set_stack(stack)
        box.pack_start(switcher, True, True, 0)
        box.pack_start(stack, True, True, 0)
        box.pack_start(settings, True, True, 0)
        # restore settings from file
        self.killbutton.set_sensitive(not self.config["enabled"])
        self.unkillbutton.set_sensitive(self.config["enabled"])
        self.port.set_value(self.config["port"])
        self.reconnectingswitch.set_state(self.config["reconnecting"])
        self.port.set_sensitive(self.reconnectingswitch.get_state())
        self.applybutton.set_sensitive(self.reconnectingswitch.get_state())

    def on_reconnecting_changed(self, widget, state):
        self.config["reconnecting"] = not self.reconnectingswitch.get_state()
        self.port.set_sensitive(self.config["reconnecting"])
        self.applybutton.set_sensitive(self.config["reconnecting"])
        yaml.safe_dump(self.config, open(self.configPath, "r+"))

    def on_port_apply(self, widget):
        self.config["port"] = self.port.get_value()
        yaml.safe_dump(self.config, open(self.configPath, "r+"))

    def on_enable_clicked(self, widget):
        if self.config["reconnecting"] and self.config["port"]:
            command = "pkexec bash -c \'ufw default deny incoming \n ufw default deny outgoing \n ufw allow out on tun0 from any to any \n ufw allow out " + str(int(self.config["port"])) + "/udp \n ufw allow in " + str(int(self.config["port"])) + "/udp \n ufw allow out 53 \n ufw allow in 53\'"
        else:
            command = "pkexec bash -c \'ufw default deny incoming \n ufw default deny outgoing \n ufw allow out on tun0 from any to any\'"

        if not os.system(command):
            self.killbutton.set_sensitive(False)
            self.unkillbutton.set_sensitive(True)
            self.config["enabled"] = True
            yaml.safe_dump(self.config, open(self.configPath, "r+"))

    def on_disable_clicked(self, widget):
        if not os.system("pkexec bash -c \'ufw --force reset \n ufw enable \n rm /etc/ufw/*.rules.* \n ufw default deny incoming \n ufw default allow outgoing\'"):
            self.killbutton.set_sensitive(True)
            self.unkillbutton.set_sensitive(False)
            self.config["enabled"] = False
            yaml.safe_dump(self.config, open(self.configPath, "r+"))

win = Smother()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()