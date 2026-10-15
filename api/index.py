from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
import urllib.request, urllib.error
import re, time, random, string

CANAL = "6a024684fd4ca6a938f3a118"
REF = "https://www.mitelefe.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": REF,
    "Origin": "https://www.mitelefe.com",
}

def rid(n=32):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))

def pedir(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")

def sacar_token(body):
    m = re.search(r'access_token["\']?\s*[:=]\s*["\']?([A-Za-z0-9_\-\.]+)', body)
    if m:
        return m.group(1)
    limpio = body.strip().strip('"')
    if len(limpio) > 40 and re.fullmatch(r"[A-Za-z0-9_\-\.]+", limpio):
        return limpio
    return None

class handler(BaseHTTPRequestHandler):
    def texto(self, code, msg):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(msg.encode())

    def do_GET(self):
        debug = "debug" in parse_qs(urlparse(self.path).query)
        acceso = (
            f"https://mdstrm.com/api/live-stream/{CANAL}/access"
            f"?_={int(time.time() * 1000)}&G={quote(REF, safe='')}"
        )
        status, body = pedir(acceso)
        token = sacar_token(body) if status == 200 else None

        if debug:
            return self.texto(200, f"Estado: {status}\nToken encontrado: {bool(token)}\n\n{body[:1500]}")
        if not token:
            return self.texto(502, f"No pude obtener el token (estado {status})")

        playlist = (
            f"https://mdstrm.com/live-stream-playlist/{CANAL}.m3u8"
            f"?uid={rid()}&sid={rid()}&pid={rid()}&pid_dvr={rid()}"
            f"&an=Mediastream_Player&at=web-app&av=v7.0.129"
            f"&ref={quote(REF, safe='')}&res=936x527"
            f"&without_cookies=false&listenerid=&dnt=true&access_token={token}"
        )
        self.send_response(302)
        self.send_header("Location", playlist)
        self.end_headers()
