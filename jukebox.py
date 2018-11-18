import tkinter
import sqlite3


class ScrollBox(tkinter.Listbox):

    """
    Class that inherits from tkinter.Listbox class. Allows to create Listbox and Scrollbar with __init__ method.
    Contains also grid method which allows to pack both elements inside the window.
    """
    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)
        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky="nsw", rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, sticky="nse", rowspan=rowspan, columnspan=columnspan, **kwargs)
        self["yscrollcommand"] = self.scrollbar.set


class DataListBox(ScrollBox):

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)
        self.linked_box = None
        self.link_field = None

        self.cursor = connection.cursor()
        self.table = table
        self.field = field

        self.bind("<<ListboxSelect>>", self.on_select)

        self.sql_select = "SELECT " + self.field + ", _id " + "FROM " + table
        if sort_order:
            self.sql_sort = " ORDER BY " + ",".join(sort_order)
        else:
            self.sql_sort = " ORDER BY " + self.field

    def clear(self):
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        self.linked_box = widget
        widget.link_field = link_field

    def requery(self, link_value=None):
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.link_field + "=?" + self.sql_sort
            self.cursor.execute(sql, (link_value,))

        else:
            self.cursor.execute(self.sql_select + self.sql_sort)

        # clear listbox content before re-loading
        self.clear()
        for value in self.cursor:
            self.insert(tkinter.END, value[0])

        if self.linked_box:
            self.linked_box.clear()

    def on_select(self, event):
        if self.linked_box:
            if self.curselection():
                index = self.curselection()[0]
                name_element = self.get(index),  # It's tuple (query statement)
                # Get artist ID
                link_id = self.cursor.execute(self.sql_select + " WHERE " + self.field + " =?",
                                              name_element).fetchone()[1]
                self.linked_box.requery(link_id)


if __name__ == "__main__":
    conn = sqlite3.connect("music.sqlite")

    mainWindow = tkinter.Tk()
    mainWindow.geometry("1024x768")
    mainWindow.title("Music DB Browser")

    # Configure proportion between columns and rows
    mainWindow.columnconfigure(0, weight=2)
    mainWindow.columnconfigure(1, weight=2)
    mainWindow.columnconfigure(2, weight=2)
    mainWindow.columnconfigure(3, weight=1)  # spacer column on right

    mainWindow.rowconfigure(0, weight=1)
    mainWindow.rowconfigure(1, weight=5)
    mainWindow.rowconfigure(2, weight=5)
    mainWindow.rowconfigure(3, weight=1)

    # Labels with name of columns
    artistLabel = tkinter.Label(mainWindow, text="Artist").grid(row=0, column=0)
    albumsLabel = tkinter.Label(mainWindow, text="Albums").grid(row=0, column=1)
    songsLabel = tkinter.Label(mainWindow, text="Songs").grid(row=0, column=2)

    # Artists Listbox + Scrollbar
    artistListbox = DataListBox(mainWindow, conn, "artists", "artists.name")
    artistListbox.grid(1, 0, rowspan=2, padx=(30, 0), sticky="nswe")
    # padx=(left_side_distance, right_side_distance)
    artistListbox.config(border=2, relief="sunken")
    artistListbox.config(border=2, relief="sunken")
    artistListbox.requery()  # Add artist list from database

    # Albums Listbox + Scrollbar
    albumLV = tkinter.Variable(mainWindow)
    albumLV.set(("Choose an artist.",))
    albumsListbox = DataListBox(mainWindow, conn, "albums", "albums.name", ("albums.name",), listvariable=albumLV)
    albumsListbox.grid(row=1, column=1, sticky="nswe", padx=(30, 0))
    artistListbox.link(albumsListbox, "artist")

    # Songs Listbox+ Scrollbar
    songsLV = tkinter.Variable(mainWindow)
    songsLV.set(("Choose an album.",))
    songsListbox = DataListBox(mainWindow, conn, "songs", "songs.title", ("songs.track", "songs.title"),
                               listvariable=songsLV)
    songsListbox.grid(row=1, column=2, sticky="nswe", padx=(30, 0))
    songsListbox.config(border=2, relief="sunken")
    albumsListbox.link(songsListbox, "album")

    mainWindow.mainloop()
    print("Closing database connection.")
    conn.close()
