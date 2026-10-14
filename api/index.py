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
        
        stream_url = None
        
        try:
            # 1. Petición a la web principal de Telefe
            req = urllib.request.Request(target_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                
            # Buscar si el m3u8 ya viene explícito
            match_m3u8 = re.search(r'(https?://[^\s<>"]+?mdstrm\.com[^\s<>"]*?\.m3u8[^\s<>"]*)', html_content)
            if match_m3u8:
                stream_url = match_m3u8.group(1)
            else:
                # 2. Si no está directo, buscamos la URL del reproductor embebido de mdstrm
                match_embed = re.search(r'https?://[^\s<>"]+?mdstrm\.com/[^\s<>"]+', html_content)
                if match_embed:
                    embed_url = match_embed.group(0).split('"')[0].split("'")[0].split('\\')[0]
                    
                    # 3. Entramos al reproductor de mdstrm para extraer el stream real
                    req_embed = urllib.request.Request(embed_url, headers=headers)
                    with urllib.request.urlopen(req_embed, timeout=8) as embed_resp:
                        embed_html = embed_resp.read().decode('utf-8', errors='ignore')
                        
                    match_sub = re.search(r'(https?://[^\s<>"]+?\.m3u8[^\s<>"]*)', embed_html)
                    if match_sub:
                        stream_url = match_sub.group(1)

            if stream_url:
                m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="Telefe" tvg-name="Telefe" tvg-logo="https://i.imgur.com/telefe_logo.png",Telefe En Vivo
{stream_url}
"""
                self.send_response(200)
                self.send_header('Content-type', 'audio/x-mpegurl')
                self.end_headers()
                self.wfile.write(m3u_content.encode('utf-8'))
                return
                
        except Exception as e:
            pass
            
        self.send_response(500)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"No se pudo extraer el enlace dinamico de mdstrm")
