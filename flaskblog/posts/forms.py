from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    travel_or_explore = BooleanField('Travel/Explore(tick if explore)')
    content = TextAreaField('Content', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    picture = FileField('Add Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
