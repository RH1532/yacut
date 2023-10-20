from flask import flash, render_template, request, redirect

from . import app
from .forms import URLForm
from .models import URLMap
from .constants import SHORT_URL_READY_MESSAGE


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        new_url, error_message = URLMap.create_short_url(original_link, custom_id)
        if error_message:
            flash(error_message)
        else:
            flash(SHORT_URL_READY_MESSAGE)
            flash(request.host_url + new_url.short)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)
