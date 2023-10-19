from flask import flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    url_map = URLMap()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = url_map.get_unique_short_id()
        existing_url = url_map.query.filter_by(original=original_link).first()
        if existing_url:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        short_id = URLMap(
            original=original_link,
            short=custom_id
        )
        db.session.add(short_id)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        flash(f'http://localhost/{short_id.short}')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)
