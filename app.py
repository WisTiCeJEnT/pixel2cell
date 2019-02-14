import os
from flask import Flask, request, redirect, url_for, send_from_directory, send_file
from werkzeug import secure_filename
import px2cell

UPLOAD_FOLDER = './Uploaded_data/'
ALLOWED_EXTENSIONS = set(['txt','png','jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def root():
    return "Working"

def download(filename):
    #uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_file(UPLOAD_FOLDER+filename, mimetype='image/jpg',as_attachment=True)
    #send_from_directory(UPLOAD_FOLDER,filename)
    #(directory=uploads, filename=filename)

@app.route("/uploader/", methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        try:
            file = request.files['file']
        except:
            return "File Error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = px2cell.px2cell(filename)
            download(filename)
            return "Uploaded"#redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
