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

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Alexa Shutdown pc")
        window.set_default_size(250, 150)                               # Set the size of the window
        window.set_resizable(False)                                     # Fixes the window from being resized

        def on_cancel_clicked(button):
            GLib.source_remove(self.timer_id)
            label.set_label("Shutdown aborted")

            subprocess.run(["shutdown", "-c"])                          # Cancel shutdown
            button.set_sensitive(False)  

            return True

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        window.set_child(box)                                           

        label = Gtk.Label(label="Shuting pc down in " + str(self.counter))
        label.set_margin_top(50)
        label.set_margin_bottom(50)
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)
        box.append(label)

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
            self.counter -= 1
            label.set_label("Shuting pc down in " + str(self.counter))
            if self.counter == 0:
                GLib.source_remove(self.timer_id)
            return True

        def on_shutdown_clicked(button):
            os.system('systemctl poweroff')                             # Force shutdown instantly

        btn_cancel.connect("clicked", on_cancel_clicked)
        btn_Shutdown.connect("clicked", on_shutdown_clicked)

        self.timer_id = GLib.timeout_add(1000, update_counter)

        window.connect("destroy", on_destroy)                           # Connect the window destroy to the on_destroy

        window.set_visible(True)

app = CentralizedTextApp()
app.run(None)
