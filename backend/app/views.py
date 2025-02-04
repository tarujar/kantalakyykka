from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import YourFormClass

@app.route('/your_form', methods=['GET', 'POST'])
def your_form_view():
    form = YourFormClass()
    if form.validate_on_submit():
        # Process form data
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('form_template.html', form=form)
