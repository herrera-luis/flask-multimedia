from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta


db = SQLAlchemy()

def init_db(app):
    db.init_app(app)


class Multimedia(db.Model):
    __tablename__ = 'multimedia'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    
class UploadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    file = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Upload')


def get_blob_url_with_sas(blob_service_client, container_name, blob_name):
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
    return blob_url