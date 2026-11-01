"""Downloads official Diyanet prayer time tables for the city pages (data/*.json).

Run: python3 scripts/fetch_data.py   (polite: one request every ~0.6 s)
"""
import json, re, time, html, unicodedata, urllib.request, pathlib

BASE = 'https://namazvakitleri.diyanet.gov.tr'
OUT = pathlib.Path(__file__).resolve().parent.parent / 'data'
UA = {'User-Agent': 'Mozilla/5.0 (hilalim.com city pages)'}
MONTHS = {'ocak': 1, 'şubat': 2, 'mart': 3, 'nisan': 4, 'mayıs': 5, 'haziran': 6, 'temmuz': 7,
          'ağustos': 8, 'eylül': 9, 'ekim': 10, 'kasım': 11, 'aralık': 12}
ROW = re.compile(r'<tr>\s*<td>(\d{1,2}) (\S+) (\d{4})[^<]*</td>\s*<td>[^<]*</td>((?:\s*<td>\d{2}:\d{2}</td>){6})')

# Diaspora cities: (country id, state name, district name, display name, slug)
ABROAD = [
    ('13', 'BERLIN', 'BERLIN', 'Berlin', 'berlin'),
    ('13', 'HAMBURG', 'HAMBURG', 'Hamburg', 'hamburg'),
    ('13', 'BAYERN', 'MUNCHEN', 'München', 'munih'),
    ('13', 'NORDRHEIN-WESTFALEN', 'KOLN', 'Köln', 'koln'),
    ('13', 'NORDRHEIN-WESTFALEN', 'DUISBURG', 'Duisburg', 'duisburg'),
    ('13', 'NORDRHEIN-WESTFALEN', 'DORTMUND', 'Dortmund', 'dortmund'),
    ('13', 'NORDRHEIN-WESTFALEN', 'DUSSELDORF', 'Düsseldorf', 'dusseldorf'),
    ('13', 'NORDRHEIN-WESTFALEN', 'ESSEN', 'Essen', 'essen'),
    ('13', 'HESSEN', 'FRANKFURT', 'Frankfurt', 'frankfurt'),
    ('13', 'BADEN WURTTEMBERG', 'STUTTGART', 'Stuttgart', 'stuttgart'),
    ('4', None, 'AMSTERDAM', 'Amsterdam', 'amsterdam'),
    ('4', None, 'ROTTERDAM', 'Rotterdam', 'rotterdam'),
    ('4', None, 'LAHEY', 'Lahey', 'lahey'),
    ('11', None, 'BRUKSEL', 'Brüksel', 'bruksel'),
    ('11', None, 'ANTWERPEN', 'Anvers', 'anvers'),
    ('35', None, 'VIYANA', 'Viyana', 'viyana'),
    ('21', None, 'PARIS', 'Paris', 'paris'),
    ('21', None, 'STRASBOURG', 'Strazburg', 'strazburg'),
    ('49', None, 'ZURIH', 'Zürih', 'zurih'),
    ('15', None, 'LONDRA', 'Londra', 'londra'),
]


def norm(s):
    s = s.upper().translate(str.maketrans('ÇĞİÖŞÜÄẞ', 'CGIOSUAS'))
    s = unicodedata.normalize('NFD', s)
    return re.sub(r'[^A-Z0-9]+', ' ', ''.join(c for c in s if not unicodedata.combining(c))).strip()


def get(path, tries=4):
    for attempt in range(tries):
        time.sleep(0.6 + attempt * 3)
        try:
            req = urllib.request.Request(BASE + path, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode('utf-8')
        except Exception as error:  # timeouts / resets: back off and retry
            if attempt == tries - 1:
                raise
            print('retry', path, error)


def states(country):
    return json.loads(get(f'/tr-TR/home/GetRegList?ChangeType=country&CountryId={country}&Culture=tr-TR'))['StateList'] or []


def districts(country, state):
    return json.loads(get(f'/tr-TR/home/GetRegList?ChangeType=state&CountryId={country}&StateId={state}&Culture=tr-TR'))['StateRegionList'] or []


def table(district_id):
    days = {}
    for d, m, y, cells in ROW.findall(get(f'/tr-TR/{district_id}')):
        month = MONTHS.get(html.unescape(m).lower().replace('i̇', 'i'))
        if month:
            days[f'{y}-{month:02d}-{int(d):02d}'] = re.findall(r'\d{2}:\d{2}', cells)
    return dict(sorted(days.items()))


def tr_title(s):
    low = s.replace('I', 'ı').replace('İ', 'i').lower()
    return ' '.join(w[:1].replace('i', 'İ').replace('ı', 'I').upper() + w[1:] for w in low.split())


def slugify(s):
    return norm(s).lower().replace(' ', '-')


def save(slug, name, region, country, did, days):
    OUT.mkdir(exist_ok=True)
    (OUT / f'{slug}.json').write_text(json.dumps(
        {'slug': slug, 'name': name, 'region': region, 'country': country, 'diyanetId': did, 'days': days},
        ensure_ascii=False, separators=(',', ':')))


def main():
    for st in states('2'):
        name = tr_title(st['SehirAdi'])
        slug = slugify(st['SehirAdi'])
        if (OUT / f'{slug}.json').exists():
            continue
        ds = districts('2', st['SehirID'])
        centre = next((d for d in ds if norm(d['IlceAdi']) == norm(st['SehirAdi'])), ds[0] if ds else None)
        if not centre:
            continue
        save(slug, name, 'Türkiye', 'TR', centre['IlceID'], table(centre['IlceID']))
        print('TR', name)
    state_cache = {}
    for country, state_name, district, name, slug in ABROAD:
        if (OUT / f'{slug}.json').exists():
            continue
        sts = state_cache.setdefault(country, states(country))
        cands = [s for s in sts if state_name is None or norm(s['SehirAdi']) == norm(state_name)]
        hit = None
        for s in cands:
            hit = next((d for d in districts(country, s['SehirID']) if norm(d['IlceAdi']) == norm(district)), None)
            if hit:
                break
        if not hit:
            print('MISSING', name)
            continue
        save(slug, name, {'13': 'Almanya', '4': 'Hollanda', '11': 'Belçika', '35': 'Avusturya', '21': 'Fransa',
                          '49': 'İsviçre', '15': 'İngiltere'}[country], 'ABROAD', hit['IlceID'], table(hit['IlceID']))
        print('ABROAD', name)


if __name__ == '__main__':
    main()
