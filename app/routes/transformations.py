from app import app
from flask import render_template
from app.forms.transformation_form import TransformationForm


@app.route('/transformation', methods=['GET', 'POST'])
def transformations():
    """API to select an image and define transformation parameters
    and then realize the image transformation. Returns as output
    the result of the transformation."""
    form = TransformationForm()
    if form.validate_on_submit():
        pass
    return render_template('transformation_select.html', form=form)