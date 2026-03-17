from controller.base_handler import BaseHandler
from http.server import HTTPServer, BaseHTTPRequestHandler


class CurrencyHTTPServer(HTTPServer):
    def __init__(self, host, port):
        super().__init__((host, port), BaseHandler)


def main():
    host = "localhost"
    port = 8000
    print(f"Сервер запущен на http://{host}:{port}")

    server = CurrencyHTTPServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
        server.shutdown()
        server.server_close()
    except Exception as e:
        print(f"Ошибка сервера: {e}")


if __name__ == "__main__":
    main()
