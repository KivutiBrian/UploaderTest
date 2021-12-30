import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDERS")

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
@app.before_first_request
def create_tables():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = UPLOAD_FOLDER + f"/{filename}"

            record = File(file=filepath)
            db.session.add(record)
            db.session.commit()

            print(filepath)

            return redirect(url_for('upload_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''