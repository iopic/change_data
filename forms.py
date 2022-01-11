from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email


class DocumentUploadForm(FlaskForm):
    document = FileField('Document', validators=[FileRequired(), FileAllowed(['csv'], 'CSV Document only!')])
    result_path = StringField(label='user_path',description='where_to_save')
    #submit = SubmitField('Submit bia')
