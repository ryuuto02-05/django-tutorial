from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/hello":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello, World!")

        elif path == "/calc":
            params = parse_qs(parsed_path.query)
            if "a" in params and "b" in params:
                try:
                    a = int(params["a"][0])
                    b = int(params["b"][0])
                    result = a + b
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(str(result).encode())
                except ValueError:
                    self.send_error(
                        400, "Invalid parameters. 'a' and 'b' must be integers."
                    )
            else:
                self.send_error(
                    400, "Missing parameters. Both 'a' and 'b' are required."
                )

        else:
            self.send_error(404, "Not Found")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
