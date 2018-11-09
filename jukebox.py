import tkinter
import sqlite3

conn = sqlite3.connect("music.sqlite")
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

# Artists Listbox
artistList = tkinter.Listbox(mainWindow)
# padx=(left_side_distance, right_side_distance)
artistList.grid(row=1, column=0, sticky='nswe', rowspan=2, padx=(30, 0))
artistList.config(border=2, relief="sunken")

# Albums Listbox
albumsListbox = tkinter.Listbox(mainWindow)
albumsListbox.grid(row=1, column=1, sticky="nswe", padx=(30, 0))
albumsListbox.config(border=2, relief="sunken")

# Songs Listbox
songsListbox = tkinter.Listbox(mainWindow)
songsListbox.grid(row=1, column=2, sticky="nswe", padx=(30, 0))
songsListbox.config(border=2, relief="sunken")

mainWindow.mainloop()
