from app import app
from flask import render_template
from app.forms.transformation_form import TransformationForm
from ml.classification_utils import image_transformation


@app.route('/transformation', methods=['GET', 'POST'])
def transformations():
    """API to select an image and define transformation parameters
    and then realize the image transformation. Returns as output
    the result of the transformation."""
    form = TransformationForm()
    if form.validate_on_submit():
        image_id = form.image.data
        color_en = form.color.data
        contrast_en = form.contrast.data
        brightness_en = form.brightness.data
        sharpness_en = form.sharpness.data

        transformation_path = 'app/static/Transformations'
        transformation_id = image_transformation(image_id, transformation_path, color_en, contrast_en,
                                                 brightness_en, sharpness_en)
        return render_template('transformation_output.html', image_id=image_id, transformation_id=transformation_id)
    return render_template('transformation_select.html', form=form)