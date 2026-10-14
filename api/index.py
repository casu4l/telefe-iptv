from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enlace funcional de mdstrm de Telefe extraído directamente
        stream_url = "https://us-b4-p-e-zs14.cdn.mdstrm.com/live-stream-gdai/6a024684fd4ca6a938f3a118/linear/hls/pa/event/ZTApTmdVQWOhwTvIXtIGXQ/stream/ff76acda-aff5-4983-a540-37f11c5a145d:TUL/variant/27d892eda46db8ff6803150f828bc30a/bandwidth/1491534.m3u8?aid=69dfb44d09ecc98dc876969f&uid=sNcOwi3Y5nfnCwi2kT3ZKaG089JjJe0a&sid=nfty2UCXkvKUxEGXnle92quDH7OKfgMf&pid=CzBC4IToFiK2qaekfhpDwqOxGrggBcLK&pid_dvr=KJVfRnpT75oBhziHcj66bqlqSpUJ0TZK&ref=https%3A%2F%2Fwww.mitelefe.com%2F&without_cookies=false&listenerid=&dnt=true&access_token=zSdze5aOR7XY1ozeOYuk3eolV7KHq53QeBkXGLwjJ2pnjvzB8QEEsRi745r9rMFsnzMiHaE8YXP&adInsertionGoogleStreamId=ff76acda-aff5-4983-a540-37f11c5a145d%3ATUL&CMCD=cid%3D%226a024684fd4ca6a938f3a118%22%2Cmtp%3D1600%2Cot%3Dm%2Csf%3Dh%2Csid%3D%22CzBC4IToFiK2qaekfhpDwqOxGrggBcLK%22&es=us-b4-p-e-zs14.cdn.mdstrm.com&ote=1792098683750&ot=1-7JgoAIFy-ioDbbBT1B4g&proto=https&pz=us"

        m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="Telefe" tvg-name="Telefe" tvg-logo="https://i.imgur.com/telefe_logo.png",Telefe En Vivo
{stream_url}
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'audio/x-mpegurl')
        self.end_headers()
        self.wfile.write(m3u_content.encode('utf-8'))
