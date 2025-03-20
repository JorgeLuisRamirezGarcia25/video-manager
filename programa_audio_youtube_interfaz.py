import yt_dlp
import os
import json
from tkinter import filedialog, Tk, Button, Label, Entry, messagebox
from threading import Thread

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("400x200")
        
        # Labels
        self.url_label = Label(root, text="URL de Playlist de YouTube o Archivo:")
        self.url_label.pack(pady=10)
        
        # Entry field for URL or file
        self.url_entry = Entry(root, width=50)
        self.url_entry.pack(pady=10)
        
        # Button to choose download folder
        self.folder_button = Button(root, text="Seleccione la carpeta de descarga", command=self.choose_folder)
        self.folder_button.pack(pady=5)
        
        # Download button
        self.download_button = Button(root, text="Descargar", command=self.start_download)
        self.download_button.pack(pady=10)
        
        # Download status label
        self.status_label = Label(root, text="")
        self.status_label.pack(pady=10)
        
        # Folder path for download
        self.download_folder = ""
        
    def choose_folder(self):
        # Let user choose a folder to save videos
        self.download_folder = filedialog.askdirectory()
        if self.download_folder:
            self.status_label.config(text=f"Descargar carpeta configurada en: {self.download_folder}")

    def start_download(self):
        # Start the download process in a separate thread
        url_or_file = self.url_entry.get()
        if not url_or_file:
            messagebox.showerror("Error", "Por favor introduzca una URL de playlist de YouTube o ruta de archivo.")
            return
        if not self.download_folder:
            messagebox.showerror("Error", "Por favor seleccione una carpeta de descarga.")
            return
        
        self.status_label.config(text="Downloading...")
        download_thread = Thread(target=self.download_videos, args=(url_or_file,))
        download_thread.start()

    def download_videos(self, url_or_file):
        # Check if the input is a URL or a file path
        video_urls = []
        if os.path.isfile(url_or_file):
            with open(url_or_file, 'r') as file:
                video_urls = file.read().splitlines()
        else:
            video_urls = [url_or_file]
        
        # Download videos as audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',  # Descargar solo el mejor audio disponible
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'noplaylist': False,  # Set this to True to avoid downloading playlists
            'ignoreerrors': True,  # Ignore errors and continue downloading
            'verbose': True,  # Enable verbose output to see details in the console
            'progress_hooks': [self.my_hook],  # Hook for download status updates
            'postprocessors': [{  # Convert the audio to MP3
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'retries': 40,  # Intentos de reintento
            'connect_timeout': 2000,  # Aumentar el tiempo de espera de conexión
        }

        # Iniciar el proceso de descarga
        for url in video_urls:
            # Generate file name based on URL title (it avoids duplicate downloads)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                title = info_dict.get('title', None)
                file_name = os.path.join(self.download_folder, f"{title}.mp3")
            
            # Verificar si el archivo ya existe
            if os.path.exists(file_name):
                self.status_label.config(text=f"Saltando (ya existe): {file_name}")
                continue
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])  # Intentar descargar el video
                    self.status_label.config(text="Descarga completa! Ignorando videos inaccesibles.")
            except Exception as e:
                self.status_label.config(text=f"Error: {e}")
                messagebox.showerror("Error de Descarga", str(e))

    def my_hook(self, d):
        if d['status'] == 'downloading':
            self.status_label.config(text=f"Descargando: {d['_percent_str']} of {d['filename']}")
        elif d['status'] == 'finished':
            self.status_label.config(text="Descarga completada, finalizando...")

if __name__ == "__main__":
    root = Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
