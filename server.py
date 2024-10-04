from flask import Flask, request, redirect, url_for, jsonify, send_file
import datetime
import math
import os
import model_generator

MAX_MODELS_ON_DISK = 100

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("static", filename="index.html"))


@app.route("/generate", methods=["POST"])
def generate():
    delete_old_files()

    top_left = parse_coords(request.form.get("top_left"))
    bottom_right = parse_coords(request.form.get("bottom_right"))
    points = int(request.form.get("points"))
    api = request.form.get("api")
    show_points = request.form.get("show_points")

    if top_left and bottom_right:
        try:
            points_per_axis = round(math.sqrt(float(points)))
            id = model_generator.generate(
                "static", top_left, bottom_right, points_per_axis, points_per_axis, show_points, api
            )
            return jsonify({"id": id}), {"Content-Type": "application/json"}
        except Exception as e:
            return jsonify(f"Error: {e}"), 500, {"Content-Type": "application/json"}
    else:
        return jsonify("Invalid coordinates"), 400, {"Content-Type": "application/json"}


@app.route("/preview", methods=["GET"])
def preview():
    try:
        id = request.args.get("id")
        filename = f"{id}.html"
        return redirect(url_for("static", filename=os.path.join("models", filename)))
    except Exception as e:
        return jsonify(f"Error: {e}"), 500, {"Content-Type": "application/json"}


@app.route("/download", methods=["GET"])
def download():
    try:
        id = request.args.get("id")
        path = os.path.join("static", "csv", f"{id}.csv")
        return send_file(path, mimetype="text/csv", download_name="terrain.csv", as_attachment=True)
    except Exception as e:
        return jsonify(f"Error: {e}"), 500, {"Content-Type": "application/json"}


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("static", filename="404.html"))


@app.errorhandler(500)
def page_not_found(e):
    return redirect(url_for("static", filename="500.html"))


def parse_coords(input):
    coords = list(map(float, input.split(",")))
    return (coords[0], coords[1])


def delete_old_files():
    delete_old_model_files(os.path.join("static", "models"), ".html")
    delete_old_model_files(os.path.join("static", "csv"), ".csv")


def delete_old_model_files(dir, ext):
    files = [os.path.join(dir, filename) for filename in os.listdir(dir) if filename.endswith(ext)]
    files.sort(key=lambda file: datetime.datetime.fromtimestamp(os.path.getmtime(file)))
    while len(files) >= MAX_MODELS_ON_DISK:
        try:
            os.remove(files.pop(0))
        except:
            pass


if __name__ == "__main__":
    app.run(debug=True)
