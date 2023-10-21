from http import HTTPStatus

from flask import abort, flash, render_template, redirect, request

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    custom_id = form.custom_id.data
    try:
        url_map = URLMap.create(original_link, custom_id)
    except Exception as e:
        flash(str(e))
        return render_template('index.html', form=form)
    return render_template('index.html',
                           form=form,
                           result_url=request.url_root + url_map.short)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url = URLMap.get_id(short_id)
    if not url:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original)
