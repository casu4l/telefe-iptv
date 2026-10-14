from http.server import BaseHTTPRequestHandler
import urllib.request
import re

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        target_url = "https://www.mitelefe.com/telefe-en-vivo"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.mitelefe.com/'
        }
        
        try:
            req = urllib.request.Request(target_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                
            # Buscar cualquier enlace m3u8 de mdstrm en el código de la página
            match = re.search(r'(https?://[^\s<>"]+?mdstrm\.com[^\s<>"]*?\.m3u8[^\s<>"]*)', html_content)
            
            if match:
                stream_url = match.group(1)
                
                m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="Telefe" tvg-name="Telefe" tvg-logo="https://i.imgur.com/telefe_logo.png",Telefe En Vivo
{stream_url}
"""
                self.send_response(200)
                self.send_header('Content-type', 'audio/x-mpegurl')
                self.end_headers()
                self.wfile.write(m3u_content.encode('utf-8'))
                return
                
        except Exception:
            pass
            
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"No se pudo extraer el enlace mdstrm de Telefe")
