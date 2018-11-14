import tkinter
import sqlite3

conn = sqlite3.connect("music.sqlite")


class ScrollBox(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)
        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky="nsw", rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, sticky="nse", rowspan=rowspan, columnspan=columnspan, **kwargs)
        self["yscrollcommand"] = self.scrollbar.set


mainWindow = tkinter.Tk()
mainWindow.geometry("1024x768")
mainWindow.title("Music DB Browser")

# Configure proportion weight between columns and rows

mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=2)
mainWindow.columnconfigure(2, weight=2)
mainWindow.columnconfigure(3, weight=1)  # spacer column on right

mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=5)
mainWindow.rowconfigure(2, weight=5)
mainWindow.rowconfigure(3, weight=1)

# Labels with name of column
artistLabel = tkinter.Label(mainWindow, text="Artist").grid(row=0, column=0)
albumsLabel = tkinter.Label(mainWindow, text="Albums").grid(row=0, column=1)
songsLabel = tkinter.Label(mainWindow, text="Songs").grid(row=0, column=2)

# Artists Listbox + Scrollbar
artistListbox = ScrollBox(mainWindow)
# padx=(left_side_distance, right_side_distance)
artistListbox.grid(row=1, column=0, sticky='nswe', rowspan=2, padx=(30, 0))
artistListbox.config(border=2, relief="sunken")

# Albums Listbox + Scrollbar
albumLV = tkinter.Variable(mainWindow)
albumLV.set(("Choose an artist.",))
albumsListbox = ScrollBox(mainWindow, listvariable=albumLV)
albumsListbox.grid(row=1, column=1, sticky="nswe", padx=(30, 0))
albumsListbox.config(border=2, relief="sunken")

# Songs Listbox+ Scrollbar
songsLV = tkinter.Variable(mainWindow)
songsLV.set(("Choose an album.",))
songsListbox = ScrollBox(mainWindow, listvariable=songsLV)
songsListbox.grid(row=1, column=2, sticky="nswe", padx=(30, 0))
songsListbox.config(border=2, relief="sunken")


testlist = range(0, 100)
albumLV.set(tuple(testlist))


mainWindow.mainloop()

print("Closing database connection.")
conn.close()
