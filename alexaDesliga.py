#vinicius

import gi
import subprocess
import os   

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class CenteredTextWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Desligar PC con Alexa")
        self.set_default_size(300, 200)                 #screen size
        self.set_resizable(False)                       #screen size fixed
        self.set_position(Gtk.WindowPosition.CENTER)    #screem position

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_box)

        self.label = Gtk.Label()
        main_box.pack_start(self.label, True, True, 0)

        self.label.set_halign(Gtk.Align.CENTER)         #horizontal alignment to center
        self.label.set_valign(Gtk.Align.CENTER)         #vertical alignment to center

        button_box = Gtk.Box(spacing=6)
        main_box.pack_start(button_box, False, False, 0)

        button_box.set_halign(Gtk.Align.END)
        button_box.set_hexpand(True)

        btnCancelar = Gtk.Button(label="Cancelar")
        btnCancelar.connect("clicked", self.on_btnCancelar_clicked)
        btnCancelar.set_size_request(100, 30)                       #button size
        btnCancelar.set_margin_bottom(10)                           #button margin
        button_box.pack_start(btnCancelar, False, False, 0)         #button position

        btnDesligar = Gtk.Button(label="Desligar")
        btnDesligar.connect("clicked", self.on_btnDesligar_clicked)
        btnDesligar.set_size_request(100, 30)                       #button size
        btnDesligar.set_margin_end(10)                              #button margin
        btnDesligar.set_margin_bottom(10)                           #button margin
        button_box.pack_start(btnDesligar, False, False, 0)         #button position

        subprocess.run(["shutdown", "+2"])                          #shutdown in 2 minutes
        self.counter = 120                                          #time to shutdown   
        self.update_counter()
        self.timeout_id = None                                      #Initialize the timeout ID

    def update_counter(self):
        self.label.set_text(f"Desligando computador em {self.counter} segundos!")

        if self.counter > 0:
            self.counter -= 1
            self.timeout_id = GLib.timeout_add_seconds(1, self.update_counter)

    def on_btnCancelar_clicked(self, button):
        subprocess.run(["shutdown", "-c"])          #Cancel shutdown
        subprocess.run(["shutdown", "--show"])      #Show shutdown schedule
        if self.timeout_id is not None:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None                  #Reset the timeout ID

    def on_btnDesligar_clicked(self, button):
        os.system('systemctl poweroff')             #Shutdown

win = CenteredTextWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
