from flask import Flask, flash, redirect, request, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not 'file' in request.files:
            return {"status": "error", "message": "no_file_object"}

        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {"status": "error", "message": "no_selected_file"}

        # create a secure filename
        filename = secure_filename(file.filename)

        # save this file to the uploads folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return {"status": "processing"}
    elif request.method == 'GET':
        return '''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Upload new File</title>
                </head>
                <body>
                    <h1>Upload new File</h1>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file">
                        <input type="submit" value="Upload">
                    </form>
                </body>
            </html>
        '''

if __name__ == "__main__":
    host = "127.0.0.1"
    port = os.environ.get("PORT", 5000)

    app.run(host, port)
