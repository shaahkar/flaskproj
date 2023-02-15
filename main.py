from flask import Flask, render_template, redirect, url_for, request, Response
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from flask_sqlalchemy import SQLAlchemy
import os
import subprocess

# from db import db_init, db

from db_database import db, db_init

from models import Img

UPLOAD_FOLDER = 'uploads/images'
IMAGE_FOLDER ='/home/dev/flaskproj/uploads/images'
HOME_FOLDER = '/home/dev/flaskproj'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['HOME_FOLDER'] = HOME_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing the database.
db_init(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

directory_location=os.path.join(app.config['UPLOAD_FOLDER'])

@app.route("/")
@app.route("/home")
def start():
    print("hjhkhjk")
    all_data = Img.query.all()
    return render_template("index.html", current_working_directory=os.getcwd(),
    file_list=subprocess.check_output('ls', shell=True).decode('utf-8').split('\n'),
    directory_location=os.path.join(app.config['UPLOAD_FOLDER']),
    home_location=os.path.join(app.config['HOME_FOLDER']),
    file_query=all_data)




# Handle 'cd' command
@app.route('/cd')
def cd():
    #run level up command
    os.chdir(request.args.get('path'))
    print("check")
    #redirect to file manager 
    return redirect("/")


@app.route("/upload")
def files():
    return render_template("upload.html", directory_location=os.path.join(app.config['UPLOAD_FOLDER']),
    file_list=subprocess.check_output('ls', shell=True).decode('utf-8').split('\n'))
### Result checker HTML page 

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
       
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            final_location = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            mimetype = file.mimetype
            img = Img(mimetype=mimetype, name=filename, location=final_location)
            db.session.add(img)
            db.session.commit()
            #save file to the UPLOAD_FOLDER
            file.stream.seek(0)
            # print(app.config['UPLOAD_FOLDER'])
          
            file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))
            all_data = Img.query.all()
            return render_template("index.html", current_working_directory=os.getcwd(),
            file_list=subprocess.check_output('ls', shell=True).decode('utf-8').split('\n'),
            directory_location=os.path.join(app.config['UPLOAD_FOLDER']),
            home_location=os.path.join(app.config['HOME_FOLDER']),
            file_query=all_data)
    return 'ho gaya '

@app.route('/image_upload')
def imagePage():    
    return render_template('image_page.html', home_location=os.path.join(app.config['HOME_FOLDER']))



@app.route('/images', methods=['POST'])
def image_upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400
    
    filename = secure_filename(pic.filename)
    # mimetype = pic.mimetype

    # img = Img(img=pic.read(), mimetype=mimetype, name=filename, location=)
    # db.session.add(img)
    # db.session.commit()

    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # return render_template('index.html', home_location=os.path.join(app.config['HOME_FOLDER']))
    return redirect("/cd?path=" + directory_location)
    # return 'Img has been uploaded, 200'

@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
# if __name__ == '__main__':
#     print("here")
#     app.init_db(app)
#     app.run(debug=True)


@app.route('/webcam')
def webcam():


    return(render_template('webcam.html'))