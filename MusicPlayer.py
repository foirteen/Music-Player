import tkinter as tk
import fnmatch
import os
from pygame import mixer

class MusicPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player by kelompok 4")
        self.master.geometry("650x650")
        self.master.config(bg='black')

        self.rootpath = "C:\\Users\All Users.DESKTOP-0Q7IECQ\Desktop\music"
        self.pattern = "*.mp3"
        mixer.init()

        self.prev_img = tk.PhotoImage(file="prev_img.png")
        self.stop_img = tk.PhotoImage(file="stop_img.png")
        self.play_img = tk.PhotoImage(file="play_img.png")
        self.pause_img = tk.PhotoImage(file="pause_img.png")
        self.next_img = tk.PhotoImage(file="next_img.png")

        self.create_widgets()
        self.populate_listbox()

    def create_widgets(self):
        self.create_search_widgets()

        self.listbox = tk.Listbox(self.master, fg="black", bg="white", width=100, font=('ds-digital', 14))
        self.listbox.pack(padx=15, pady=15)

        top_frame = tk.Frame(self.master, bg="black")
        top_frame.pack(padx=10, pady=5, anchor='center')

        buttons = [
            ("prev", self.prev_img, self.play_prev),
            ("stop", self.stop_img, self.stop),
            ("play", self.play_img, self.select),
            ("pause", self.pause_img, self.pause_song),
            ("next", self.next_img, self.play_next),
        ]

        for text, image, command in buttons:
            button = tk.Button(self.master, text=text, image=image, bg="black", borderwidth=0, command=command)
            button.pack(pady=15, in_=top_frame, side="left")

        self.label = tk.Label(self.master, text='', bg="black", fg="yellow", font=('ds-digital', 18))
        self.label.pack(pady=15)

    def create_search_widgets(self):
        self.search_label = tk.Label(self.master, text="Enter your search query:", bg="black", fg="white")
        self.search_label.pack(pady=5)

        self.search_entry = tk.Entry(self.master, width=40)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.master, text="Search", command=self.perform_search)
        self.search_button.pack(pady=5)

    def populate_listbox(self):
        for root, dirs, files in os.walk(self.rootpath):
            for filename in fnmatch.filter(files, self.pattern):
                self.listbox.insert('end', filename)

    def perform_search(self):
        query = self.search_entry.get().lower()
        results = self.search(query)

        self.listbox.delete(0, 'end')  # Clear previous listbox content
        self.populate_listbox()  # Repopulate the listbox with all songs

        if results:
            self.listbox.selection_clear(0, 'end')  # Clear previous selection
            for result in results:
                index = self.listbox.get(0, 'end').index(result)
                self.listbox.selection_set(index)

    def search(self, query):
        # For demonstration purposes, a simple list of strings is used as the data.
        data = [filename.lower() for filename in os.listdir(self.rootpath) if fnmatch.fnmatch(filename, self.pattern)]

        # Perform a case-insensitive search and return matching results.
        return [result for result in data if query in result]

    def select(self):
        selected_song = self.listbox.get("anchor")
        self.label.config(text=selected_song)
        mixer.music.load(os.path.join(self.rootpath, selected_song))
        mixer.music.play()

    def stop(self):
        mixer.music.stop()
        self.listbox.selection_clear('active')

    def play_next(self):
        current_index = self.listbox.curselection()[0]
        next_index = current_index + 1 if current_index < self.listbox.size() - 1 else 0
        self.play_song_by_index(next_index)

    def play_prev(self):
        current_index = self.listbox.curselection()[0]
        prev_index = current_index - 1 if current_index > 0 else self.listbox.size() - 1
        self.play_song_by_index(prev_index)

    def play_song_by_index(self, index):
        next_song_name = self.listbox.get(index)
        self.label.config(text=next_song_name)
        mixer.music.load(os.path.join(self.rootpath, next_song_name))
        mixer.music.play()
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(index)

    def pause_song(self):
        if self.pausebutton["text"] == "Pause":
            mixer.music.pause()
            self.pausebutton["text"] = "Play"
        else:
            mixer.music.unpause()
            self.pausebutton["text"] = "Pause"


if __name__ == "__main__":
    canvas = tk.Tk()
    app = MusicPlayerApp(canvas)
    canvas.mainloop()
