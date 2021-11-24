from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	video_id = StringField('Youtube Link or Video ID')
	#video = FileField('Upload Video')
	submit = SubmitField('Post')

class ReplyForm(FlaskForm):
	content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Post a reply"})
	submit = SubmitField('Submit')
