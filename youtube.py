import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import threading
import os
import sys

class YouTubeDownloader:
    def check_ffmpeg(self):
        ffmpeg_path = os.path.join(self.get_download_dir(), 'ffmpeg', 'bin', 'ffmpeg.exe')
        print(f"Buscando FFmpeg en: {ffmpeg_path}")  # Para depuración

        if not os.path.exists(ffmpeg_path):
            messagebox.showerror(
                "FFmpeg requerido",
                f"FFmpeg no encontrado en:\n{ffmpeg_path}\n\n"
                "Descarga FFmpeg desde:\n"
                "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip\n"
                "y extrae la carpeta 'ffmpeg' junto al archivo .py"
            )
            self.root.destroy()  # Solo se ejecuta si FFmpeg NO está

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        
        # Variables
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar()
        self.formats = []
        
        # Configuración yt-dlp
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'referer': 'https://www.youtube.com/',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            'ffmpeg_location': os.path.join(self.get_download_dir(), 'ffmpeg', 'bin')
        }
        self.check_ffmpeg()
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack()
        
        # Interfaz
        ttk.Label(main_frame, text="URL de YouTube:").grid(row=0, column=0, sticky="w")
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=0, padx=5, pady=5)
        
        ttk.Button(main_frame, text="Buscar calidades", command=self.fetch_formats).grid(row=1, column=1, padx=5)
        
        ttk.Label(main_frame, text="Seleccionar calidad:").grid(row=2, column=0, sticky="w", pady=10)
        self.quality_combobox = ttk.Combobox(main_frame, textvariable=self.quality_var, state="readonly", width=30)
        self.quality_combobox.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.progress_label = ttk.Label(main_frame, text="0%", foreground="gray")
        self.progress_label.grid(row=5, column=0, columnspan=2)
        
        ttk.Button(main_frame, text="Descargar video", command=self.start_download_thread).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.status_label = ttk.Label(main_frame, text="", foreground="gray")
        self.status_label.grid(row=7, column=0, columnspan=2)
    
    def get_download_dir(self):
        if getattr(sys, 'frozen', False):
            # Si está empaquetado con PyInstaller, usar la carpeta del ejecutable
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    
    def fetch_formats(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Introduce una URL válida")
            return
        
        try:
            self.status_label.config(text="Analizando video...", foreground="gray")
            self.root.update()
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Filtrar formatos de video
                video_formats = [
                    f for f in info['formats'] 
                    if f.get('vcodec') != 'none' 
                    and f.get('width') is not None
                    and f.get('height') is not None
                ]
                
                # Ordenar por resolución
                video_formats.sort(key=lambda x: x['height'], reverse=True)
                
                # Obtener resoluciones únicas
                resolutions = []
                seen = set()
                for f in video_formats:
                    res = f"{f['height']}p"
                    if res not in seen and f['height'] <= 2160:  # Filtrar resoluciones realistas
                        seen.add(res)
                        resolutions.append({
                            'resolution': res,
                            'format_id': f['format_id'],
                            'note': f.get('format_note', '')
                        })
                
                # Crear lista legible para el combobox
                format_list = [
                    f"{fmt['resolution']} ({fmt['note']})" 
                    for fmt in resolutions
                ]
                
                self.formats = resolutions
                self.quality_combobox['values'] = format_list
                
                if format_list:
                    self.quality_var.set(format_list[0])
                    self.status_label.config(text="Formatos disponibles", foreground="green")
                else:
                    messagebox.showerror("Error", "No hay formatos disponibles")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar: {str(e)}")
            self.status_label.config(text="Error", foreground="red")
    
    def download_video(self):
        try:
            selected = self.quality_combobox.current()
            if selected == -1:
                messagebox.showerror("Error", "Selecciona una calidad")
                return
            
            format_id = self.formats[selected]['format_id']
            download_dir = self.get_download_dir()
            
            # Configurar opciones de descarga (cambiar noprogress a False)
            download_opts = {
                **self.ydl_opts,
                'format': f"{format_id}+bestaudio",
                'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'progress_hooks': [self.update_progress],
                'noprogress': False  # ← Este era el principal problema
            }
            
            self.status_label.config(text="Preparando descarga...", foreground="blue")
            self.progress_bar['value'] = 0
            self.progress_label.config(text="0%")
            self.root.update()
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                ydl.download([self.url_var.get()])
            
            self.status_label.config(text="Descarga completada!", foreground="green")
            messagebox.showinfo("Éxito", f"Video descargado en:\n{download_dir}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error en descarga: {str(e)}")
            self.status_label.config(text="Error", foreground="red")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            # Usar after() para actualizar la GUI en el hilo principal
            self.root.after(0, lambda: self._update_progress_gui(d))

    def _update_progress_gui(self, d):
        try:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

            if total > 0:
                progress = downloaded / total * 100
                self.progress_bar['value'] = progress
                self.progress_label.config(text=f"{progress:.1f}%")
                self.root.update_idletasks()
        except Exception as e:
            print(f"Error actualizando progreso: {str(e)}")
    
    def start_download_thread(self):
        threading.Thread(target=self.download_video, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()