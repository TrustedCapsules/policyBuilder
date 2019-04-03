from flask import Flask, request, send_from_directory, send_file
from http import HTTPStatus

app = Flask(__name__)


@app.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/")
def home():
    return send_file('html/index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


if __name__ == "__main__":
    app.run()
