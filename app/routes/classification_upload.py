from flask import render_template, request, redirect, flash

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import save_image, allowed_file
from config import Configuration

conf = Configuration()


@app.route('/upload_classification', methods=['GET', 'POST'])
def upload_image():
    """API for upload an image and then start a
    classification job. Returns the output scores
    from the model."""
    form = ClassificationForm()

    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        upload_image = request.files.get('file', None)
        filename = upload_image.filename

        if filename == '':
            flash('No selected file')
            return redirect(request.url)

        if upload_image and allowed_file(filename):
            save_image(upload_image)
        else:
            flash("The uploaded image is not valid, you should select another image.")
            return redirect(request.url)
    return render_template("classification_upload_select.html", form=form)