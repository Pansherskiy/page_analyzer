from datetime import date
from page_analyzer.setting import SECRET_KEY
from page_analyzer.url_validator import validate_url
from page_analyzer.db_management import (
    create_tables,
    db_connect,
    db_query,
    db_select_query,
)
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
    'url_exist': ('Страница уже существует', 'primary'),
    'add_url': ('Страница успешно добавлена', 'success'),
    'invalid_url': ('Некорректный URL', 'danger')
}


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
db_conn = db_connect()
create_tables(db_conn)


@app.route('/')
def index():
    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)


@app.route('/urls/<id>')
def url_added(id):
    messages = get_flashed_messages()
    data = db_select_query(db_conn,
                           f"SELECT name, created_at FROM urls"
                           f" WHERE id = {id};")
    name, created_at = data
    return render_template('url_page.html',
                           id=id,
                           url_name=name,
                           created_at=created_at,
                           messages=messages,
                           )


@app.route('/urls', methods=["GET", "POST"])
def urls_page():
    if request.method == 'GET':
        urls = db_select_query(db_conn, "SELECT * FROM urls;")
        messages = get_flashed_messages()
        return render_template('urls.html',
                               messages=messages,
                               urls=urls)
    if request.method == 'POST':
        url = request.form.get('url')
        urls = db_select_query(db_conn, "SELECT name FROM urls;")
        errors = validate_url(url)
        if errors:
            for error in errors:
                flash(FLASH_MESSAGES[error])
            return redirect(url_for('index'))
        if urls and url in urls:
            flash(FLASH_MESSAGES['url_exist'])
            url_id = db_select_query(db_conn, f"SELECT id FROM urls "
                                              f"WHERE name = '{url}'")
            return redirect(url_for('url_added', id=url_id))
        else:
            flash(FLASH_MESSAGES['add_url'])
            db_query(db_conn,
                     f"INSERT INTO urls(name, created_at) VALUES "
                     f"('{url}', '{date.today()}');")
            url_id = db_select_query(db_conn, f"SELECT id FROM urls "
                                              f"WHERE name = '{url}'")
            return redirect(url_for('url_added', id=url_id))


@app.errorhandler(404)
def not_found(_):
    return render_template('not_found404.html'), 404
