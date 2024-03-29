from datetime import date
from page_analyzer.setting import SECRET_KEY
from page_analyzer.url_validator import validate_url
from page_analyzer.parser import parse_url, normalize_url
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
)


FLASH_MESSAGES = {
    'empty_url': ('URL обязателен', 'danger'),
    'very_long': ('URL превышает 255 символов', 'danger'),
    'url_exist': ('Страница уже существует', 'primary'),
    'add_url': ('Страница успешно добавлена', 'success'),
    'invalid_url': ('Некорректный URL', 'danger'),
    'url_checked': ('Страница успешно проверена', 'success'),
    'url_check_error': ('Произошла ошибка при проверке', 'danger')
}


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
db_conn = db_connect()
create_tables(db_conn)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls/<id>')
def url_added(id):
    url_data = db_select_query(db_conn,
                               f"SELECT name, created_at FROM urls"
                               f" WHERE id = {id};")
    name, created_at = url_data[0]
    check_data = db_select_query(db_conn,
                                 f"SELECT url_checks.id, url_checks"
                                 f".status_code, url_checks.h1, "
                                 f"url_checks.title, url_checks.description, "
                                 f"url_checks.created_at FROM urls JOIN "
                                 f"url_checks ON urls.id = url_checks.url_id "
                                 f"WHERE urls.id = '{id}'"
                                 f"ORDER BY id DESC;")
    return render_template('url_page.html',
                           id=id,
                           url_name=name,
                           created_at=created_at,
                           checks=check_data
                           )


@app.route('/urls', methods=["GET", "POST"])
def urls_page():
    if request.method == 'GET':
        urls = db_select_query(db_conn, """
        SELECT DISTINCT ON (urls.id)
                urls.id,
                urls.name,
                url_checks.created_at,
                url_checks.status_code
            FROM urls LEFT JOIN url_checks
            ON urls.id = url_checks.url_id
            ORDER BY urls.id DESC, url_checks.created_at DESC""")
        return render_template('urls.html', urls=urls)
    if request.method == 'POST':
        url = request.form.get('url')
        errors = validate_url(url)
        normal_url = normalize_url(url)
        urls = db_select_query(db_conn, "SELECT name FROM urls;")
        if errors:
            for error in errors:
                flash(FLASH_MESSAGES[error])
            return render_template('index.html'), 422
        if urls and normal_url in urls:
            flash(FLASH_MESSAGES['url_exist'])
            url_id = db_select_query(db_conn, f"SELECT id FROM urls "
                                              f"WHERE name = '{normal_url}'")
            return redirect(url_for('url_added', id=url_id))
        else:
            flash(FLASH_MESSAGES['add_url'])
            db_query(db_conn,
                     f"INSERT INTO urls(name, created_at) VALUES "
                     f"('{normal_url}', '{date.today()}');")
            url_id = db_select_query(db_conn, f"SELECT id FROM urls "
                                              f"WHERE name = '{normal_url}'")
            return redirect(url_for('url_added', id=url_id))


@app.post('/urls/<id>/check')
def url_check(id):
    url = db_select_query(db_conn, f"SELECT name FROM urls WHERE id = '{id}'")
    response, h1, title, description = parse_url(url)
    if response == 200:
        db_query(db_conn, f"INSERT INTO url_checks (url_id, status_code, "
                          f"h1, title, description, created_at) VALUES "
                          f"('{id}', '{response}', '{h1}', '{title}', "
                          f"'{description}', '{date.today()}');")
        flash(FLASH_MESSAGES['url_checked'])
    else:
        flash(FLASH_MESSAGES['url_check_error'])
    return redirect(url_for('url_added', id=id))


@app.errorhandler(404)
def not_found(_):
    return render_template('not_found404.html'), 404
