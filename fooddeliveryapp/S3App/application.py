from flask import Flask, Response, render_template, request, redirect, url_for
from s3_utils import S3Utils
from config import BUCKET, UPLOAD_FOLDER
import os


app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index.html")
    
    
@app.route("/s3ostorage")
def storage():
    items = S3Utils.list_objects_from_bucket(BUCKET)
    return render_template('s3ostorage.html', contents=items)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        
        f = request.files['file']
        if f.filename != '': #ensure that only upload to S3 if a file has been provided
            path = "{}/{}".format(UPLOAD_FOLDER, f.filename)
            f.save(path)
            
            S3Utils.upload_file(BUCKET, path, f.filename)
            
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)  # remove the file from the application (i.e. machine that hosts this application)
        
        return redirect("s3ostorage")



@app.route("/retrieve/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        file_object = S3Utils.get_object(BUCKET, filename)
        return Response(file_object['Body'].read(),
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename={}".format(filename)}
        )
        

if __name__ == '__main__':
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()
