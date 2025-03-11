import http.server
import socketserver
import subprocess
import urllib.parse

PORT = 8080

class CommandHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/cmd?"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            command = params.get("command", [""])[0]
            
            if command:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                except subprocess.CalledProcessError as e:
                    output = e.output
            else:
                output = "No command received."
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<pre>{output}</pre>".encode())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = """
                <html>
                <body>
                    <h2>Ejecutar comando Bash</h2>
                    <form action="/cmd" method="get">
                        <input type="text" name="command" />
                        <input type="submit" value="Ejecutar" />
                    </form>
                </body>
                </html>
            """
            self.wfile.write(html_content.encode())

with socketserver.TCPServer(("", PORT), CommandHandler) as httpd:
    print(f"Servidor iniciado en el puerto {PORT}")
    httpd.serve_forever()
