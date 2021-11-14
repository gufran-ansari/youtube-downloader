from __future__ import unicode_literals
import youtube_dl
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog as fd


class Downloader(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        tabControl = ttk.Notebook(root)
        tabControl.configure(width=600, height=400)

        self.download_tab = ttk.Frame(tabControl)
        tabControl.add(self.download_tab, text='Download')
        tabControl.grid()

        self.about_tab = ttk.Frame(tabControl)
        tabControl.add(self.about_tab, text="About")
        tabControl.grid()

        self.options = IntVar()
        self.options.set(value=0)
        self.quality = StringVar()
        self.format = StringVar()
        self.quality_opts = ['144', '320', '720', '1080']
        self.format_opts = ['', 'mp4', 'mp3', 'm4a', 'flac', 'wav', 'acc']

        self.save_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        os.chdir(self.save_path)
        self.download_page()
        self.about_page()

    def download_page(self):
        self.url_label = Label(
            self.download_tab, text='Enter Youtube URL: ')
        self.url_label.grid(column=0, row=1, padx=10, pady=10)

        self.url_entry = Entry(self.download_tab, text='Entry')
        self.url_entry.grid(column=1, row=1, padx=10, pady=10)

        self.option = LabelFrame(
            self.download_tab, text="Download as ", height=50, width=250)
        self.option.grid(column=1, row=2)

        self.video_option = Radiobutton(
            self.option, text='Video', variable=self.options, value=0)
        self.video_option.grid(column=0, row=0, padx=10)

        self.song_option = Radiobutton(
            self.option, text='Song', variable=self.options, value=1)
        self.song_option.grid(column=1, row=0, padx=10)

        self.audioQ_label = Label(self.option, text='Audio Quality')
        self.audioQ_label.grid(column=0, row=1, padx=5)

        self.audioQ_drop = OptionMenu(
            self.option, self.format, *self.format_opts)
        self.audioQ_drop.grid(column=1, row=1)

        self.audioF_label = Label(self.option, text='Audio Format')
        self.audioF_label.grid(column=0, row=2)

        self.audioF_drop = OptionMenu(
            self.option, self.format, *self.format_opts)
        self.audioF_drop.grid(column=1, row=2)

        self.location_label = Label(
            self.download_tab, text='Download Location: ')
        self.location_label.grid(column=0, row=4, padx=5, pady=10)

        self.location_entry = Entry(self.download_tab, width=35)
        self.location_entry.grid(column=1, row=4, columnspan=2)

        self.location_button = Button(
            self.download_tab, text='Set', command=self.set_path)
        self.location_button.grid(column=3, row=4, padx=5, pady=5)

        self.download_button = Button(
            self.download_tab, text='Download', command=self.download)
        self.download_button.grid(column=1, row=5, pady=15)

    def about_page(self):
        pass

    def download(self):
        url = self.url_entry.get()
        ydl = youtube_dl.YoutubeDL(self.get_opts())
        ydl.download([url])

    def set_path(self):
        self.path = fd.askdirectory()
        self.location_entry.delete(0, END)
        self.location_entry.insert(0, str(self.path))

    def get_opts(self):
        save = self.location_entry.get()
        filetype = self.options.get()
        quality = self.quality.get()
        file_format = self.format.get()

        if filetype == 0:
            opts = {
                'verbose': True,
                'fixup': "detect_or_warn",
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }],
                'outtmpl': save + '/%(title)s.%(ext)s',
                'noplaylist': True
            }
        elif filetype == 1:
            opts = {
                'verbose': True,
                'fixup': "detect_or_warn",
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': file_format,
                    'preferredquality': quality,
                }],
                'extractaudio': True,
                'outtmpl': save + '/%(title)s.%(ext)s',
                'noplaylist': True
            }
        return opts


if __name__ == '__main__':
    root = Tk()
    root.title('Youtube Downloader')
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    icon = PhotoImage(file='icon.png')
    root.iconphoto(False, icon)
    Downloader(root)
    root.mainloop()
