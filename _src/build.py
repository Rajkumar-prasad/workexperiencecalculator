#!/usr/bin/env python3
"""Generates the static site into ../site"""
import json, os, shutil, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import PAGES, TOOLS, HOME, SBOR, OSIG, PEN, KLAS
from blog import POSTS, SUPPORT, DATE as BLOG_DATE

DOMAIN = "https://workexperiencecalculator.online"
SITE_NAME = "Калкулатор за трудов стаж"
EMAIL = "contact@workexperiencecalculator.online"   # change to your real inbox
TODAY = datetime.date.today().isoformat()
TODAY_BG = datetime.date.today().strftime("%d.%m.%Y")
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # repo root = deployed site

GOOGLE_TAGS = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-HCHC0B0Y7R"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-HCHC0B0Y7R');
  </script>
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7904206080765704"
     crossorigin="anonymous"></script>"""

NAV = [("/", "Трудов стаж"), ("/sbor-na-trudov-stazh/", "Сбор на стаж"), ("/osiguritelen-stazh/", "Осигурителен стаж"), ("/stazh-za-pensia/", "Пенсия"), ("/klas-prosluzheno-vreme/", "Клас"), ("/blog/", "Блог")]


def head(title, desc, path, extra_schema=None, robots="index, follow"):
    url = DOMAIN + path
    schema = ""
    if extra_schema:
        schema = '  <script type="application/ld+json">\n' + json.dumps(extra_schema, ensure_ascii=False, indent=2) + "\n  </script>\n"
    return f"""<!doctype html>
<html lang="bg">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#1d4ed8">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="bg_BG">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{DOMAIN}/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/og-image.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap&subset=cyrillic" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css">
{schema}{GOOGLE_TAGS}
</head>
<body>
<a class="skip" href="#main">Към съдържанието</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{SITE_NAME} - начало"><span class="logo-mark" aria-hidden="true">ТС</span>{SITE_NAME}</a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav">Меню</button>
    <nav class="nav" id="nav" aria-label="Основна навигация">
{nav_links(path)}
    </nav>
  </div>
</header>
"""


def nav_links(path):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == path else ""
        out.append(f'      <a href="{href}"{cur}>{label}</a>')
    return "\n".join(out)


FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h2>{SITE_NAME}</h2>
        <p>Безплатен онлайн инструмент за изчисляване на трудов стаж в години, месеци и дни. Работи изцяло в браузъра ви - датите не се изпращат никъде.</p>
      </div>
      <div>
        <h2>Калкулатори</h2>
        <ul>
          <li><a href="/">Калкулатор за трудов стаж</a></li>
          <li><a href="/sbor-na-trudov-stazh/">Сбор на трудов стаж</a></li>
          <li><a href="/osiguritelen-stazh/">Осигурителен стаж</a></li>
          <li><a href="/stazh-za-pensia/">Стаж за пенсия</a></li>
          <li><a href="/klas-prosluzheno-vreme/">Клас прослужено време</a></li>
        </ul>
      </div>
      <div>
        <h2>Информация</h2>
        <ul>
          <li><a href="/blog/">Блог</a></li>
          <li><a href="/za-nas/">За нас</a></li>
          <li><a href="/kontakti/">Контакти</a></li>
          <li><a href="/poveritelnost/">Поверителност</a></li>
          <li><a href="/usloviya/">Общи условия</a></li>
          <li><a href="/otkaz-ot-otgovornost/">Отказ от отговорност</a></li>
        </ul>
      </div>
    </div>
    <p class="copy">&copy; <span id="y">2026</span> workexperiencecalculator.online. Резултатите са ориентировъчни и не заместват официален документ за стаж.</p>
  </div>
</footer>
<script>
  (function(){{var b=document.querySelector('.menu-toggle'),n=document.getElementById('nav');
  b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);}});
  document.getElementById('y').textContent=new Date().getFullYear();}})();
</script>
"""


def write(path, html):
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/404" else os.path.join(OUT, "404.html")
    if path == "/":
        fp = os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)



POST_BY_PATH = {p["path"]: p for p in POSTS}


def articles_block(page_path, heading="Полезни статии"):
    items = SUPPORT.get(page_path, [])
    if not items:
        return ""
    cards = "\n".join(f'        <a class="post-card" href="{h}"><b>{POST_BY_PATH[h]["h1"]}</b><span>{POST_BY_PATH[h]["excerpt"]}</span></a>' for h in items)
    return f"""
    <section class="section">
      <h2>{heading}</h2>
      <div class="post-list">
{cards}
      </div>
    </section>"""

# ---------------------------------------------------------------- Home
FAQ = [
    ("Как се изчислява трудовият стаж?",
     "Въведете началната и крайната дата на всеки период, в който сте работили, и натиснете „Изчисли“. Калкулаторът брои и първия, и последния работен ден, обединява припокриващите се периоди и показва общия стаж в години, месеци и дни."),
    ("Мога ли да събера стажа от няколко работодатели?",
     "Да. Добавете отделен период за всяка работа с бутона „Добави период“. Калкулаторът сумира всички периоди и показва както общия резултат, така и стажа за всеки период поотделно."),
    ("Какво става, ако два периода се припокриват?",
     "Ако сте работили на две места едновременно, едно и също време не се брои два пъти. Припокриващите се дни се отчитат само веднъж и калкулаторът ви уведомява за това."),
    ("Как да изчисля стажа на текущата си работа?",
     "Въведете началната дата и отметнете „Работя тук и в момента“. Крайната дата автоматично става днешната и виждате натрупания стаж до днес."),
    ("Как се събират дните и месеците?",
     "Всеки период се смята по календара. При сумиране на няколко периода 30 дни се приравняват на 1 месец, а 12 месеца - на 1 година. Затова резултатът никога не показва 30 дни или 12 месеца."),
    ("Може ли резултатът да се използва за пенсия?",
     "Калкулаторът дава бърза ориентировъчна справка. Официалният осигурителен стаж за пенсия се установява от НОИ въз основа на трудовата книжка и документите от работодателите, като се прилагат правилата на Кодекса на труда и Кодекса за социалното осигуряване."),
    ("Безплатен ли е калкулаторът и пазите ли данните ми?",
     "Да, напълно безплатен е и не изисква регистрация. Изчисленията се правят в браузъра ви. Въведените дати се запазват само на вашето устройство, за да не ги въвеждате отново, и не се изпращат до сървър."),
]

home_schema = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": SITE_NAME, "inLanguage": "bg"},
        {"@type": "WebApplication", "@id": DOMAIN + "/#calculator", "name": SITE_NAME, "url": DOMAIN + "/",
         "applicationCategory": "BusinessApplication", "operatingSystem": "Any", "inLanguage": "bg",
         "description": "Безплатен онлайн калкулатор за трудов стаж в години, месеци и дни с няколко периода и автоматично обединяване на припокриващи се периоди.",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
        {"@type": "FAQPage", "@id": DOMAIN + "/#faq",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ],
}

faq_html = "\n".join(f"      <details>\n        <summary>{q}</summary>\n        <p>{a}</p>\n      </details>" for q, a in FAQ)

home = head("Калкулатор за трудов стаж | Изчисли стажа си онлайн безплатно",
            "Безплатен калкулатор за трудов стаж. Изчисли общия си стаж в години, месеци и дни, събери няколко работни периода и провери текущия си стаж до днес.",
            "/", home_schema) + f"""
<main id="main">
  <section class="hero">
    <div class="wrap">
      <h1>Калкулатор за трудов стаж</h1>
      <p>Изчислете общия си трудов стаж в години, месеци и дни. Добавете всички работни периоди - калкулаторът ги сумира и не брои два пъти припокриващо се време.</p>
      <ul class="badges">
        <li>Безплатно</li><li>Без регистрация</li><li>Няколко периода</li><li>Стаж до днес</li>
      </ul>
    </div>
  </section>

  <div class="wrap">
    <section class="calc" aria-labelledby="calc-title">
      <h2 id="calc-title">Изчислете стажа си</h2>
      <p class="hint">Първият и последният работен ден се включват в изчислението.</p>

      <div id="periods"></div>

      <template id="period-tpl">
        <div class="period">
          <div class="period-head">
            <span class="p-num">Период 1</span>
            <button type="button" class="p-remove" aria-label="Премахни периода" title="Премахни периода">&times;</button>
          </div>
          <div class="fields">
            <div>
              <label>Начална дата<input type="date" class="p-start" min="1940-01-01" max="2100-12-31"></label>
            </div>
            <div>
              <label>Крайна дата<input type="date" class="p-end" min="1940-01-01" max="2100-12-31"></label>
            </div>
          </div>
          <label class="now"><input type="checkbox" class="p-now"> Работя тук и в момента</label>
        </div>
      </template>

      <div class="actions">
        <button type="button" class="btn btn-ghost" id="add-period">+ Добави период</button>
        <button type="button" class="btn btn-primary" id="calc-btn">Изчисли стажа</button>
        <button type="button" class="btn btn-ghost" id="clear-btn">Изчисти</button>
      </div>
      <p class="error" id="calc-error" role="alert" hidden></p>

      <div class="result" id="result" hidden aria-live="polite">
        <p class="result-title">Общ трудов стаж</p>
        <div class="result-nums">
          <div class="num"><b id="r-y">0</b><span>години</span></div>
          <div class="num"><b id="r-m">0</b><span>месеца</span></div>
          <div class="num"><b id="r-d">0</b><span>дни</span></div>
        </div>
        <p class="result-words" id="r-words"></p>
        <p class="result-meta">Общо календарни дни: <strong id="r-days">0</strong></p>
        <p class="overlap" id="r-overlap" hidden>Някои периоди се припокриват. Общото време е отчетено само веднъж.</p>
        <table class="breakdown">
          <thead><tr><th>№</th><th>Период</th><th>Стаж</th></tr></thead>
          <tbody id="r-rows"></tbody>
        </table>
      </div>
    </section>

    <section class="section" id="kalkulatori">
      <h2>Още калкулатори за стаж</h2>
      <p>Трудовият стаж е само едната част от картината. С тези инструменти ще разберете и как стажът влияе на пенсията и на заплатата ви.</p>
      <div class="related">
        <a href="/sbor-na-trudov-stazh/"><b>Сбор на трудов стаж</b><span>Съберете стаж от няколко места в години, месеци и дни.</span></a>
        <a href="/osiguritelen-stazh/"><b>Калкулатор за осигурителен стаж</b><span>И при непълно работно време, по часове на ден.</span></a>
        <a href="/stazh-za-pensia/"><b>Стаж и възраст за пенсия</b><span>Вижте кога ще имате право на пенсия.</span></a>
        <a href="/klas-prosluzheno-vreme/"><b>Клас прослужено време</b><span>Колко евро на месец ви носи стажът.</span></a>
      </div>
    </section>

    <section class="section" id="kak-raboti">
      <h2>Как работи калкулаторът за трудов стаж</h2>
      <p>Ръчното броене на месеци и дни лесно води до грешки - особено когато сте сменили няколко работодатели или сте имали прекъсвания. Калкулаторът прави сметката вместо вас в четири стъпки.</p>
      <ol class="steps">
        <li><strong>Въведете първия период</strong>Посочете началната и крайната дата на работа, както са записани в трудовата книжка или договора.</li>
        <li><strong>Добавете още периоди</strong>За всяка следваща работа натиснете „Добави период“. Прекъсванията между периодите не се броят. Ако стажът ви вече е записан в години, месеци и дни, използвайте <a href="/sbor-na-trudov-stazh/">сбор на трудов стаж</a>.</li>
        <li><strong>Отбележете текущата работа</strong>Ако още работите на последното място, отметнете „Работя тук и в момента“ и крайната дата става днешната.</li>
        <li><strong>Натиснете „Изчисли стажа“</strong>Виждате общия стаж в години, месеци и дни, общия брой дни и стажа за всеки период поотделно.</li>
      </ol>
    </section>

    <section class="section">
      <h2>Какво прави този калкулатор точен</h2>
      <div class="grid">
        <div class="feature"><h3>Календарно изчисление</h3><p>Всеки период се смята по реалните месеци в календара, а не със средни стойности като 30,44 дни.</p></div>
        <div class="feature"><h3>Включва последния ден</h3><p>От 01.01.2018 до 31.12.2022 са точно 5 години, защото и последният работен ден се брои.</p></div>
        <div class="feature"><h3>Без двойно броене</h3><p>Ако два договора се застъпват, едно и също време се отчита само веднъж.</p></div>
        <div class="feature"><h3>Поверителност</h3><p>Изчисленията се извършват на вашето устройство. Не събираме въведените дати.</p></div>
      </div>
    </section>

    <section class="section">
      <h2>Примери за изчисляване на трудов стаж</h2>
      <div class="example">
        <h3>Пример 1: Един работодател</h3>
        <p>Работили сте от 01.01.2018 до 31.12.2022.</p>
        <p>Резултат: <span class="res">5 г. 0 м. 0 д.</span></p>
      </div>
      <div class="example">
        <h3>Пример 2: Двама работодатели с прекъсване</h3>
        <p>Период 1: 01.03.2015 - 31.05.2018 (3 г. 3 м. 0 д.)<br>Период 2: 01.09.2018 - 31.08.2022 (4 г. 0 м. 0 д.)</p>
        <p>Резултат: <span class="res">7 г. 3 м. 0 д.</span> Трите месеца между двете работи не се броят.</p>
      </div>
      <div class="example">
        <h3>Пример 3: Припокриващи се договори</h3>
        <p>Основна работа: 01.01.2020 - 31.12.2021. Втори договор: 01.06.2021 - 30.06.2022.</p>
        <p>Резултат: <span class="res">2 г. 6 м. 0 д.</span> Периодът юни - декември 2021 г. се отчита веднъж.</p>
      </div>
    </section>

    <section class="section">
      <h2>Трудов стаж и осигурителен стаж - каква е разликата</h2>
      <p><strong>Трудовият стаж</strong> е времето, през което сте работили по трудово правоотношение. Той се вписва в трудовата книжка и има значение например за <a href="/klas-prosluzheno-vreme/">клас прослужено време</a> и за размера на някои обезщетения.</p>
      <p><strong>Осигурителният стаж</strong> е времето, за което са внасяни осигуровки, включително при работа без трудов договор, например като самоосигуряващо се лице. Той е определящ за правото на пенсия. Изчислете го с <a href="/osiguritelen-stazh/">калкулатора за осигурителен стаж</a> и проверете <a href="/stazh-za-pensia/">колко стаж ви трябва за пенсия</a>.</p>
      <p class="note">Калкулаторът е полезен за CV, кандидатстване за работа, проверка на данни в трудовата книжка и ориентировъчна справка за пенсия. За официални цели използвайте документите от работодателя или справка от НОИ.</p>
    </section>

{articles_block("/", "Как да изчислите стажа си: полезни статии")}

    <section class="section faq" id="vaprosi">
      <h2>Често задавани въпроси</h2>
{faq_html}
    </section>
  </div>
</main>
{FOOTER}<script src="/assets/calc.js" defer></script>
</body>
</html>
"""
write("/", home)



# ---------------------------------------------------------------- Tool pages
def tool_page(pg):
    url = DOMAIN + pg["path"]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": pg["h1"], "url": url, "applicationCategory": "BusinessApplication",
         "operatingSystem": "Any", "inLanguage": "bg", "description": pg["app_desc"],
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Начало", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": pg["crumb"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pg["faq"]]},
    ]}
    faq = "\n".join(f"      <details>\n        <summary>{q}</summary>\n        <p>{a}</p>\n      </details>" for q, a in pg["faq"])
    rel = "\n".join(f'        <a href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in TOOLS if h != pg["path"])
    html = head(pg["title"], pg["desc"], pg["path"], schema) + f"""
<main id="main">
  <section class="hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Навигационна пътека"><ol><li><a href="/">Начало</a></li><li aria-current="page">{pg["crumb"]}</li></ol></nav>
      <h1>{pg["h1"]}</h1>
      <p>{pg["lead"]}</p>
    </div>
  </section>

  <div class="wrap">
{pg["tool"]}
{pg["body"]}

    <section class="section faq">
      <h2>Често задавани въпроси</h2>
{faq}
    </section>

{articles_block(pg["path"])}

    <section class="section">
      <h2>Свързани калкулатори</h2>
      <div class="related">
{rel}
      </div>
      <p class="updated" style="margin-top:18px">Последна актуализация: {TODAY_BG}</p>
    </section>
  </div>
</main>
{FOOTER}<script src="/assets/tools.js" defer></script>
</body>
</html>
"""
    write(pg["path"], html)


for pg in PAGES:
    tool_page(pg)



AUTHOR = {
    "name": "Мария Димитрова",
    "name_lat": "Maria Dimitrova",
    "url": "/avtor/maria-dimitrova/",
    "img": "/assets/maria-dimitrova.jpg",
    "bio": "Мария Димитрова (Maria Dimitrova) е редакционният псевдоним, под който се публикуват ръководствата в „Калкулатор за трудов стаж“. Статиите ѝ обясняват как да изчислите годините трудов стаж, как да съберете времето от няколко работи и как да посочите датите на заетост в CV и при кандидатстване за работа.",
}
AUTHOR_SCHEMA = {"@type": "Person", "name": AUTHOR["name"], "alternateName": AUTHOR["name_lat"],
                 "url": DOMAIN + AUTHOR["url"], "image": DOMAIN + AUTHOR["img"], "description": AUTHOR["bio"]}

# ---------------------------------------------------------------- Blog
import re as _re
BG_MONTHS = ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"]
def bg_date(iso):
    y, m, d = map(int, iso.split("-"))
    return f"{d} {BG_MONTHS[m-1]} {y} г."


def blog_post(pt):
    url = DOMAIN + pt["path"]
    words = len(_re.sub(r"<[^>]+>", " ", pt["body"]).split())
    mins = max(3, round(words / 200))
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": pt["h1"], "description": pt["desc"], "inLanguage": "bg",
         "datePublished": pt.get("date", BLOG_DATE), "dateModified": pt.get("date", BLOG_DATE), "mainEntityOfPage": url,
         "image": DOMAIN + "/og-image.png",
         "author": AUTHOR_SCHEMA,
         "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": DOMAIN + "/icon-512.png"}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Начало", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Блог", "item": DOMAIN + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": pt["h1"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pt["faq"]]},
    ]}
    tldr = "\n".join(f"          <li>{x}</li>" for x in pt["summary"])
    faq = "\n".join(f"        <details>\n          <summary>{q}</summary>\n          <p>{a}</p>\n        </details>" for q, a in pt["faq"])
    i = POSTS.index(pt)
    others = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
    more = "\n".join(f'        <a class="post-card" href="{p["path"]}"><b>{p["h1"]}</b><span>{p["excerpt"]}</span></a>' for p in others)
    th, tl = pt["tool"]
    html = head(pt["title"], pt["desc"], pt["path"], schema) + f"""
<main id="main">
  <section class="hero" style="padding-bottom:100px">
    <div class="wrap">
      <nav class="crumbs" aria-label="Навигационна пътека"><ol><li><a href="/">Начало</a></li><li><a href="/blog/">Блог</a></li><li aria-current="page">Статия</li></ol></nav>
      <h1>{pt["h1"]}</h1>
      <div class="byline"><img src="{AUTHOR["img"]}" alt="{AUTHOR["name"]}" width="44" height="44"><div><a href="{AUTHOR["url"]}">{AUTHOR["name"]}</a><span>Публикувано: {bg_date(pt.get("date", BLOG_DATE))} · {mins} мин. четене</span></div></div>
    </div>
  </section>
  <div class="wrap">
    <article class="post">
      <div class="tldr">
        <b>Накратко</b>
        <ul>
{tldr}
        </ul>
      </div>
{pt["body"]}

      <h2>Често задавани въпроси</h2>
      <div class="faq">
{faq}
      </div>

      <div class="cta"><p>Сметнете за секунди с {tl}.</p><a href="{th}">Към калкулатора →</a></div>

      <aside class="author-box" aria-label="За автора">
        <img src="{AUTHOR["img"]}" alt="{AUTHOR["name"]}" width="84" height="84" loading="lazy">
        <div><b><a href="{AUTHOR["url"]}">{AUTHOR["name"]}</a></b><small>Автор</small><p>{AUTHOR["bio"]}</p></div>
      </aside>
    </article>

    <section class="section">
      <h2>Още статии</h2>
      <div class="post-list">
{more}
      </div>
    </section>
  </div>
</main>
{FOOTER}</body>
</html>
"""
    write(pt["path"], html)


for pt in POSTS:
    blog_post(pt)

NEWEST = sorted(POSTS, key=lambda p: p.get("date", BLOG_DATE), reverse=True)
cards = "\n".join(f'        <a class="post-card" href="{p["path"]}"><b>{p["h1"]}</b><span>{p["excerpt"]}</span></a>' for p in NEWEST)
blog_index = head("Блог за трудов и осигурителен стаж | Полезни статии и съвети",
                  "Статии как да изчислите трудовия и осигурителния си стаж, да проверите стажа си в НОИ, да подадете заявление за пенсия и да проверите класа си.",
                  "/blog/", {"@context": "https://schema.org", "@type": "Blog", "name": "Блог - " + SITE_NAME, "url": DOMAIN + "/blog/", "inLanguage": "bg"}) + f"""
<main id="main">
  <section class="hero" style="padding-bottom:60px">
    <div class="wrap">
      <nav class="crumbs" aria-label="Навигационна пътека"><ol><li><a href="/">Начало</a></li><li aria-current="page">Блог</li></ol></nav>
      <h1>Блог за трудов и осигурителен стаж</h1>
      <p>Практични статии стъпка по стъпка - как да изчислите стажа си, да го проверите в НОИ и да не изпуснете парите, които ви се полагат.</p>
    </div>
  </section>
  <div class="wrap">
    <section class="section" style="margin-top:32px">
      <div class="post-list">
{cards}
      </div>
    </section>
  </div>
</main>
{FOOTER}</body>
</html>
"""
write("/blog/", blog_index)

author_cards = "\n".join(f'        <a class="post-card" href="{p["path"]}"><b>{p["h1"]}</b><span>{p["excerpt"]}</span></a>' for p in NEWEST)
author_schema = {"@context": "https://schema.org", "@type": "ProfilePage", "mainEntity": AUTHOR_SCHEMA}
author_page = head(f'{AUTHOR["name"]} - автор | {SITE_NAME}',
                   "Статии от Мария Димитрова за изчисляване на трудов стаж, сбор на стаж от няколко работи и посочване на датите на заетост в CV.",
                   AUTHOR["url"], author_schema) + f"""
<main id="main">
  <section class="hero" style="padding-bottom:60px">
    <div class="wrap">
      <nav class="crumbs" aria-label="Навигационна пътека"><ol><li><a href="/">Начало</a></li><li><a href="/blog/">Блог</a></li><li aria-current="page">{AUTHOR["name"]}</li></ol></nav>
      <div class="author-hero">
        <img src="{AUTHOR["img"]}" alt="{AUTHOR["name"]}" width="120" height="120">
        <div><h1>{AUTHOR["name"]}</h1><p>{AUTHOR["bio"]}</p></div>
      </div>
    </div>
  </section>
  <div class="wrap">
    <section class="section" style="margin-top:32px">
      <h2>Статии от {AUTHOR["name"]}</h2>
      <div class="post-list">
{author_cards}
      </div>
    </section>
  </div>
</main>
{FOOTER}</body>
</html>
"""
write(AUTHOR["url"], author_page)

# ---------------------------------------------------------------- Static pages
def page(path, title, desc, h1, body, robots="index, follow"):
    html = head(title, desc, path, robots=robots) + f"""
<main id="main">
  <article class="page">
    <h1>{h1}</h1>
{body}
  </article>
</main>
{FOOTER}</body>
</html>
"""
    write(path, html)


MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

page("/za-nas/", "За нас | Калкулатор за трудов стаж",
     "Научете повече за безплатния онлайн калкулатор за трудов стаж и защо го създадохме.",
     "За нас", f"""    <p>workexperiencecalculator.online е безплатен онлайн инструмент за бързо изчисляване на трудов стаж в години, месеци и дни.</p>
    <h2>Защо създадохме калкулатора</h2>
    <p>Ръчното събиране на стаж от няколко работни места е досадно и лесно води до грешки - пропуснат месец, неправилно преброени дни или двойно отчетено време при застъпващи се договори. Искахме инструмент, който дава ясен и проверим резултат за секунди.</p>
    <h2>Какво предлагаме</h2>
    <ul>
      <li>Неограничен брой работни периоди</li>
      <li>Календарно изчисление с включен последен работен ден</li>
      <li>Автоматично обединяване на припокриващи се периоди</li>
      <li>Стаж до днешна дата за текущата ви работа</li>
      <li>Работи на телефон, таблет и компютър, без регистрация</li>
    </ul>
    <h2>За кого е полезен</h2>
    <p>За служители, които подготвят CV или документи за нова работа, за HR специалисти и счетоводители, които правят бърза проверка, и за всеки, който иска ориентир колко стаж е натрупал.</p>
    <h2>Връзка с нас</h2>
    <p>Имате въпрос или идея как да подобрим калкулатора? Пишете ни на {MAIL}.</p>""")

page("/kontakti/", "Контакти | Калкулатор за трудов стаж",
     "Свържете се с екипа на калкулатора за трудов стаж за въпроси, предложения или сигнал за грешка.",
     "Контакти", f"""    <p>Ще се радваме да получим вашите въпроси, предложения или сигнали за грешка.</p>
    <h2>Имейл</h2>
    <p>{MAIL}</p>
    <p>Отговаряме обикновено в рамките на 1-2 работни дни.</p>
    <p class="note">Не можем да предоставяме индивидуални правни консултации или официални справки за стаж. За тях се обърнете към работодателя си или към НОИ.</p>""")

page("/poveritelnost/", "Политика за поверителност | Калкулатор за трудов стаж",
     "Политика за поверителност на workexperiencecalculator.online - какви данни, бисквитки и услуги на трети страни използваме.",
     "Политика за поверителност", f"""    <p class="updated">Последна актуализация: {TODAY}</p>
    <p>Тази политика обяснява как workexperiencecalculator.online обработва информация, когато използвате сайта.</p>
    <h2>Данни, въведени в калкулатора</h2>
    <p>Калкулаторът работи изцяло в браузъра ви. Въведените дати не се изпращат до наш сървър. За удобство последните въведени периоди се запазват в локалното хранилище на браузъра (localStorage) на вашето устройство. Можете да ги изтриете с бутона „Изчисти“ или чрез настройките на браузъра.</p>
    <h2>Google Analytics</h2>
    <p>Използваме Google Analytics 4, за да разберем как посетителите използват сайта (например брой посещения и използвани устройства). Google може да използва бисквитки и подобни технологии за тази цел.</p>
    <h2>Реклами чрез Google AdSense</h2>
    <p>Сайтът показва реклами чрез Google AdSense. Google и неговите партньори използват бисквитки, за да показват реклами въз основа на предишни посещения на този и други сайтове. Можете да управлявате персонализираните реклами в <a href="https://adssettings.google.com" rel="nofollow noopener" target="_blank">настройките за реклами на Google</a>. Повече информация: <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow noopener" target="_blank">Как Google използва данни от сайтове, които използват услугите му</a>.</p>
    <h2>Съгласие за бисквитки</h2>
    <p>За посетители от Европейското икономическо пространство показваме съобщение за съгласие, чрез което можете да приемете или откажете бисквитките за персонализирани реклами и анализ.</p>
    <h2>Вашите права</h2>
    <p>Съгласно Общия регламент относно защитата на данните (GDPR) имате право на достъп, коригиране, изтриване и възражение срещу обработването на лични данни. Тъй като не събираме данните, въведени в калкулатора, обикновено нямаме лична информация за вас.</p>
    <h2>Промени</h2>
    <p>Можем да актуализираме тази политика. Актуалната версия е винаги публикувана на тази страница.</p>
    <h2>Контакт</h2>
    <p>{MAIL}</p>""")

page("/usloviya/", "Общи условия | Калкулатор за трудов стаж",
     "Общи условия за използване на безплатния калкулатор за трудов стаж.",
     "Общи условия", f"""    <p class="updated">Последна актуализация: {TODAY}</p>
    <p>С използването на workexperiencecalculator.online приемате следните условия.</p>
    <h2>Използване на сайта</h2>
    <p>Калкулаторът се предоставя безплатно и е предназначен само за информационни цели. Резултатите не представляват правна, счетоводна или осигурителна консултация.</p>
    <h2>Точност</h2>
    <p>Полагаме усилия изчисленията да са точни, но резултатът зависи от въведените дати и не отчита специални правила (например зачитане на отпуск, категории труд или осигурителен стаж без трудов договор). За официални цели се обърнете към компетентна институция.</p>
    <h2>Ограничаване на отговорността</h2>
    <p>Не носим отговорност за вреди или загуби, произтичащи от използването на калкулатора или от решения, взети въз основа на резултатите.</p>
    <h2>Интелектуална собственост</h2>
    <p>Съдържанието и дизайнът на сайта са защитени от авторското право. Копирането без писмено съгласие не е разрешено.</p>
    <h2>Промени</h2>
    <p>Можем да променяме тези условия по всяко време. Актуалната версия е публикувана на тази страница.</p>
    <h2>Контакт</h2>
    <p>{MAIL}</p>""")

page("/otkaz-ot-otgovornost/", "Отказ от отговорност | Калкулатор за трудов стаж",
     "Отказ от отговорност за резултатите от онлайн калкулатора за трудов стаж.",
     "Отказ от отговорност", f"""    <p>Информацията и резултатите на workexperiencecalculator.online са само с информационна цел.</p>
    <h2>Не е правен съвет</h2>
    <p>Резултатите не са правна, счетоводна или друга професионална консултация. Официалният трудов и осигурителен стаж се удостоверява с трудовата книжка, документи от работодателя и справки от НОИ.</p>
    <h2>Без гаранция</h2>
    <p>Различни тълкувания на трудовото и осигурителното законодателство могат да доведат до различен резултат. Не гарантираме, че изчисленията отговарят на всеки конкретен случай.</p>
    <h2>Използване на собствена отговорност</h2>
    <p>Използвате калкулатора на своя отговорност. Не носим отговорност за решения, взети въз основа на резултатите.</p>
    <h2>Контакт</h2>
    <p>{MAIL}</p>""")

page("/404", "Страницата не е намерена | Калкулатор за трудов стаж",
     "Страницата, която търсите, не съществува.", "Страницата не е намерена",
     """    <p>Страницата, която търсите, не съществува или е преместена.</p>
    <p><a class="btn btn-primary" href="/" style="display:inline-block;text-decoration:none">Към калкулатора</a></p>""",
     robots="noindex, follow")

# ---------------------------------------------------------------- Support files
pages = ["/", SBOR, OSIG, PEN, KLAS, "/blog/", "/avtor/maria-dimitrova/"] + [p["path"] for p in POSTS] + [ "/za-nas/", "/kontakti/", "/poveritelnost/", "/usloviya/", "/otkaz-ot-otgovornost/"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages:
    pr = "1.0" if p == "/" else ("0.8" if p in (SBOR, OSIG, PEN, KLAS) else ("0.6" if p.startswith("/blog/") else "0.3"))
    sm.append(f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
files = {
    "sitemap.xml": "\n".join(sm) + "\n",
    "robots.txt": f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n",
    "ads.txt": "google.com, pub-7904206080765704, DIRECT, f08c47fec0942fa0\n",
    "google663c0df5aabba0ac.html": "google-site-verification: google663c0df5aabba0ac.html",
    # Old React routes (Cyrillic) -> new Latin URLs
    "_redirects": "\n".join([
        "/за-нас /za-nas/ 301",
        "/контакти /kontakti/ 301",
        "/поверителност /poveritelnost/ 301",
        "/условия /usloviya/ 301",
        "/отказ-от-отговорност /otkaz-ot-otgovornost/ 301",
        "/%D0%B7%D0%B0-%D0%BD%D0%B0%D1%81 /za-nas/ 301",
        "/%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B8 /kontakti/ 301",
        "/index.html / 301",
    ]) + "\n",
    "_headers": "\n".join([
        "/assets/*",
        "  Cache-Control: public, max-age=604800",
        "/*",
        "  X-Content-Type-Options: nosniff",
        "  Referrer-Policy: strict-origin-when-cross-origin",
    ]) + "\n",
}
for name, content in files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)

os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
here = os.path.dirname(__file__)
shutil.copy(os.path.join(here, "style.css"), os.path.join(OUT, "assets", "style.css"))
shutil.copy(os.path.join(here, "calc.js"), os.path.join(OUT, "assets", "calc.js"))
shutil.copy(os.path.join(here, "tools.js"), os.path.join(OUT, "assets", "tools.js"))
shutil.copy(os.path.join(here, "maria-dimitrova.jpg"), os.path.join(OUT, "assets", "maria-dimitrova.jpg"))
print("built", OUT)
