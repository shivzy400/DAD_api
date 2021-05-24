from flask import Flask, render_template , redirect , url_for , Response , flash , request
from camera import VideoCamera
from forms import SettingsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a5c5cbdf1428d6fe3f40a3114eea2ac4'

@app.route('/')
@app.route('/home')
def home() :

    return render_template('home.html' , title='Home Page')

@app.route('/detection')
def detection() :

    return render_template('detection.html' , title='Detection')

def gen(camera):
    while True:
        #get camera frame
        frame , message = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
@app.route('/video_feed')
def video_feed():
    videocam = VideoCamera()
    return Response(gen(videocam) ,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/settings' , methods=['GET' , 'POST']) 
def settings() :

    setting_form = SettingsForm()
    if setting_form.validate_on_submit() :

        flash('Changes Saved Successfully' , 'success')
        return redirect(url_for('home'))

    return render_template('settings.html' , form = setting_form , title = 'Settings')

if __name__ == '__main__' :

    app.run(debug = True)