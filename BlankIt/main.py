from flask import Flask, render_template, request, redirect, url_for, flash
import random
import os
from werkzeug.utils import secure_filename
from verify import readTextFile, read
from fill_in_blank import create_question
app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
FILENAME = ""

# filename = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/')
# def blankit():
#     return render_template('UI3.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("I am here")
        # check if the post request has the file part
        if 'file' not in request.files:
            print("bad")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print("bad")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            # return render_template("SecondUI.html")
            print("im here")
            return redirect(url_for('question', filename=filename))
    return render_template("UI3.html")

@app.route('/question/<string:filename>', methods=['GET', 'POST'])
def question(filename): 
  if request.method == 'POST': 

    return redirect(url_for('upload_file'))

  FILENAME = filename
  if filename.endswith(".pdf"): 
    text = read(filename)
  else: 
    text = readTextFile(filename)
  Q = [create_question(text)[0]]
  print(Q)
  return render_template('SecondUI.html', data=Q)


# @app.route('/')
# def change_name(new_text):
#   return render_template('SecondUI.html', question = new_text)
#change_name('''The _____________ is the powerhouse of the cell.''')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'pdf-file' not in request.files:
#             flash('No pdf file')
#             return redirect(request.url)
#         pdf_file = request.files['pdf-file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if img_file.filename == '':
#             flash('No image file selected')
#             return redirect(request.url)
#         if pdf_file.filename == '':
#             flash('No pdf file selected')
#             return redirect(request.url)
#         if img_file and allowed_file(img_file.filename):
#             filename = secure_filename(img_file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "\image" , filename))
#         if pdf_file and allowed_file(pdf_file.filename):
#             filename = secure_filename(pdf_file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "\pdf" , filename))
#         return redirect(url_for('uploads'))
#     return render_template('UI2.html')

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=3000  # Randomly select the port the machine hosts on.
	)