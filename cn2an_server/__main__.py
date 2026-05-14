import cn2an
import argparse
from http import server
from urllib.parse import urlparse, parse_qs


class MyHTTPRequestHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        requestline = str(self.raw_requestline, "utf-8")
        url = requestline.split()[1]
        url = urlparse(url)
        path = url.path
        if path == "/favicon.ico":
            self.send_error(404, "Not Found")
            return
        args = parse_qs(url.query)
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        if "text" not in args:
            result = f"参数错误：缺少必要参数 text"
            self.send_response(400)
            self.wfile.write(result.encode())
            return
        for i in args:
            args[i] = str(args[i][0])
        text = args["text"]
        if path == "/cn2an":
            mode = args.get("mode", "strict")
            result = str(cn2an.cn2an(text, mode))
        elif path == "/an2cn":
            mode = args.get("mode", "low")
            result = str(cn2an.an2cn(text, mode))
        elif path == "/transform":
            mode = args.get("mode", "cn2an")
            direct = args.get("direct", "false")
            result = str(cn2an.transform(text, mode, direct))
        else:
            self.send_response(404)
            result = "404 Not Found"
        self.wfile.write(result.encode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple HTTP server for cn2an")
    parser.add_argument("port", type=int, help="Port number")
    parser.add_argument("-b", "--bind", default="localhost", help="Host")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    args = parser.parse_args()

    server_instance = server.HTTPServer((args.bind, args.port), MyHTTPRequestHandler)
    print(f"Server running at http://{args.bind}:{args.port}")

    try:
        server_instance.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        server_instance.shutdown()
