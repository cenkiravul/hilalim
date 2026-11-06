"""Builds the static SEO pages of hilalim.com from data/*.json (see fetch_data.py).

Run: python3 scripts/build.py
Outputs: index.html, <city>/index.html, imsakiye-2027/index.html, sitemap.xml, robots.txt
"""
import datetime as dt
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://hilalim.com'
APP_ID = '6829459110'
IOS_URL = f'https://apps.apple.com/tr/app/hilalim-ezan-vakti-i-msakiye/id{APP_ID}'
RAMADAN_START = dt.date(2027, 2, 8)  # 1 Ramazan 1448 (Diyanet)
RAMADAN_DAYS = 29
NAMES = ['İmsak', 'Güneş', 'Öğle', 'İkindi', 'Akşam', 'Yatsı']
TR_MONTHS = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
TR_DAYS = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']

CSS = """
:root{--bg:#0B1A24;--surface:#132836;--line:#1f3a4a;--text:#F2F5F3;--muted:#A9B8B2;--gold:#E2B04A;--green:#3FB59A}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.6;font-size:17px}
a{color:var(--gold)}main{max-width:760px;margin:0 auto;padding:24px 16px 64px}
header.top{display:flex;align-items:center;gap:10px;padding:16px;max-width:760px;margin:0 auto}
header.top a{color:var(--text);text-decoration:none;font-weight:800;font-size:20px}
h1{font-size:32px;line-height:1.2;margin:8px 0 8px}h2{font-size:22px;margin:36px 0 12px;color:var(--gold)}
p,li{color:var(--muted)}strong{color:var(--text)}
.card{background:var(--surface);border-radius:20px;padding:20px;margin:16px 0}
.times{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.t{background:var(--bg);border-radius:14px;padding:12px;text-align:center}
.t b{display:block;font-size:24px;color:var(--text);font-variant-numeric:tabular-nums}.t span{color:var(--muted);font-size:15px}
.t.next{outline:2px solid var(--gold)}
.count{font-size:44px;font-weight:800;font-variant-numeric:tabular-nums;margin:4px 0}
.label{color:var(--gold);font-weight:700}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
th,td{padding:10px 6px;text-align:left;border-bottom:1px solid var(--line);font-size:16px}th{color:var(--muted);font-weight:600}
td.num{text-align:right}tr.today td{color:var(--gold);font-weight:700}
.btn{display:block;text-align:center;padding:16px;border-radius:16px;background:var(--gold);color:var(--bg);font-weight:800;text-decoration:none;font-size:18px;margin:12px 0}
.cities{columns:3 160px;padding:0;list-style:none}.cities li{margin:4px 0}.cities a{text-decoration:none}
footer{color:var(--muted);font-size:14px;text-align:center;padding:32px 16px}footer a{color:var(--muted)}
@media(max-width:480px){h1{font-size:27px}.count{font-size:36px}.t b{font-size:21px}}
"""

LOGO = ('<svg width="34" height="34" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="10" '
        'stroke="#FAF3E2" stroke-width="2" stroke-dasharray="52 63" transform="rotate(-90 12 12)"/>'
        '<path d="M11 7a3.6 3.6 0 0 0 5.4 5.4A5.4 5.4 0 1 1 11 7Z" fill="#F0BE54"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def tr_date(d, weekday=True):
    s = f'{d.day} {TR_MONTHS[d.month - 1]} {d.year}'
    return f'{s} {TR_DAYS[d.weekday()]}' if weekday else s


def page(title, description, path, body, extra_head=''):
    url = SITE + path
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B1A24">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="apple-touch-icon" href="/icon.png">
<style>{CSS}</style>
{extra_head}
</head>
<body>
<header class="top">{LOGO}<a href="/">Hilalim</a></header>
<main>
{body}
</main>
<footer>Vakitler: T.C. Diyanet İşleri Başkanlığı resmî namaz vakitleri tablosu · <a href="/privacy.html">Gizlilik</a> · <a href="/support.html">Destek</a><br>© {dt.date.today().year} KRVL Games</footer>
</body>
</html>
"""


def app_cta(city=None):
    where = f'{city} için ' if city else ''
    return f"""<div class="card">
<p class="label">Hilalim uygulaması</p>
<p><strong>{where}ezan vakti bildirimi, iftar ve sahur sayacı, kıble pusulası ve zikirmatik</strong> — büyük yazılarla, sade ve ücretsiz. Vakitler Diyanet’in resmî tablosundan, internetsiz de çalışır.</p>
<a class="btn" href="{IOS_URL}">App Store’dan ücretsiz indir</a>
</div>"""


def ramadan_rows(days):
    rows = []
    for i in range(RAMADAN_DAYS):
        d = RAMADAN_START + dt.timedelta(days=i)
        t = days.get(d.isoformat())
        if t:
            rows.append((i + 1, d, t))
    return rows


def city_page(c, cities, today):
    name, slug, days = c['name'], c['slug'], c['days']
    t_today = days.get(today.isoformat())
    rows = ramadan_rows(days)
    title = f'{name} Ezan Vakti ve İmsakiye 2027 — Namaz Vakitleri | Hilalim'
    desc = (f'{name} ezan vakti, namaz vakitleri ve Ramazan 2027 imsakiyesi. Diyanet’in resmî {name} imsak, '
            f'güneş, öğle, ikindi, akşam (iftar) ve yatsı vakitleri; iftara kalan süre.')
    cells = ''.join(f'<div class="t" data-i="{i}"><span>{n}</span><b>{t_today[i] if t_today else "–"}</b></div>'
                    for i, n in enumerate(NAMES))
    ram = ''.join(f'<tr><td>{n}</td><td>{d.day} {TR_MONTHS[d.month-1][:3]} {TR_DAYS[d.weekday()][:3]}</td>'
                  f'<td class="num">{t[0]}</td><td class="num">{t[4]}</td></tr>' for n, d, t in rows)
    month = []
    for k in range(30):
        d = today + dt.timedelta(days=k)
        t = days.get(d.isoformat())
        if t:
            month.append(f'<tr{" class=today" if k == 0 else ""}><td>{d.day} {TR_MONTHS[d.month-1][:3]}</td>'
                         + ''.join(f'<td class="num">{x}</td>' for x in t) + '</tr>')
    others = ''.join(f'<li><a href="/{o["slug"]}/">{esc(o["name"])}</a></li>' for o in cities if o['slug'] != slug)
    data = json.dumps(days, separators=(',', ':'))
    ld = json.dumps({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Hilalim', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': f'{name} ezan vakti', 'item': f'{SITE}/{slug}/'}]},
        ensure_ascii=False)
    first_iftar = rows[0][2][4] if rows else ''
    body = f"""
<h1>{esc(name)} ezan vakti</h1>
<p>{esc(name)} için bugünkü namaz vakitleri ve 2027 Ramazan imsakiyesi. Vakitler, Diyanet İşleri Başkanlığı’nın {esc(name)} için yayınladığı resmî tablodan alınmıştır.</p>
<div class="card">
<p class="label" id="when">Bugün · {tr_date(today)}</p>
<p id="next-label" class="label" style="margin:0"></p>
<div class="count" id="count"></div>
<div class="times">{cells}</div>
</div>
{app_cta(name)}
<h2>{esc(name)} imsakiye 2027 (Ramazan 1448)</h2>
<p>Ramazan 2027, 8 Şubat 2027 Pazartesi günü başlıyor (ilk sahur 7 Şubat’ı 8 Şubat’a bağlayan gece). {esc(name)} için ilk gün iftar saati <strong>{first_iftar}</strong>.</p>
<div class="card"><table><thead><tr><th>Gün</th><th>Tarih</th><th class="num">İmsak</th><th class="num">İftar</th></tr></thead><tbody>{ram}</tbody></table></div>
<h2>{esc(name)} namaz vakitleri — önümüzdeki 30 gün</h2>
<div class="card" style="overflow-x:auto"><table><thead><tr><th>Tarih</th>{''.join(f'<th class="num">{n}</th>' for n in NAMES)}</tr></thead><tbody>{''.join(month)}</tbody></table></div>
<h2>Diğer şehirler</h2>
<ul class="cities">{others}</ul>
<script type="application/ld+json">{ld}</script>
<script>
var D={data};
var N={json.dumps(NAMES, ensure_ascii=False)};
function key(d){{return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}}
function at(d,hm){{var p=hm.split(':');return new Date(d.getFullYear(),d.getMonth(),d.getDate(),+p[0],+p[1])}}
function tick(){{
  var now=new Date(),t=D[key(now)];if(!t)return;
  var cells=document.querySelectorAll('.t');cells.forEach(function(c,i){{c.querySelector('b').textContent=t[i];c.classList.remove('next')}});
  var i=t.findIndex(function(x){{return at(now,x)>now}}),target,label;
  if(i<0){{var tm=new Date(now);tm.setDate(tm.getDate()+1);var tt=D[key(tm)];if(!tt)return;target=at(tm,tt[0]);label='İmsak vaktine kalan'}}
  else{{target=at(now,t[i]);label=N[i]+' vaktine kalan';cells[i].classList.add('next')}}
  var s=Math.max(0,Math.floor((target-now)/1000));
  document.getElementById('next-label').textContent=label;
  document.getElementById('count').textContent=[Math.floor(s/3600),Math.floor(s%3600/60),s%60].map(function(n){{return String(n).padStart(2,'0')}}).join(':');
}}
tick();setInterval(tick,1000);
</script>
"""
    return page(title, desc, f'/{slug}/', body)


def home_page(cities, today):
    tr = [c for c in cities if c['country'] == 'TR']
    ab = [c for c in cities if c['country'] != 'TR']
    lst = lambda cs: ''.join(f'<li><a href="/{c["slug"]}/">{esc(c["name"])} ezan vakti</a></li>' for c in cs)
    faq = [
        ('Hilalim’deki ezan vakitleri doğru mu?', 'Vakitler, Diyanet İşleri Başkanlığı’nın her ilçe için yayınladığı resmî namaz vakitleri tablosundan alınır ve telefonunuza kaydedilir.'),
        ('Ramazan 2027 ne zaman başlıyor?', 'Ramazan 1448, 8 Şubat 2027 Pazartesi günü başlıyor; ilk sahur 7 Şubat’ı 8 Şubat’a bağlayan gece yapılır. Ramazan Bayramı 9 Mart 2027’de.'),
        ('Uygulama ücretli mi?', 'Hilalim ücretsizdir ve reklamlarla desteklenir. İsterseniz reklamları tek seferlik bir satın almayla kaldırabilirsiniz; abonelik yoktur.'),
        ('Almanya ve Avrupa’da çalışıyor mu?', 'Evet. Diyanet’in Almanya, Hollanda, Belçika, Fransa, Avusturya ve diğer ülkeler için yayınladığı vakitler de kullanılır.'),
        ('İnternet olmadan çalışır mı?', 'Evet. Vakit tablosu bir kez indirildikten sonra uygulama internetsiz çalışır; bildirimler de telefonda zamanlanır.'),
    ]
    faq_html = ''.join(f'<h3 style="font-size:18px;margin:20px 0 4px">{esc(q)}</h3><p>{esc(a)}</p>' for q, a in faq)
    ld = json.dumps([
        {'@context': 'https://schema.org', '@type': 'MobileApplication', 'name': 'Hilalim: Ezan Vakti & İmsakiye',
         'operatingSystem': 'iOS', 'applicationCategory': 'LifestyleApplication', 'inLanguage': 'tr',
         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'TRY'},
         'url': SITE + '/', 'downloadUrl': IOS_URL, 'publisher': {'@type': 'Organization', 'name': 'KRVL Games'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]},
    ], ensure_ascii=False)
    body = f"""
<h1>Hilalim — Ezan Vakti, İmsakiye ve İftar Sayacı</h1>
<p><strong>Diyanet’in resmî ezan vakitleri</strong>, Ramazan imsakiyesi, iftar ve sahur sayacı, kıble pusulası ve zikirmatik tek uygulamada. Büyük yazılar, sade kullanım, ücretsiz.</p>
<a class="btn" href="{IOS_URL}">App Store’dan ücretsiz indir</a>
<div class="card">
<p class="label">Neler var?</p>
<ul>
<li><strong>Ezan vakitleri:</strong> Türkiye’nin tüm il ve ilçeleri ve Avrupa’daki şehirler için Diyanet vakitleri</li>
<li><strong>İftar ve sahur sayacı:</strong> Ramazan’da iftara kalan süre, sahur alarmı, iftar bildirimi</li>
<li><strong>İmsakiye 2027:</strong> 30 günlük Ramazan imsakiyesi, paylaşılabilir görsel</li>
<li><strong>Kıble pusulası</strong> ve <strong>zikirmatik</strong> (33 ve 99’luk turlar)</li>
<li><strong>Oruç takvimi:</strong> tuttuğunuz ve kaza oruçlarınız</li>
<li><strong>Günün hadisi:</strong> kaynağıyla sahih hadisler</li>
<li>Ana ekran ve kilit ekranı widget’ları, Dynamic Island, Apple Watch</li>
</ul>
</div>
<h2>Şehrinizin ezan vakti</h2>
<ul class="cities">{lst(tr)}</ul>
<h2>Avrupa’da ezan vakti</h2>
<ul class="cities">{lst(ab)}</ul>
<p><a href="/imsakiye-2027/">Ramazan 2027 imsakiyesi — tüm şehirler</a></p>
<h2>Sık sorulan sorular</h2>
{faq_html}
<script type="application/ld+json">{ld}</script>
"""
    return page('Hilalim — Ezan Vakti, Namaz Vakitleri ve İmsakiye 2027',
                'Diyanet’in resmî ezan vakitleri, namaz vakitleri, Ramazan 2027 imsakiyesi, iftar sayacı, kıble ve zikirmatik. Türkiye ve Avrupa’daki tüm şehirler için ücretsiz uygulama.',
                '/', body)


def imsakiye_page(cities):
    ist = next(c for c in cities if c['slug'] == 'istanbul')
    rows = ''.join(f'<tr><td>{n}</td><td>{tr_date(d)}</td><td class="num">{t[0]}</td><td class="num">{t[4]}</td></tr>'
                   for n, d, t in ramadan_rows(ist['days']))
    links = ''.join(f'<li><a href="/{c["slug"]}/">{esc(c["name"])} imsakiye</a></li>' for c in cities)
    body = f"""
<h1>İmsakiye 2027 — Ramazan 1448 imsak ve iftar vakitleri</h1>
<p>Ramazan 2027, <strong>8 Şubat 2027 Pazartesi</strong> başlıyor ve <strong>8 Mart 2027</strong> son oruçla bitiyor; Ramazan Bayramı 9 Mart 2027. Aşağıda İstanbul imsakiyesi; diğer şehirler için listeden şehrinizi seçin. Vakitler Diyanet İşleri Başkanlığı’nın resmî tablosundandır.</p>
<h2>İstanbul imsakiye 2027</h2>
<div class="card"><table><thead><tr><th>Gün</th><th>Tarih</th><th class="num">İmsak</th><th class="num">İftar</th></tr></thead><tbody>{rows}</tbody></table></div>
{app_cta()}
<h2>Şehirlere göre imsakiye 2027</h2>
<ul class="cities">{links}</ul>
"""
    return page('İmsakiye 2027 — Ramazan İmsak ve İftar Vakitleri | Hilalim',
                'Ramazan 2027 imsakiyesi: 81 il ve Avrupa şehirleri için Diyanet’in resmî imsak (sahur) ve iftar vakitleri. Ramazan 8 Şubat 2027’de başlıyor.',
                '/imsakiye-2027/', body)


def main():
    cities = [json.loads(p.read_text()) for p in sorted((ROOT / 'data').glob('*.json'))]
    cities.sort(key=lambda c: (c['country'] != 'TR', c['name'].replace('İ', 'I').replace('Ç', 'Cz').replace('Ş', 'Sz').replace('Ö', 'Oz').replace('Ü', 'Uz')))
    today = dt.date.today()
    for c in cities:
        (ROOT / c['slug']).mkdir(exist_ok=True)
        (ROOT / c['slug'] / 'index.html').write_text(city_page(c, cities, today))
    (ROOT / 'imsakiye-2027').mkdir(exist_ok=True)
    (ROOT / 'imsakiye-2027' / 'index.html').write_text(imsakiye_page(cities))
    (ROOT / 'index.html').write_text(home_page(cities, today))
    urls = ['/', '/imsakiye-2027/'] + [f'/{c["slug"]}/' for c in cities] + ['/support.html', '/privacy.html']
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{today.isoformat()}</lastmod></url>\n' for u in urls)
                                      + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    print(len(cities), 'cities')


if __name__ == '__main__':
    main()
