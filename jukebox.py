import tkinter
import sqlite3


class ScrollBox(tkinter.Listbox):
    """Class that inherits from tkinter.Listbox class. Allows to create Listbox and Scrollbar with __init__ method.
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
    """"Class allows to display data from database using the simple GUI.
    If in the database are store connected tables, user can choose record and in the next GUI listBox will appearance
    data linked with chosen record.

        Attributes:
            window(str): Main GUI window earlier configured.
            connection(method): Connection build in function sqlite with database.
            table(str): Name of the table stored in DB which will use to sql query.
            field(str): Name of field from table which will use to sql query.
            sort_order(tuple): Parameters according to which will by sort and display records.

        Methods:
            add_song: Used to add new song to the album's track list
            clear(): Used to clear indicated listBox
            link(): Used to link relationship between listBox
            requery(): Used to display records in indicated listBox
            on_select(): Used to find _id chosen element in the listBox and search matching records from connected
            listBox. Then call the requery method and display matching records in the next listBox.
        """

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)
        self.linked_box = None
        self.link_field = None
        self.link_value = None

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
        self.link_value = link_value  # store the _id the master record
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
        if self.linked_box and self.curselection():
            index = self.curselection()[0]
            name_element = self.get(index)  # It's tuple (query statement)
            if self.link_value:
                # get the ID from database row
                # make sure we're getting the correct one, by including the link value if appropriate
                link_id = self.cursor.execute(self.sql_select + " WHERE " + self.field + " =? AND "
                                              + self.link_field + " =?", (name_element, self.link_value)).fetchone()[1]
            # get artist or album ID
            else:
                link_id = self.cursor.execute(self.sql_select + " WHERE " + self.field + " =?",
                                              (name_element,)).fetchone()[1]
            self.linked_box.requery(link_id)


if __name__ == "__main__":
    conn = sqlite3.connect("music.sqlite")
    print(type(conn), conn)
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
    albumsListbox = DataListBox(mainWindow, conn, "albums", "albums.name", ("albums.name",))
    albumsListbox.grid(row=1, column=1, sticky="nswe", padx=(30, 0))
    albumsListbox.requery()
    artistListbox.link(albumsListbox, "artist")

    # Songs Listbox+ Scrollbar
    songsListbox = DataListBox(mainWindow, conn, "songs", "songs.title", ("songs.track", "songs.title"))
    songsListbox.grid(row=1, column=2, sticky="nswe", padx=(30, 0))
    songsListbox.config(border=2, relief="sunken")
    songsListbox.requery()
    albumsListbox.link(songsListbox, "album")

    mainWindow.mainloop()
    print("Closing database connection.")
    conn.close()

