import cn2an
import argparse
import json
from http import server
from urllib.parse import urlparse, parse_qs


class MyHTTPRequestHandler(server.BaseHTTPRequestHandler):
    def go_cn2an(self, func, args):
        result = {"output": "", "msg": "转化成功"}
        try:
            result["output"] = str(func(**args))
        except ValueError as e:
            result["msg"] = str(e)
        except TypeError as e:
            result["msg"] = "参数错误"
        return result

    def get_req_line(self):
        requestline = str(self.raw_requestline, "utf-8")
        url = requestline.split()[1]
        url = urlparse(url)
        path = url.path[1:]
        print(path)
        args = parse_qs(url.query)
        return path, args

    def set_res_(self, code: int, msg: str):
        self.send_response(code)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(msg, ensure_ascii=False).encode())

    def do_GET(self):
        path, args = self.get_req_line()
        functions = ["cn2an", "an2cn", "transform"]

        if path not in functions:
            self.send_error(404, "Not Found")
            return

        for i in args:
            args[i] = str(args[i][0])

        if "text" not in args:
            self.set_res_(200, {"output": "", "msg": "缺少参数 text"})

        args["inputs"] = args.pop("text")
        if path == functions[2]:
            if "mode" in args:
                args["method"] = args.pop("mode")
            if "direct" in args:
                direct = args["direct"]
                if direct == "0" or direct.lower() == "false":
                    args["direct"] = False
                else:
                    args["direct"] = True

        result = self.go_cn2an(getattr(cn2an, path), args)
        self.set_res_(200, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple HTTP server for cn2an")
    parser.add_argument("port", default=11233, type=int, help="Port number", nargs="?")
    parser.add_argument("-b", "--bind", default="localhost", help="Host")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.2")
    args = parser.parse_args()

    server_instance = server.HTTPServer((args.bind, args.port), MyHTTPRequestHandler)
    print(f"Server running at http://{args.bind}:{args.port}")

    try:
        server_instance.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        server_instance.shutdown()
