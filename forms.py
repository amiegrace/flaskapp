from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import InputRequired, EqualTo

class ReviewForm(FlaskForm):
    chocolate = StringField("Chocolate Purchased:")
    review = StringField("What are your thoughts?:")
    submit = SubmitField("Submit")

class SuggestionForm(FlaskForm):
    suggestion = StringField("Suggest our next big creation:")
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("User id:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class QuizForm(FlaskForm):
    first_question = RadioField(
        label="Do you have a sweet tooth? ",
        choices=[
            ("yes", "Yes"),
            ("not really", "not really"),
            ("no", "No/Unknown")
            ],
        default = "yes")
    second_question = RadioField( 
        label="Do you prefer sweet or savoury? ",
        choices=[
            ("sweet", "Sweet"),
            ("savoury", "Savoury"),
            ("neither", "Neither/Unknown")
            ],
        default = "sweet")
    third_question = RadioField( 
        label="How often do you eat chocolate? ",
        choices=[
            ("everyday", "Everyday"),
            ("often", "Often"),
            ("never", "Never")
            ],
        default = "everyday")
    submit = SubmitField("Submit")

class VoteForm(FlaskForm):
    vote = RadioField(
        label="Whats our most popular chocolate? ",
        choices=[
                ("milk", "Milk"),
                ("white", "White"),
                ("dark", "Dark")
                ],
        default = "milk")
    submit = SubmitField("Submit")

class GameForm(FlaskForm):
    chocolate = SelectField("What is our most popular chocolate?",
        choices = [
                ("milk", "Milk"),
                ("white", "White"),
                ("dark", "Dark")
                ],
        validators=[InputRequired()])
    submit = SubmitField("Submit")
   


