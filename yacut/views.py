from http import HTTPStatus

from flask import abort, flash, render_template, redirect

from . import app
from .forms import URLForm
from .models import URLMap
from .exceptions import InvalidShortNameError, DuplicateShortError


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    original_link = form.original_link.data
    custom_id = form.custom_id.data
    try:
        url_map, short_url = URLMap.create(original_link, custom_id)
    except InvalidShortNameError as e:
        flash(str(e))
        return render_template('index.html', form=form)
    except DuplicateShortError as e:
        flash(str(e))
        return render_template('index.html', form=form)
    return render_template('index.html',
                           form=form,
                           result_url=short_url)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
