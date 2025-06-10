from flask import (
    Blueprint, render_template, request, flash
)
from werkzeug.utils import secure_filename
import os


upload_bp = Blueprint('upload', __name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'the_file' not in request.files:
            return "no file provided"
        
        f = request.files['the_file']
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        f.save(fr'{UPLOAD_FOLDER}/{secure_filename(f.filename)}')
        flash('File uploaded successfully')
        return "File uploaded successfully"

    else:
        return render_template('upload/upload.html')