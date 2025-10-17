from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "dev-secret"
UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/preview", methods=["POST"])
def preview():
    link_text = request.form.get("link_text", "").strip() or "Example link"
    link_url  = request.form.get("link_url", "").strip()  or "https://www.example.com"
    img_url_input = request.form.get("image_url", "").strip()

    image_url = None
    if img_url_input:
        image_url = img_url_input

    if not image_url and "image_file" in request.files:
        file = request.files["image_file"]
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Unsupported file type. Allowed: png, jpg, jpeg, gif, webp")
                return redirect(url_for("index"))
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            image_url = url_for("static", filename=f"uploads/{filename}")

    if not image_url:
        flash("Please provide an image URL or upload an image file.")
        return redirect(url_for("index"))

    return render_template("result.html", link_text=link_text, link_url=link_url, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True, port=5004)
