from flask import Flask, render_template_string, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg://site_10_user:wclx7Y4cJANDlTgXNRGjPgo4xD01x0XF"
    "@dpg-d6o44rkr85hc73dihsbg-a.virginia-postgres.render.com/site_10"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ------------------ МОДЕЛЬ ------------------
class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    speciality = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    form = db.Column(db.String(50), nullable=False)


# ------------------ ДАННЫЕ ------------------
DESIRED_COLLEGES = [
    {"name": "Колледж предпринимательства", "speciality": "Предпринимательство и бизнес", "region": "Москва", "form": "Очная"},
    {"name": "Колледж цифровых технологий", "speciality": "Информационные системы и программирование", "region": "Москва", "form": "Очная"},
    {"name": "Миэт", "speciality": "Электроника и IT", "region": "Москва", "form": "Очная"},
    {"name": "КМТ", "speciality": "Транспорт и логистика", "region": "Москва", "form": "Очная"},
    {"name": "Медицинский колледж номер 7", "speciality": "Сестринское дело", "region": "Москва", "form": "Очная"},
    {"name": "Колледж связи номер 54", "speciality": "Сети и телекоммуникации", "region": "Москва", "form": "Очная"},
    {"name": "Синергия", "speciality": "Экономика и управление", "region": "Москва", "form": "Очно-заочная"},
    {"name": "Политехнический колледж номер 8", "speciality": "Технологии машиностроения", "region": "Москва", "form": "Очная"},
    {"name": "МГТУ-МАСИ", "speciality": "Строительство и архитектура", "region": "Москва", "form": "Очная"},
    {"name": "Колледж культуры и спорта", "speciality": "Культура, спорт и туризм", "region": "Москва", "form": "Очная"},
]

COLLEGE_LINKS = {
    "синергия": "https://synergy.ru/",
    "миэт": "https://www.miet.ru/",
    "кмт": "https://kmt.moscow/",
    "медицинский колледж номер 7": "https://mk7.mskobr.ru/",
    "колледж предпринимательства": "https://kp11.mskobr.ru/",
    "колледж связи номер 54": "https://www.ks54.ru/",
    "колледж цифровых технологий": "https://topitcollege.ru/",
    "политехнический колледж номер 8": "https://pk-8.mskobr.ru/",
    "мгту-маси": "https://masi.ru/",
    "колледж культуры и спорта": "https://mos.college/",
}


def get_college_link(name: str) -> str | None:
    return COLLEGE_LINKS.get((name or "").strip().lower())


def sync_colleges_to_desired_list():
    existing = College.query.all()
    existing_names = {c.name.strip().lower() for c in existing}
    desired_names = {c["name"].strip().lower() for c in DESIRED_COLLEGES}

    if existing_names == desired_names and len(existing) == len(DESIRED_COLLEGES):
        return

    College.query.delete()
    db.session.commit()

    db.session.add_all([
        College(
            name=item["name"],
            speciality=item["speciality"],
            region=item["region"],
            form=item["form"],
        )
        for item in DESIRED_COLLEGES
    ])
    db.session.commit()


with app.app_context():
    db.create_all()
    sync_colleges_to_desired_list()


# ------------------ КАРТИНКИ ДЛЯ КАРТОЧЕК ------------------
def image_for_speciality(s: str) -> str:
    s = (s or "").lower()

    if "программ" in s or "it" in s or "айти" in s or "информац" in s:
        return "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=60"
    if "электрон" in s:
        return "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?auto=format&fit=crop&w=1600&q=60"
    if "логист" in s or "транспорт" in s:
        return "https://images.unsplash.com/photo-1529070538774-1843cb3265df?auto=format&fit=crop&w=1600&q=60"
    if "сестрин" in s or "мед" in s:
        return "https://images.unsplash.com/photo-1580281657527-47f249e8f6c1?auto=format&fit=crop&w=1600&q=60"
    if "сети" in s or "телеком" in s or "связ" in s:
        return "https://images.unsplash.com/photo-1551703599-6b3e8379aa8f?auto=format&fit=crop&w=1600&q=60"
    if "управлен" in s or "эконом" in s or "бизнес" in s or "предприним" in s:
        return "https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=1600&q=60"
    if "машино" in s or "технолог" in s:
        return "https://images.unsplash.com/photo-1581092160607-ee67f55b7b2a?auto=format&fit=crop&w=1600&q=60"
    if "стро" in s or "архит" in s:
        return "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=60"
    if "культур" in s or "спорт" in s or "туризм" in s:
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=60"

    return "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1600&q=60"



def description_for_speciality(s: str) -> str:
    s = (s or "").lower()

    if "программ" in s:
        return "Изучают разработку приложений, базы данных и основы тестирования. Подходит тем, кто любит логику и технологии. В колледже есть такие направления, как: изучение языков программирования, основы работы с БД и многие другие. Стоимость: 150000 за семестр"

    if "it" in s or "электро" in s or "электрон" in s:
        return "Работа с электроникой, датчиками и автоматикой. Подходит тем, кто хочет собирать и программировать устройства. В колледже есть такие направления, как: изучение компонентов электроники, основы соедиения компонентов и многие другие. Стоимость: 154000 за семестр"

    if "сети" in s or "телеком" in s or "связ" in s:
        return "Настройка сетей, оборудования и связи. Подходит тем, кто интересуется интернетом и инфраструктурой. В колледже есть такие направления, как: работа с сетями, основы подключения кабелей интернет и многие другие. Стоимость: 152000 за семестр"

    if "дизайн" in s or "граф" in s:
        return "Дизайн, композиция, работа в графических редакторах. Подходит творческим ребятам. В колледже есть такие направления, как: базовые навыки работы в редакторах и обучение 3D-дизайну. Стоимость: 90000 за семестр"

    if "архит" in s or "стро" in s:
        return "Основы проектирования и строительства. Подходит тем, кто хочет работать с чертежами и пространством. В колледже есть такие направления, как: основы работы архитектора, основы 3D-моделирования и многие другие. Стоимость: 150000 за семестр"

    if "логист" in s or "транспорт" in s:
       return "Планирование маршрутов, поставок и складов. Подходит тем, кто любит порядок и организацию. В колледже есть такие направления, как: основы построения маршрутов, основы логистики и многие другие. Стоимость: 160000 за семестр"

    if "преподав" in s or "педагог" in s:
        return "Педагогика, практика работы с детьми и методики обучения. Подходит тем, кто любит объяснять и помогать. В колледже есть такие направления, как: основы преподавания, методика оценивания и многие другие. Стоимость: 161000 за семестр"

    if "туризм" in s:
        return "Организация поездок, сервис, коммуникации. Подходит общительным и активным. В колледже есть такие направления, как: основы планирования путешествий, работа экскурсовода и многие другие. Стоимость: 140000 за семестр"

    if "сестрин" in s or "мед" in s:
        return "Уход за пациентами, базовая медицина, практика. Подходит тем, кто хочет помогать людям. В колледже есть такие направления, как: основы проведения операций, педиатрия и многие другие. Стоимость: 151500 за семестр"

    if "эконом" in s or "управлен" in s or "бизнес" in s or "предприним" in s:
        return "Финансы, учёт, основы бизнеса. Подходит тем, кто любит цифры и анализ. В колледже есть такие направления, как: основы работы с деньгами, работа кассира-инкасатора и многие другие. Стоимость: 60000 за семестр"

    return "Описание пока не добавлено."


# ------------------ СТИЛИ ------------------
STYLE = """
<style>
  :root{
    --line: rgba(255,255,255,.14);
    --text: rgba(255,255,255,.94);
    --muted: rgba(255,255,255,.72);
    --shadow: 0 22px 60px rgba(0,0,0,.50);
    --shadow2: 0 10px 30px rgba(0,0,0,.35);
    --a1:#7c5cff;
    --a2:#18d6ff;
  }
  *{ box-sizing:border-box; }
  body{
    margin:0;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
    color: var(--text);
    background:
      radial-gradient(1200px 700px at 12% 10%, rgba(124,92,255,.45), transparent 60%),
      radial-gradient(1000px 700px at 92% 18%, rgba(24,214,255,.32), transparent 55%),
      linear-gradient(180deg, #070a14, #0b1030 55%, #070a14);
    min-height:100vh;
  }
  a{ color:inherit; }
  .container{ max-width: 1180px; margin: 18px auto; padding: 0 16px 34px; }

  .nav{
    position: sticky; top:0; z-index:20;
    backdrop-filter: blur(12px);
    background: rgba(7,10,20,.62);
    border-bottom: 1px solid var(--line);
  }
  .nav-inner{
    max-width: 1180px;
    margin:0 auto;
    padding: 12px 16px;
    display:flex; align-items:center; justify-content:space-between; gap:14px;
  }
  .brand{ display:flex; align-items:center; gap:10px; font-weight: 950; text-decoration:none; }
  .brand-mark{
    width: 36px; height: 36px; border-radius: 14px;
    background: linear-gradient(135deg, var(--a1), var(--a2));
    box-shadow: 0 16px 30px rgba(124,92,255,.22);
  }
  .links{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
  .links a{
    text-decoration:none; padding: 8px 12px; border-radius: 14px;
    border:1px solid transparent; color: var(--muted);
    transition: background .15s ease, border-color .15s ease, transform .15s ease;
  }
  .links a:hover{ border-color: var(--line); background: rgba(255,255,255,.06); color: var(--text); transform: translateY(-1px); }

  .hero{
    border: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255,255,255,.11), rgba(255,255,255,.06));
    box-shadow: var(--shadow);
    border-radius: 22px;
    overflow:hidden;
  }
  .hero-body{ padding: 18px 18px 16px; }
  h1{ margin: 6px 0 10px; font-size: 32px; }
  p{ margin: 0 0 10px; color: var(--muted); line-height: 1.65; }

  .btn{
    display:inline-flex; align-items:center; justify-content:center;
    padding: 11px 14px; border-radius: 16px;
    border: 1px solid rgba(255,255,255,.14);
    background: linear-gradient(135deg, var(--a1), var(--a2));
    color: #070a14; font-weight: 900;
    cursor:pointer; text-decoration:none;
    box-shadow: 0 18px 40px rgba(124,92,255,.20);
  }
  .btn-secondary{ background: rgba(255,255,255,.08); color: var(--text); box-shadow:none; }

  .search-box{ display:flex; gap:10px; flex-wrap:wrap; margin-top: 12px; }
  .input{
    flex: 1 1 320px;
    padding: 12px 12px;
    border-radius: 16px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,.06);
    color: var(--text);
    outline:none;
  }

  .cards{
    margin-top: 16px;
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 14px;
  }
  .card-link{ text-decoration:none; }
  .card{
    border-radius: 20px;
    overflow:hidden;
    background: rgba(255,255,255,.06);
    border: 1px solid var(--line);
    box-shadow: var(--shadow2);
  }
  .card img{ width:100%; height: 155px; object-fit: cover; display:block; }
  .card-body{ padding: 12px 12px 14px; }
  .title{ font-weight: 950; margin: 0 0 8px; font-size: 15px; }
  .meta{ color: var(--muted); font-size: 13px; line-height:1.45; }

  .table-wrap{
    margin-top:14px;
    border-radius: 20px;
    overflow:hidden;
    border:1px solid var(--line);
    background: rgba(255,255,255,.06);
    box-shadow: var(--shadow2);
  }
  table{ width:100%; border-collapse: collapse; }
  thead th{
    background: rgba(7,10,20,.65);
    color: rgba(255,255,255,.92);
    text-align:left;
    padding: 12px;
    border-bottom: 1px solid var(--line);
  }
  tbody td{
    padding: 12px;
    border-bottom: 1px solid rgba(255,255,255,.10);
    color: rgba(255,255,255,.88);
  }

  .note{
    margin-top: 12px;
    padding: 12px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.14);
    background: rgba(255,255,255,.06);
    color: var(--muted);
  }

  .thumbs{ display:flex; gap:12px; flex-wrap:wrap; margin: 12px 0; }
  .thumbs img{ border-radius: 16px; border: 1px solid rgba(255,255,255,.14); box-shadow: var(--shadow2); }

  .top-actions{ display:flex; gap:10px; flex-wrap:wrap; margin-top: 12px; }
  .footer{ margin-top: 14px; color: rgba(255,255,255,.45); font-size: 12px; text-align:center; }
</style>
"""


NAV = """
<div class="nav">
  <div class="nav-inner">
    <a class="brand" href="/">
      <span class="brand-mark"></span>
      <span>Подбор колледжа онлайн</span>
    </a>
    <div class="links">
      <a href="/">Главная</a>
      <a href="/search">Подбор</a>
      <a href="/colleges">Все колледжи</a>
      <a href="/register">Полезные советы</a>
    </div>
  </div>
</div>
"""


# ------------------ ШАБЛОНЫ ------------------
index_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Подбор колледжа</title>
  {{ style|safe }}
</head>
<body>
  {{ nav|safe }}
  <div class="container">
    <div class="hero">
      <div class="hero-body">
        <h1>Подбор колледжа по специальности</h1>
        <p>Привет, будущий студент!  
Ты уже задумываешься о том, куда поступать? Я создал этот сайт, чтобы помочь тебе быстро и легко подобрать колледж по интересующей специальности, узнать о профессии подробнее и сделать правильный выбор.</p>

<h2>Что ты найдёшь на нашем сайте?</h2>
<ul>
    <li>Список колледжей — выбери учебное заведение по направлению, региону и форме обучения.</li>
    <li>Описание профессий — узнай, чем занимаются специалисты, какие навыки нужны и где работают.</li>
    <li>Полезные видео — посмотри советы от профессионалов и выпускников.</li>
    <li>Советы и рекомендации — получи полезные идеи от тех, кто уже прошёл этот путь.</li>
</ul>

<h3>Почему стоит начать с нас?</h3>
<ul>
    <li>Простой и понятный интерфейс</li>
    <li>Информация, проверенная и актуальная</li>
    <li>Подходит для школьников 9–11 классов</li>
</ul>

        <div class="thumbs">
          <img src="https://magistr.miet.ru/data/uploads/miet-bg-compressor.jpg" height="200" width="500">
          <img src="https://avatars.mds.yandex.net/get-altay/1007082/2a0000018635d0b652e7d8280b0685c014aa/orig" height="200" width="500">
        </div>

        <p class="muted">Подбор колледжа находится на отдельной странице.</p>

        <div class="top-actions">
          <a class="btn" href="/search">Перейти к подбору →</a>
          <a class="btn btn-secondary" href="/colleges">Открыть список колледжей</a>
        </div>

        <div class="footer">Flask + PostgreSQL (Render)</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

search_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Подбор</title>
  {{ style|safe }}
</head>
<body>
  {{ nav|safe }}
  <div class="container">
    <div class="hero">
      <div class="hero-body">
        <h1>Подбор колледжа</h1>
        <p class="muted">Введи специальность — покажем московские колледжи из базы. Нажми на карточку, чтобы открыть подробности.</p>

        <form class="search-box" action="/search" method="get">
          <input class="input" type="text" name="q" placeholder="Например: программирование, сети, медицина, архитектура..." value="{{ q }}">
          <button class="btn" type="submit">Найти</button>
          <a class="btn btn-secondary" href="/search">Сброс</a>
        </form>

        {% if q %}
          <div class="note">Результаты: "<strong>{{ q }}</strong>" • найдено: <strong>{{ colleges|length }}</strong></div>

          {% if colleges %}
            <div class="cards">
              {% for c in colleges %}
                <a class="card-link" href="/college/{{ c.id }}">
                  <div class="card">
                    <img src="{{ image_for_speciality(c.speciality) }}" alt="Колледж">
                    <div class="card-body">
                      <div class="title">{{ c.name }}</div>
                      <div class="meta">
                        Специальность: {{ c.speciality }}<br>
                        Регион: {{ c.region }} • Форма: {{ c.form }}
                      </div>
                    </div>
                  </div>
                </a>
              {% endfor %}
            </div>
          {% else %}
            <div class="note">Ничего не найдено. Попробуй другой запрос.</div>
          {% endif %}
        {% else %}
          <div class="note">Совет: попробуй “программирование”, “сети”, “медицина”, “архитектура”, “бизнес”.</div>
        {% endif %}

        <div class="thumbs">
          <img src="https://habrastorage.org/webt/pp/pr/un/ppprunckrvwqqfhcgedjwxz9jwu.jpeg" height="300" width="500">
          <img src="https://static.tildacdn.pro/tild3136-3630-4533-b234-323632663639/DALLE_2023-11-29_144.png" height="300" width="500">
        </div>

      </div>
    </div>
  </div>
</body>
</html>
"""

colleges_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Все колледжи</title>
  {{ style|safe }}
</head>
<body>
  {{ nav|safe }}
  <div class="container">
    <div class="hero">
      <div class="hero-body">
        <h1>Список колледжей (Москва)</h1>
        <p class="muted">Нажми на название, чтобы открыть страницу колледжа.</p>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Название</th>
                <th>Специальность</th>
                <th>Регион</th>
                <th>Форма</th>
              </tr>
            </thead>
            <tbody>
              {% for c in colleges %}
                <tr>
                  <td><a href="/college/{{ c.id }}"><b>{{ c.name }}</b></a></td>
                  <td>{{ c.speciality }}</td>
                  <td>{{ c.region }}</td>
                  <td>{{ c.form }}</td>
                </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  </div>
</body>
</html>
"""

college_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ college.name }}</title>
  {{ style|safe }}
</head>
<body>
  {{ nav|safe }}
  <div class="container">
    <div class="hero">
      <div class="hero-body">
        <h1 style="margin-bottom:6px;">{{ college.name }}</h1>
        <p class="muted" style="margin-top:0;">
          Специальность: <b>{{ college.speciality }}</b> • Регион: <b>{{ college.region }}</b> • Форма: <b>{{ college.form }}</b>
        </p>

        <h3 style="margin-top:14px;">Описание</h3>
        <p class="muted" style="font-size:15px; line-height:1.7;">
          {{ description }}
        </p>

        {% if website_url %}
          <div class="note">
            Официальный сайт колледжа:
            <a class="btn" style="margin-left:10px;" href="{{ website_url }}" target="_blank" rel="noopener noreferrer">
              Открыть сайт →
            </a>
            <div style="margin-top:10px; font-size:13px; color: rgba(255,255,255,.65);">
              {{ website_url }}
            </div>
          </div>
        {% endif %}

        <div class="top-actions">
          <a class="btn btn-secondary" href="/search">← Назад к подбору</a>
          <a class="btn" href="/colleges">Список колледжей →</a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

tips_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Полезные советы</title>
  {{ style|safe }}
</head>
<body>
  {{ nav|safe }}
  <div class="container">
    <div class="hero">
        <img src="https://sh14-ustilimsk-r138.gosweb.gosuslugi.ru/netcat_files/51/168/Abiturientu.jpg" height="200" width="1145">
        <h1>Полезные советы</h1>
        <h2>На что обращать внимание, выбирая колледж</h2>
        <h3 style="font-size:20px">Программы обучения:</h3>
        <ol>
        <li>Наличие государственной аккредитации и лицензии по выбранной специальности — это гарантирует получение диплома государственного образца. Проверить наличие документов можно на официальном сайте колледжа или в Рособрнадзоре</li>
        <li>Учебный план — стоит изучить соотношение теоретических и практических занятий, возможность выбора дополнительных курсов</li>
        <li>Актуальность программ — важно выбирать колледжи, которые предлагают программы, соответствующие современным требованиям и тенденциям</li>
        </ol>
        <h4 style="font-size:20px">Условия поступления:</h4>
        <ol>
        <li>Срок обучения — зависит от выбранной специальности, формы обучения и того, после какого класса поступает абитуриент. В среднем программа занимает 3–4 года, но возможны варианты от 10 месяцев до 5 лет</li>
        <li>Форма обучения — например, очная — самая быстрая форма, необходимо посещение колледжа в будни, очно-заочная, заочная или онлайн — подходят трудоустроенным студентам</li>
        <li>Требования к документам — каждый колледж имеет свои требования, важно заранее ознакомиться с ними. Некоторые колледжи могут требовать результаты вступительных экзаменов</li>
        </ol>
        <h5 style="font-size:20px">Инфраструктура:</h5>
        <ol>
        <li>Наличие учебных лабораторий и библиотек— это влияет на комфортное обучение и общение студентов</li>
        <li>Доступность учебных материалов — стоит обратить внимание на наличие онлайн-курсов и других ресурсов, которые могут помочь в учёбе</li>
        <li>Поддержка со стороны учебного персонала— важно, чтобы в колледже была поддержка, включая консультации и помощь в исследовательской деятельности</li>
        </ol>
        <h6 style="font-size:20px">Отзывы:</h6>
        <ol>
        <li>Изучить реальные мнения о колледже — можно использовать независимые форумы и социальные сети. Обращать внимание не на абстрактные жалобы («плохие преподаватели»), а на конкретику: организована ли практика, есть ли оборудование для этого, помогает ли колледж с трудоустройством</li>
        <li>Учесть достижения выпускников — стоит изучить, какие успехи они достигли после окончания колледжа</li>
        </ol>
        <p style="font-weight: bold;">Важно не выбирать колледж только на основе мнений друзей или семьи — важно учитывать свои предпочтения и карьерные цели</p>
      </div>
    </div>
  </div>
</body>
</html>
"""


# ------------------ РОУТЫ ------------------
@app.route("/")
def index():
    return render_template_string(index_template, style=STYLE, nav=NAV)


@app.route("/search")
def search():
    q = (request.args.get("q") or "").strip()
    colleges = []
    if q:
        colleges = College.query.filter(College.speciality.ilike(f"%{q}%")).all()

    return render_template_string(
        search_template,
        style=STYLE,
        nav=NAV,
        q=q,
        colleges=colleges,
        image_for_speciality=image_for_speciality,
    )


@app.route("/colleges")
def all_colleges():
    colleges = College.query.order_by(College.name).all()
    return render_template_string(colleges_template, style=STYLE, nav=NAV, colleges=colleges)


@app.route("/college/<int:college_id>")
def college_page(college_id: int):
    college = College.query.get(college_id)
    if not college:
        abort(404)

    return render_template_string(
        college_template,
        style=STYLE,
        nav=NAV,
        college=college,
        description=description_for_speciality(college.speciality),
        website_url=get_college_link(college.name),
    )


@app.route("/register")
def register():
    return render_template_string(tips_template, style=STYLE, nav=NAV)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
