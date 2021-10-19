#!/usr/bin/python3 -W ignore::DeprecationWarning
import ctypes
x11 = ctypes.cdll.LoadLibrary('libX11.so')
x11.XInitThreads()

import gi
import os
import yaml
import time
import base64
gi.require_version('Gtk', '3.0')
from threading import Thread
from gi.repository import Gtk

class Smother(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title ="Smother")
        Gtk.Window.set_resizable(self, False)
        self.set_border_width(10)
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.add(box)
        # get config file and resolve missing arguments
        self.configPath = os.path.join(os.environ['HOME'], ".config/smother.yaml")
        if not os.path.exists(self.configPath):
            os.system("echo \'enabled: false \nreconnecting: false \nport: 0 \nbackup:\' > ~/.config/smother.yaml")
        self.config = yaml.safe_load(open(self.configPath, "r+"))
        if len(self.config) != 4:
            os.system("rm ~/.config/smother.yaml \n echo \'enabled: false \nreconnecting: false \nport: 0 \nbackup:\' > ~/.config/smother.yaml")
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
        self.settingsbox.set_sensitive(not self.config["enabled"])
        if self.config["reconnecting"]:
            # this is a bad workaround but it works
            self.reconnectingswitch.set_state(True)
            self.config["reconnecting"] = True
            yaml.safe_dump(self.config, open(self.configPath, "r+"))
        self.port.set_sensitive(self.reconnectingswitch.get_state())
        self.applybutton.set_sensitive(self.reconnectingswitch.get_state())
        if self.config["enabled"]:
            Thread(target = self.status_check, args = ()).start()

    def on_reconnecting_changed(self, widget, state):
        self.config["reconnecting"] = not self.reconnectingswitch.get_state()
        self.port.set_sensitive(self.config["reconnecting"])
        self.applybutton.set_sensitive(self.config["reconnecting"])
        yaml.safe_dump(self.config, open(self.configPath, "r+"))

    def on_port_apply(self, widget):
        self.config["port"] = self.port.get_value()
        yaml.safe_dump(self.config, open(self.configPath, "r+"))

    def on_enable_clicked(self, widget):
        print("\33[6m" + "Enabling killswitch" + "\33[0m")
        Thread(target = self.enable, args = ()).start()

    def on_disable_clicked(self, widget):
        print("\33[6m" + "Disabling killswitch" + "\33[0m")
        Thread(target = self.disable, args = ()).start()

    def enable(self):
        # back up current rules
        self.backup_ufw()
        self.killbutton.set_sensitive(False)
        # check if a VPN reconnecting port has been specified
        if self.config["reconnecting"]:
            # Force all ports to pass through tun0 except VPN reconnecting ports
            commandstatus = os.system("pkexec bash -c \'ufw --force reset; rm /etc/ufw/*.rules.*; ufw enable; ufw default deny incoming; ufw default deny outgoing; ufw allow out on tun0 from any to any; ufw allow out " + str(int(self.config["port"])) + "/udp; ufw allow in " + str(int(self.config["port"])) + "/udp; ufw allow out 53; ufw allow in 53\' &> /dev/null")
            self.config["reconnecting"] = True
        else:
            # force all ports to pass through tun0
            commandstatus = os.system("pkexec bash -c \'ufw --force reset; rm /etc/ufw/*.rules.*; ufw enable; ufw default deny incoming; ufw default deny outgoing; ufw allow out on tun0 from any to any\' &> /dev/null")
        if not commandstatus:
            self.unkillbutton.set_sensitive(True)
            self.config["enabled"] = True
            yaml.safe_dump(self.config, open(self.configPath, "r+"))
            os.system("notify-send 'Smother' 'Killswitch enabled' -i smother")
            Thread(target = self.status_check, args = ()).start()
            self.settingsbox.set_sensitive(False)
            print("\33[92m" + "Killswitch enabled" + "\33[0m")
        elif commandstatus != 32256:
            self.killbutton.set_sensitive(True)
            os.system("notify-send 'Smother' 'Failed to enable killswitch' -u critical -i smother")
            print("\33[31m" + "Failed to enable killswitch" + "\33[0m")
        else:
            self.killbutton.set_sensitive(True)
            print("\33[33m" + "Request dismissed" + "\33[0m")

    def disable(self):
        self.unkillbutton.set_sensitive(False)
        self.recover_ufw()
        # clear killswitch UFW rules and replace with backed up rules
        commandstatus = os.system("pkexec bash -c \'ufw --force reset; rm /etc/ufw/*.rules.*; ufw enable; echo \"" + self.ufwRecovery + "\" > /etc/ufw/user.rules; echo \"" + self.ufwRecovery6 + "\" > /etc/ufw/user6.rules; ufw default allow outgoing\' &> /dev/null")
        if not commandstatus:
            self.killbutton.set_sensitive(True)
            self.unkillbutton.set_sensitive(False)
            self.config["enabled"] = False
            yaml.safe_dump(self.config, open(self.configPath, "r+"))
            os.system("notify-send 'Smother' 'Killswitch disabled' -i smother")
            self.settingsbox.set_sensitive(True)
            print("\33[92m" + "Killswitch disabled" + "\33[0m")
        elif commandstatus != 32256:
            self.unkillbutton.set_sensitive(True)
            os.system("notify-send 'Smother' 'Failed to disable killswitch' -u critical -i smother")
            print("\33[31m" + "Failed to disable killswitch" + "\33[0m")
        else:
            self.unkillbutton.set_sensitive(True)
            print("\33[33m" + "Request dismissed" + "\33[0m")

    def backup_ufw(self):
        # store current UFW rules as base64
        ufwBackup = base64.b64encode(open("/etc/ufw/user.rules", "r").read().replace("\"", "\\\"").encode("utf-8"))
        ufwBackup6 = base64.b64encode(open("/etc/ufw/user6.rules", "r").read().replace("\"", "\\\"").encode("utf-8"))
        self.config["backup"] = [ufwBackup, ufwBackup6]

    def recover_ufw(self):
        # recover UFW rules
        self.ufwRecovery = base64.b64decode(self.config["backup"][0]).decode("utf-8")
        self.ufwRecovery6 = base64.b64decode(self.config["backup"][1]).decode("utf-8")

    def status_check(self):
        vpnstatus = True
        time.sleep(2)
        # check if VPN is running
        while self.config["enabled"] and win.get_window():
            if not os.system("nmcli device status | grep \"tun0\" &> /dev/null"):
                vpnstatus = True
            else:
                if vpnstatus:
                    os.system("notify-send 'Smother' 'VPN is down' -u critical -i smother")
                    print("\33[33m" + "VPN is down" + "\33[0m")
                vpnstatus = False
            time.sleep(1)

win = Smother()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

