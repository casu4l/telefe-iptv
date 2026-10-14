from http.server import BaseHTTPRequestHandler
import urllib.request
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Usamos el endpoint de configuración del reproductor de mdstrm para Telefe
        player_api_url = "https://mdstrm.com/playback/6a024684fd4ca6a938f3a118"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.mitelefe.com/'
        }
        
        try:
            req = urllib.request.Request(player_api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            # Extraemos el link HLS (.m3u8) directamente del JSON de respuesta de mdstrm
            stream_url = data.get('streams', {}).get('hls', {}).get('src')
            
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
        self.wfile.write(b"No se pudo consultar la API de mdstrm")
