from .codes import *
from flask import Flask, request, jsonify, send_file, abort, send_from_directory

app = Flask(__name__)
DOWNLOAD_PATH = "data/"

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')  # Возвращаем файл index.html для главной страницы

def get_file_path(secret):
    """Возвращает путь к файлу, если секретный код существует"""
    if secret in codes:
        return DOWNLOAD_PATH + codes[secret]
    else:
        return False

@app.route("/check_secret", methods=["POST"])
def check_secret():
    """Проверяет, существует ли файл для данного секретного кода"""
    data = request.get_json()
    secret = data.get("secret")

    file_path = get_file_path(secret)
    
    if file_path:
        # Отдаем ссылку на скачивание
        return jsonify({"success": True, "download_url": f"/download/{secret}"})
    
    return jsonify({"success": False, "error": "Файл не найден или код неверный"}), 403

@app.route("/download/<secret>")
def download_file(secret):
    """Отправляет файл, если код верный и файл существует"""
    file_path = get_file_path(secret)

    if file_path:
        return send_file(file_path, as_attachment=True)  # Отдаем файл на скачивание
    
    abort(404, description="Файл не найден")  # Если файла нет — 404 ошибка

if __name__ == "__main__":
    app.run(debug=True)