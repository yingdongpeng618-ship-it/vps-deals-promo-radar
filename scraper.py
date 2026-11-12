# ::ILANG
# [TYPE:code][PROJECT:vps-deals]
# ::ROLE{按配置抓取官方公开来源；先检查robots；失败即关闭当前价格展示}
# ::BOUNDARY{never:绕证书 绕反爬 猜测价格 把普通价包装为优惠}
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
import urllib.robotparser
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, parse_qs, unquote
from config import ROOT, load_config

AGENT = 'VPSDealsBot/1.0'

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows = []; self.row = None; self.cell = None; self.link = ''; self.tables = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table': self.tables += 1
        if tag == 'tr' and self.tables: self.row = []
        if tag in ('td','th') and self.row is not None: self.cell = []; self.link = ''
        if tag == 'a' and self.cell is not None: self.link = attrs.get('href','')
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td','th') and self.cell is not None:
            self.row.append((' '.join(''.join(self.cell).split()), self.link)); self.cell = None
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None
        if tag == 'table': self.tables = max(0,self.tables-1)

def extract(html, p, now):
    if p['adapter'] == 'monitor_only': return []
    if p['adapter'] != 'monthly_table': raise ValueError('Unsupported adapter')
    # Scope to one named family, then the first actual table. Never parse arbitrary page numbers.
    start = html.find(p['start'])
    if start < 0: raise ValueError('Pricing family not found')
    # Text may appear in navigation; require the expected header and table to agree.
    tables = re.findall(r'<table\b.*?</table>', html[start:], re.S | re.I)
    selected = None
    for table in tables:
        parser = TableParser(); parser.feed(table)
        if parser.rows and [x[0] for x in parser.rows[0]] == ['Memory','vCPU','Transfer','SSD','$/hr','$/mo']:
            selected = parser.rows; break
    if selected is None: raise ValueError('Expected six-column monthly pricing table not found')
    offers = []
    for row in selected[1:]:
        if len(row) != 6: continue
        memory, cpu, transfer, disk, hourly, monthly = [x[0] for x in row]
        price = re.fullmatch(r'\$\s*(\d+\.\d{2})', monthly)
        link = row[-1][1]
        # Actual provider machine identifier is in the official purchase URL.
        decoded = unquote(unquote(link))
        model = re.search(r'(?:[?&])' + re.escape(p['plan_query']) + r'=([a-z0-9-]+)', decoded)
        if not price or not re.fullmatch(r'\$\d+\.\d+',hourly) or not model or not all((memory,cpu,disk)): continue
        model = model.group(1)
        title = p['name'] + ' ' + p['label'] + ' (' + model + ')'
        offer = {'provider_id':p['id'], 'model':model, 'title':title,
                 'price':price.group(1), 'hourly_price':hourly.removeprefix('$'), 'currency':p['currency'], 'period':p['period'],
                 'offer_url':p['source'], 'source_url':p['source'], 'fetched_at':now,
                 'kind':'standard', 'region':p['region'],
                 'specs':{'memory':memory,'cpu':cpu,'transfer':transfer,'disk':disk},
                 'evidence':{'monthly_cell':monthly,'model_url':link}}
        offer['id'] = p['id'] + '-' + model
        if p.get('billing'): offer['billing'] = p['billing']
        offers.append(offer)
    return list({(o['provider_id'],o['model'],o['currency']):o for o in offers}.values())

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent':AGENT,'Accept':'text/html,text/plain;q=0.9'})
    with urllib.request.urlopen(req, timeout=35) as response:
        if urlsplit(response.url).netloc != urlsplit(url).netloc:
            raise ValueError('Cross-host redirect requires source review')
        body = response.read(6_000_001)
        if len(body) > 6_000_000: raise ValueError('Response too large')
        return body.decode('utf-8', 'strict')

def scrape(cfg=None):
    cfg = cfg or load_config(); now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    records = []; offers = []
    for p in cfg['providers']:
        record = {'id':p['id'],'source_url':p['source'],'checked_at':now,'status':'error'}
        try:
            root = urlsplit(p['source']); robots_url = root.scheme + '://' + root.netloc + '/robots.txt'
            try: robots = fetch(robots_url)
            except urllib.error.HTTPError as error:
                if error.code != 404: raise
                robots = ''
            rp = urllib.robotparser.RobotFileParser(); rp.parse(robots.splitlines())
            record['robots_url'] = robots_url
            record['robots_sha256'] = hashlib.sha256(robots.encode()).hexdigest()
            if not rp.can_fetch(AGENT, p['source']): raise ValueError('robots.txt disallows this bot')
            delay = rp.crawl_delay(AGENT) or rp.crawl_delay('*') or 1
            if delay > 60: raise ValueError('Crawl delay exceeds v1 budget')
            time.sleep(delay)
            html = fetch(p['source'])
            record['source_sha256'] = hashlib.sha256(html.encode()).hexdigest()
            extracted = extract(html,p,now)
            offers.extend(extracted); record['offer_count'] = len(extracted)
            record['status'] = 'ok' if extracted else 'unpriced'
            record['message'] = 'Official price table parsed' if extracted else 'No current price verified by the configured adapter; consult official source.'
        except Exception as error:
            record['message'] = type(error).__name__ + ': ' + str(error)
        records.append(record)
    result = {'fetched_at':now,'providers':records,'offers':offers}
    (ROOT/'data').mkdir(exist_ok=True)
    (ROOT/'data/offers.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'providers':len(records),'offers':len(offers),'statuses':{r['id']:r['status'] for r in records}}))
    # Publishing an empty current set removes stale prices when all sources fail.
    return result

if __name__ == '__main__': scrape()
