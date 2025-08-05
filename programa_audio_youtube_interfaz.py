#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Audio Downloader Pro
Aplicación moderna para descargar audio de YouTube con interfaz responsive
"""

import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
import datetime

# Fallback para dependencias opcionales
try:
    import tkinterdnd2 as tkdnd
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class ModernYouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.download_folder = ""
        
        # Initialize variables
        self.quality_var = tk.StringVar(value="192")
        self.format_var = tk.StringVar(value="mp3")
        self.download_playlist_var = tk.BooleanVar(value=True)
        self.skip_existing_var = tk.BooleanVar(value=True)
        self.retry_var = tk.IntVar(value=3)
        
        self.setup_window()
        self.create_widgets()
        if DND_AVAILABLE:
            self.setup_drag_drop()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("🎵 YouTube Audio Downloader Pro")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        self.root.configure(bg='#f0f0f0')
        
        # Make responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text="🎵 YouTube Audio Downloader Pro", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Descarga audio de alta calidad - Soporte para playlists completas",
                                  font=('Arial', 10))
        subtitle_label.grid(row=1, column=0)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="📥 URL o Archivo", padding="15")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        input_frame.grid_columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(input_frame, text="URL de YouTube:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, font=('Arial', 10))
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.url_var.trace('w', lambda *args: self.update_download_button_state())
        
        ttk.Button(input_frame, text="📋 Pegar", command=self.paste_from_clipboard).grid(row=0, column=2)
        
        # File selection
        ttk.Label(input_frame, text="O selecciona archivo:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(10, 0))
        ttk.Button(input_frame, text="📁 Seleccionar Archivo", command=self.choose_file).grid(row=1, column=1, sticky="w", pady=(10, 0))
        
        # Drag & drop area
        self.drop_frame = tk.Frame(input_frame, bg='#E3F2FD', relief='groove', bd=2, height=50)
        self.drop_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(15, 0))
        self.drop_frame.grid_propagate(False)
        
        drop_text = "🎯 Arrastra archivos de texto aquí"
        if not DND_AVAILABLE:
            drop_text += " (Drag & Drop no disponible)"
            
        tk.Label(self.drop_frame, text=drop_text, bg='#E3F2FD', 
                font=('Arial', 9)).place(relx=0.5, rely=0.5, anchor='center')
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        control_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.folder_btn = ttk.Button(control_frame, text="📂 Carpeta de Descarga", 
                                    command=self.choose_folder)
        self.folder_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.download_btn = ttk.Button(control_frame, text="⬇️ Descargar Audio", 
                                      command=self.start_download, state='disabled')
        self.download_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        ttk.Button(control_frame, text="⚙️ Configuración", 
                  command=self.show_settings).grid(row=0, column=2, padx=(5, 0), sticky="ew")
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progreso y Estado", padding="15")
        progress_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        progress_frame.grid_rowconfigure(2, weight=1)
        progress_frame.grid_columnconfigure(0, weight=1)
        
        # Folder path display
        self.folder_path_var = tk.StringVar(value="No se ha seleccionado carpeta de descarga")
        ttk.Label(progress_frame, textvariable=self.folder_path_var, 
                 font=('Arial', 9), foreground='gray').grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Status text
        status_frame = ttk.Frame(progress_frame)
        status_frame.grid(row=2, column=0, sticky="nsew")
        status_frame.grid_rowconfigure(0, weight=1)
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_text = tk.Text(status_frame, height=10, font=('Courier', 9), 
                                  bg='#FAFAFA', wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=4, column=0, sticky="ew")
        footer_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.stats_label = ttk.Label(footer_frame, text="📈 Descargas: 0 | Exitosas: 0 | Errores: 0",
                                    font=('Arial', 9))
        self.stats_label.grid(row=0, column=0, sticky="w")
        
        ttk.Label(footer_frame, text="v2.0 Pro", font=('Arial', 9)).grid(row=0, column=1, sticky="e")
        
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            self.drop_frame.drop_target_register(tkdnd.DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        except:
            pass
            
    def paste_from_clipboard(self):
        """Paste URL from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_var.set(clipboard_content)
            self.log_status("📋 URL pegada desde el portapapeles")
        except:
            messagebox.showwarning("Advertencia", "No hay contenido válido en el portapapeles")
    
    def choose_file(self):
        """Choose a file containing URLs"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo con URLs",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.url_var.set(file_path)
            self.log_status(f"📁 Archivo seleccionado: {os.path.basename(file_path)}")
    
    def on_drop(self, event):
        """Handle drag and drop files"""
        if not DND_AVAILABLE:
            return
            
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            if os.path.isfile(file_path) and file_path.endswith('.txt'):
                self.url_var.set(file_path)
                self.log_status(f"🎯 Archivo arrastrado: {os.path.basename(file_path)}")
            else:
                messagebox.showwarning("Advertencia", "Solo se aceptan archivos de texto (.txt)")
        
    def choose_folder(self):
        """Choose download folder"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta de descarga")
        if folder:
            self.download_folder = folder
            folder_display = folder if len(folder) <= 60 else "..." + folder[-57:]
            self.folder_path_var.set(f"📂 {folder_display}")
            self.log_status(f"📂 Carpeta configurada: {folder}")
            self.update_download_button_state()
    
    def update_download_button_state(self):
        """Update download button state"""
        url_or_file = self.url_var.get().strip()
        has_input = bool(url_or_file)
        has_folder = bool(self.download_folder)
        
        if has_input and has_folder:
            self.download_btn.config(state='normal')
        else:
            self.download_btn.config(state='disabled')
    
    def log_status(self, message):
        """Log status with timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, formatted_message)
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Configuración Avanzada")
        settings_window.geometry("450x400")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Center settings window
        settings_window.update_idletasks()
        x = self.root.winfo_x() + 50
        y = self.root.winfo_y() + 50
        settings_window.geometry(f"450x400+{x}+{y}")
        
        main_frame = ttk.Frame(settings_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Quality settings
        quality_frame = ttk.LabelFrame(main_frame, text="🎵 Calidad de Audio", padding="10")
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(quality_frame, text="128 kbps (Básica)", 
                       variable=self.quality_var, value="128").pack(anchor=tk.W)
        ttk.Radiobutton(quality_frame, text="192 kbps (Buena)", 
                       variable=self.quality_var, value="192").pack(anchor=tk.W)
        ttk.Radiobutton(quality_frame, text="320 kbps (Excelente)", 
                       variable=self.quality_var, value="320").pack(anchor=tk.W)
        
        # Format settings
        format_frame = ttk.LabelFrame(main_frame, text="📁 Formato de Salida", padding="10")
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(format_frame, text="MP3 (Recomendado)", 
                       variable=self.format_var, value="mp3").pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="M4A (Apple)", 
                       variable=self.format_var, value="m4a").pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="OGG (Open Source)", 
                       variable=self.format_var, value="ogg").pack(anchor=tk.W)
        
        # Advanced options
        advanced_frame = ttk.LabelFrame(main_frame, text="🔧 Opciones Avanzadas", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(advanced_frame, text="Omitir archivos existentes", 
                       variable=self.skip_existing_var).pack(anchor=tk.W)
        
        ttk.Checkbutton(advanced_frame, text="Descargar playlists completas", 
                       variable=self.download_playlist_var).pack(anchor=tk.W, pady=(5, 0))
        
        ttk.Label(advanced_frame, text="(Si está desmarcado, solo descarga el primer video)", 
                 font=('Arial', 8)).pack(anchor=tk.W, padx=(20, 0))
        
        ttk.Label(advanced_frame, text="Número de reintentos:").pack(anchor=tk.W, pady=(10, 0))
        
        retry_frame = ttk.Frame(advanced_frame)
        retry_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Scale(retry_frame, from_=1, to=10, variable=self.retry_var, 
                 orient=tk.HORIZONTAL).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(retry_frame, textvariable=self.retry_var).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="💾 Guardar", 
                  command=settings_window.destroy).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Cancelar", 
                  command=settings_window.destroy).pack(side=tk.RIGHT)

    def start_download(self):
        """Start download process"""
        url_or_file = self.url_var.get().strip()
        
        if not url_or_file:
            messagebox.showerror("❌ Error", "Por favor introduce una URL o selecciona un archivo.")
            return
            
        if not self.download_folder:
            messagebox.showerror("❌ Error", "Por favor selecciona una carpeta de descarga.")
            return
        
        self.download_btn.config(state='disabled', text="⏳ Descargando...")
        self.progress_var.set(0)
        
        # Clear status
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
        self.log_status("🚀 Iniciando descarga...")
        
        # Start download thread
        download_thread = Thread(target=self.download_videos, args=(url_or_file,))
        download_thread.daemon = True
        download_thread.start()

    def download_videos(self, url_or_file):
        """Download videos function"""
        try:
            # Get URLs
            video_urls = []
            if os.path.isfile(url_or_file):
                self.log_status(f"📄 Leyendo archivo: {os.path.basename(url_or_file)}")
                with open(url_or_file, 'r', encoding='utf-8') as file:
                    video_urls = [line.strip() for line in file.readlines() if line.strip()]
            else:
                video_urls = [url_or_file]
            
            if not video_urls:
                self.log_status("❌ No se encontraron URLs válidas")
                return
            
            self.log_status(f"📋 Total URLs: {len(video_urls)}")
            
            # Get settings
            quality = self.quality_var.get()
            format_ext = self.format_var.get()
            download_playlist = self.download_playlist_var.get()
            
            # yt-dlp options
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(
                    self.download_folder, 
                    '%(playlist_index)02d - %(title)s.%(ext)s' if download_playlist 
                    else '%(title)s.%(ext)s'
                ),
                'noplaylist': not download_playlist,
                'ignoreerrors': True,
                'progress_hooks': [self.progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_ext,
                    'preferredquality': quality,
                }],
                'retries': self.retry_var.get(),
                'socket_timeout': 30,
            }
            
            # Statistics
            total_count = len(video_urls)
            success_count = 0
            error_count = 0
            
            # Download each URL
            for i, url in enumerate(video_urls, 1):
                try:
                    self.log_status(f"🎵 [{i}/{total_count}] Procesando: {url[:50]}...")
                    
                    # Check if playlist
                    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
                        try:
                            info_dict = ydl.extract_info(url, download=False)
                            if 'entries' in info_dict:
                                playlist_title = info_dict.get('title', 'Unknown Playlist')
                                entry_count = len(list(info_dict['entries']))
                                if download_playlist:
                                    self.log_status(f"🎼 Playlist: '{playlist_title}' ({entry_count} elementos) - Descargando todos")
                                else:
                                    self.log_status(f"🎼 Playlist: '{playlist_title}' ({entry_count} elementos) - Solo el primero")
                            else:
                                video_title = info_dict.get('title', 'Unknown Video')
                                self.log_status(f"🎵 Video: '{video_title}'")
                        except Exception as e:
                            self.log_status(f"⚠️ No se pudo obtener info previa: {str(e)}")
                    
                    # Download
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                        success_count += 1
                        self.log_status(f"✅ Descarga exitosa")
                        
                except Exception as e:
                    error_count += 1
                    self.log_status(f"❌ Error: {str(e)}")
                
                # Update progress
                progress = (i / total_count) * 100
                self.progress_var.set(progress)
                self.root.update_idletasks()
            
            # Final status
            self.log_status(f"🎉 Completado! Exitosas: {success_count}, Errores: {error_count}")
            self.update_stats(total_count, success_count, error_count)
            
        except Exception as e:
            self.log_status(f"❌ Error crítico: {str(e)}")
        finally:
            self.root.after(0, self.reset_download_button)
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            try:
                filename = os.path.basename(d.get('filename', 'Unknown'))
                percent = d.get('_percent_str', '0%')
                speed = d.get('_speed_str', 'N/A')
                self.log_status(f"⬇️ {filename}: {percent} a {speed}")
            except:
                pass
        elif d['status'] == 'finished':
            filename = os.path.basename(d.get('filename', 'Unknown'))
            self.log_status(f"✅ Completado: {filename}")
    
    def reset_download_button(self):
        """Reset download button"""
        self.download_btn.config(state='normal', text="⬇️ Descargar Audio")
        self.progress_var.set(0)
        self.update_download_button_state()
    
    def update_stats(self, total, success, errors):
        """Update statistics"""
        stats_text = f"📈 Descargas: {total} | Exitosas: {success} | Errores: {errors}"
        self.stats_label.config(text=stats_text)

def main():
    """Main function"""
    # Create root window
    if DND_AVAILABLE:
        root = tkdnd.Tk()
    else:
        root = tk.Tk()
    
    # Create app
    app = ModernYouTubeDownloader(root)
    
    # Initial messages
    app.log_status("🎵 YouTube Audio Downloader Pro iniciado")
    if not DND_AVAILABLE:
        app.log_status("⚠️ Drag & Drop no disponible (instalar tkinterdnd2)")
    
    # Run
    root.mainloop()

if __name__ == "__main__":
    main()
