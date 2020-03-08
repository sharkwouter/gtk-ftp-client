import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

@Gtk.Template.from_file("window.glade")
class Window(Gtk.ApplicationWindow):

    __gtype_name__ = "Window"

    button_connect = Gtk.Template.Child()
    button_left = Gtk.Template.Child()
    button_right = Gtk.Template.Child()
    button_up_left = Gtk.Template.Child()
    treeview_left = Gtk.Template.Child()
    treeview_right = Gtk.Template.Child()

    def __init__(self):
        Gtk.ApplicationWindow.__init__(self, title="FTP Client")
        self.current_directory_left = os.getcwd()
        self.current_directory_right = os.path.expanduser("~/")
        self.add_list(self.treeview_left, self.current_directory_left)
        self.add_list(self.treeview_right, self.current_directory_right)
        self.show_all()

    @Gtk.Template.Callback("on_button_up_left_clicked")
    def button_up_left_clicked(self, widget):
        self.current_directory_left = os.path.abspath(os.path.join(self.current_directory_left, ".."))
        self.add_list(self.treeview_right, self.current_directory_left)


    def add_list(self, treeview, directory):
        treeview.set_model(self.make_file_list(directory))
        self.make_columns(treeview)

    def make_file_list(self, directory):
        liststore = Gtk.ListStore(str, str, str)
        liststore.append(["gtk-directory", "..", ""])
        for file_name in os.listdir(directory):
            if file_name.startswith("."):
                continue
            file_path = os.path.join(directory, file_name)
            if os.path.isdir(file_path):
                icon = "gtk-directory"
            else:
                icon = "gtk-file"
            try:
                file_stat = os.stat(file_path)
                size = self.size_to_human_readable(file_stat.st_size)
            except FileNotFoundError:
                continue
            liststore.append([icon, file_name, size])

        return liststore

    def make_columns(self, treeview):
        renderer_text = Gtk.CellRendererText()
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_icon = Gtk.TreeViewColumn("Icon",renderer_pixbuf, icon_name=0)
        column_name = Gtk.TreeViewColumn("Name", renderer_text, text=1)
        column_size = Gtk.TreeViewColumn("Size", renderer_text, text=2)
        treeview.append_column(column_icon)
        treeview.append_column(column_name)
        treeview.append_column(column_size)

    def size_to_human_readable(self, size: int, suffix='B') -> str:
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(size) < 1024.0:
                return "%3.1f%s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f%s%s" % (size, 'Yi', suffix)
