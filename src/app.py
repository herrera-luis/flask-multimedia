from flask import Flask, render_template, flash
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobServiceClient
from models import Multimedia, UploadForm, init_db, db, get_blob_url_with_sas
from logs import configure_logger 
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = host=os.getenv('AZURE_STORAGE_SECRET_KEY')
app.config['AZURE_STORAGE_CONNECTION_STRING'] = host=os.getenv('AZURE_STORAGE_CONNECTION_STRING')
app.config['AZURE_CONTAINER_NAME'] = host=os.getenv('AZURE_CONTAINER_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = host=os.getenv('DATABASE_URL')
init_db(app)  # Initialize db with the Flask app
configure_logger(app)  # Configure logger with the Flask app

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    blob_service_client = BlobServiceClient.from_connection_string(app.config['AZURE_STORAGE_CONNECTION_STRING'])
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        blob_client = blob_service_client.get_blob_client(app.config['AZURE_CONTAINER_NAME'], filename)

        try:
            blob_client.upload_blob(f)
            multimedia = Multimedia(name=form.name.data, filename=filename)
            db.session.add(multimedia)
            db.session.commit()
            app.logger.info("New multimedia file uploaded")
            msg = 'File uploaded successfully'
            flash(msg, 'success')
        except Exception as e:
            app.logger.error(e)
            msg = 'Failed to upload file'
            flash(msg, 'danger')

    multimedia_records = Multimedia.query.all()
    multimedia_urls = [
        {
            'name': record.name,
            'url': get_blob_url_with_sas(blob_service_client, app.config['AZURE_CONTAINER_NAME'], record.filename)
        }
        for record in multimedia_records
    ]

    return render_template('upload.html', form=form, multimedia_urls=multimedia_urls)

if __name__ == '__main__':
    app.run(debug=True)