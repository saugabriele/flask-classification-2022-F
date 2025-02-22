from app import app
from flask import render_template
from app.forms.histogram_form import HistogramForm
from ml.classification_utils import create_histogram, check_path
from config import Configuration


conf = Configuration()


@app.route('/histograms', methods=['GET', 'POST'])
def histograms():
    """API for selecting an image through a specific id
    and then compute the histogram. Returns as output
    the histogram."""
    form = HistogramForm()
    if form.validate_on_submit():
        image_id = form.image.data

        check_path(conf.histogram_path)
        hist_id = create_histogram(image_id, conf.histogram_path)

        return render_template('histogram_output.html', image_id=image_id, histogram=hist_id)
    return render_template('histogram_selection.html', form=form)
