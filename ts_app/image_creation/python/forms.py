from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length


class image_save_load(Form):
    """
    Form for saving or loading an image.

    Attributes:
    - imageName (StringField): Input field for the name of the image.
        Validators:
            - DataRequired: Ensures that the field is not empty.
            - Length: Validates the length of the input (between 4 and 25 characters).
    - save (SubmitField): Button for saving the image.
    """

    imageName = StringField("ImageName", [DataRequired(), Length(min=4, max=25)])
    save = SubmitField("Save Image")


class ts_image_form(FlaskForm):
    """
    Form for generating a time-series plot image.

    Attributes:
    - image_title (StringField): Input field for the title of the plot.
    - xlabel (StringField): Input field for the label of the x-axis.
    - ylabel (StringField): Input field for the label of the y-axis.
    - line_color (SelectField): Dropdown menu for selecting the color of the plot line.
    - submit (SubmitField): Button for generating and displaying the plot image.
    """

    image_title = StringField(
        label="Plot Title", validators=[InputRequired()], default="Time Series"
    )
    xlabel = StringField(label="X label", validators=[InputRequired()], default="Date")
    ylabel = StringField(
        label="Y label", validators=[InputRequired()], default="Intresting variable"
    )
    line_color = SelectField(
        label="Line Color",
        validators=[InputRequired()],
        choices=[("red", "Red"), ("blue", "Blue")],
    )
    submit = SubmitField("Show Image", id="draw_image_button")
