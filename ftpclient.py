#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from window import Window


if __name__ == "__main__":
    window = Window()
    window.connect("destroy", Gtk.main_quit)
    Gtk.main()