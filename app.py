import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from src.inference.predict_image import predict_image  # your image predictor
from src.inference.alert_logic import get_alert  # alert logic without SMS for now
import cv2

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4", "avi", "mov"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_video(video_path):
    """
    Predict video status by running the image model on frames.
    Returns the majority label and average confidence.
    """
    cap = cv2.VideoCapture(video_path)
    frame_labels = []
    frame_confidences = []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        return "empty", 0.0

    frame_skip = max(1, total_frames // 30)  # sample ~30 frames

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_skip == 0:
            # Save frame temporarily
            tmp_path = "temp_frame.jpg"
            cv2.imwrite(tmp_path, frame)
            result = predict_image(tmp_path)
            frame_labels.append(result["label"])
            frame_confidences.append(result["confidence"])
            os.remove(tmp_path)
        frame_idx += 1

    cap.release()

    # Majority vote
    from collections import Counter
    label_counts = Counter(frame_labels)
    majority_label = label_counts.most_common(1)[0][0]

    # Average confidence for that label
    confs = [c for l, c in zip(frame_labels, frame_confidences) if l == majority_label]
    avg_conf = sum(confs) / len(confs) if confs else 0.0

    return majority_label, round(avg_conf, 2)


@app.route("/", methods=["GET", "POST"])
def index():
    status = ""
    confidence = ""
    alert_msg = ""
    filename = None
    file_url = ""
    file_type = ""

    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "" or not allowed_file(file.filename):
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        ext = filename.rsplit(".", 1)[1].lower()
        if ext in {"png", "jpg", "jpeg"}:
            label_conf = predict_image(file_path)
            label = label_conf["label"]
            confidence = round(label_conf["confidence"], 2)
            file_type = "image"
        else:  # video
            label, confidence = predict_video(file_path)
            file_type = "video"

        status = label
        alert_msg = get_alert(label)  # returns your alert string (no SMS for now)
        file_url = f"/{app.config['UPLOAD_FOLDER']}/{filename}"

    return render_template(
        "index.html",
        status=status,
        confidence=confidence,
        alert=alert_msg,
        filename=filename,
        file_url=file_url,
        file_type=file_type
    )


if __name__ == "__main__":
    app.run(debug=True)
