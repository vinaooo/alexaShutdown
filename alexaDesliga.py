import os
import subprocess
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

def on_destroy(window):
    subprocess.run(["shutdown", "-c"])                                  # Cancel shutdown on close window

class CentralizedTextApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.example.centralized_text_app")

        subprocess.run(["shutdown", "+2"])                              # Shutdown in 2 minutes

        self.counter = 120
        self.timer_id = None
        self.label = None

    def do_activate(self):
        self.timer_id = GLib.timeout_add(1000, self.update_counter)     # Start the timer

        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Alexa Shutdown pc")
        window.set_default_size(350, 150)                               # Set the size of the window
        window.set_resizable(False)                                     # Fixes the window from being resized

        def on_cancel_clicked(button):
            GLib.source_remove(self.timer_id)
            self.label.set_label("Shutdown aborted")

            subprocess.run(["shutdown", "-c"])                          # Cancel shutdown
            button.set_sensitive(False)  

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        window.set_child(box)                                           

        self.label = Gtk.Label(label=" ")
        self.label.set_margin_top(50)
        self.label.set_margin_bottom(50)
        self.label.set_halign(Gtk.Align.CENTER)
        self.label.set_valign(Gtk.Align.CENTER)
        box.append(self.label)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_bottom(10)

        box.append(button_box)

        btn_cancel = Gtk.Button(label="Cancel")
        btn_cancel.set_size_request(100, -1)
        button_box.append(btn_cancel)

        btn_Shutdown = Gtk.Button(label="Shutdown")
        btn_Shutdown.set_size_request(100, -1)
        button_box.append(btn_Shutdown)

        def update_counter():
            minutes = self.counter // 60
            seconds = self.counter % 60
            self.label.set_label("Shutting pc down in " + str(minutes) + " minutes and " + str(seconds) + " seconds")
            self.counter -= 1
            if self.counter == 0:
                GLib.source_remove(self.timer_id)
            return True


        def on_shutdown_clicked(button):
            os.system('systemctl poweroff')                             # Force shutdown instantly

        btn_cancel.connect("clicked", on_cancel_clicked)
        btn_Shutdown.connect("clicked", on_shutdown_clicked)

        window.connect("destroy", on_destroy)                           # Connect the window destroy to the on_destroy

        window.set_visible(True)

    def update_counter(self):
        minutes = self.counter // 60
        seconds = self.counter % 60
        self.label.set_label("Shutting pc down in " + str(minutes) + " minutes and " + str(seconds) + " seconds")
        self.counter -= 1
        if self.counter == 0:
            GLib.source_remove(self.timer_id)
        return True

app = CentralizedTextApp()
app.run(None)
