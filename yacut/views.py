from http import HTTPStatus

from flask import abort, flash, render_template, redirect, url_for

from . import app
from .forms import URLForm
from .models import URLMap
from .constants import SHORT_URL_READY_MESSAGE


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    custom_id = form.custom_id.data
    try:
        url_map = URLMap.create_short_url(original_link, custom_id)
        flash(SHORT_URL_READY_MESSAGE)
    except Exception as e:
        flash(str(e))
        return render_template('index.html', form=form)
    return render_template('index.html',
                           form=form,
                           result_url=url_for('index_view', _external=True) + url_map.short)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url = URLMap.get_short_id(short_id)
    if not url:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
