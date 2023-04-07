from app import app
from flask import render_template
from app.forms.histogram_form import HistogramForm


@app.route('/histograms', methods=['GET', 'POST'])
def histograms():
    """API for selecting an image through a specific id
    and then compute the histogram. Returns as output
    the histogram."""
    form = HistogramForm()
    if form.validate_on_submit():
        pass
    return render_template('histogram_selection.html', form=form)
