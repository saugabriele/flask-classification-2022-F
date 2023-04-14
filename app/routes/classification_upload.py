import redis
from flask import render_template, request, redirect, flash
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import save_image, allowed_file, classify_image
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

        model_id = form.model.data
        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": filename
            })
            task = q.enqueue_job(job)
        return render_template("classification_upload_output_queue.html", image_id=filename, jobID=task.get_id())
    return render_template("classification_upload_select.html", form=form)