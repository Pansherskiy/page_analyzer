from page_analyzer.setting import SECRET_KEY
from page_analyzer.url_validator import validate_url
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    get_flashed_messages
)


FLASH_MESSAGES = {
    'empty_url': ('URL обязателен', 'danger'),
    'very_long': ('URL превышает 255 символов', 'danger'),
    'url_exist': ("Страница уже существует", 'primary'),
    'add_url': ("Страница успешно добавлена", 'success'),
    'invalid_url': ("Некорректный URL", 'danger')
}


app = Flask(__name__)


app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)


@app.route('/urls', methods=["GET", "POST"])
def urls():
    if request.method == 'GET':
        return render_template('urls.html')
    if request.method == 'POST':
        url = request.form.get('url')
        errors = validate_url(url)
        if errors:
            for error in errors:
                flash(FLASH_MESSAGES[error])
            return redirect(url_for('index'))
        return redirect(url_for('urls'))


@app.errorhandler(404)
def not_found(_):
    return render_template('not_found404.html'), 404
