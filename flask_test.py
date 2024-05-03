from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Funktion zum Lesen des Video-Streams der Webcam
def generate_frames():
    camera = cv2.VideoCapture(0)  # Zugriff auf die Standard-Webcam (ID: 0)
    while True:
        success, frame = camera.read()  # Erfolgreiches Lesen des Video-Streams
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)  # Codieren des Frames in das JPEG-Format
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Flask-Routen definieren
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
