from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, email_validator, EqualTo

vakken = [("Geen", "Geen"),("Engels", "Engels"),("Nederlands", "Nederlands"),("Wiskunde A", "Wiskunde A"),("Wiskunde B", "Wiskunde B"),("Wiskunde C", "Wiskunde C"),("Wisku>
("KUA/ KUBV", "KUA/ KUBV"),("L.O.", "LO"),("MAW", "MAW"),("Maatschappijleer", "Maatschappijleer"),("Natuurkunde", "Natuurkunde"),("O&O", "O&O"),("Scheikunde", "Scheikunde">

class ZoekenForm(FlaskForm):
    klas = SelectField('klas: ', choices=["4V", "5V", "6V", "3H", "4H", "5H"], validators=[DataRequired()])
    vak1 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak2 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak3 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak4 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak5 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak6 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak7 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak8 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak9 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak10 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak11 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak12 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak13 = SelectField('', choices=vakken, validators=[DataRequired()])
    vak14 = SelectField('', choices=vakken, validators=[DataRequired()])
    submit = SubmitField('gekozen')

class KlassenForm(FlaskForm):
    klas = SelectField('klas: ', choices=["4V", "5V", "6V", "3H", "4H", "5H"], validators=[DataRequired()])
    submit = SubmitField('Bevestig klas')
    submit2 = SubmitField('kies vakken')

class VolgendeWeekForm(FlaskForm):
    vorige = SubmitField('vorige')
    volgende = SubmitField('volgende')

class SaveForm(FlaskForm):
    save = SubmitField('opnieuw invullen')
