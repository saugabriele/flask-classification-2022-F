from app import app
from flask import render_template
from app.forms.classification_form import ClassificationForm
from config import Configuration

conf = Configuration()


@app.route('/upload_image', methods=['GET', 'POST'])
def update_image():
    """API for upload an image and then start a
    classification job. Returns the output scores
    from the model."""
    form = ClassificationForm()
    return render_template('classification_upload_select.html', form=form)
