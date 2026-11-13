# ::ILANG
# [TYPE:code][PROJECT:vps-deals]
# ::ROLE{校验生成站点的内链 canonical JSON-LD与sitemap数量；不声称代替谷歌在线测试}
import json
import re
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit
from build import fresh_offers
from config import ROOT, load_config

def verify():
    cfg=load_config(); root=ROOT/'site'; data=json.loads((ROOT/'data/offers.json').read_text(encoding='utf-8'))
    measurement_id=cfg.get('analytics',{}).get('measurement_id','')
    if measurement_id:
        for html in root.rglob('*.html'):
            source=html.read_text(encoding='utf-8')
            assert source.count('https://www.googletagmanager.com/gtag/js?id='+measurement_id)==1,html
            assert source.count("gtag('config', '"+measurement_id+"')")==1,html
        headers=(root/'_headers').read_text(encoding='utf-8')
        assert 'https://www.googletagmanager.com' in headers
        assert 'https://*.google-analytics.com' in headers
    offers=fresh_offers(cfg,data); pages=list(root.rglob('index.html'))
    sitemap=ET.parse(root/'sitemap.xml'); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[x.text for x in sitemap.findall('.//s:loc',ns)]
    if cfg['base_url']:
        assert len(urls)==len(pages),(len(urls),len(pages))
        assert sum('/plans/' in u for u in urls)==len(offers)
        assert all(u.startswith(cfg['base_url']+'/') for u in urls)
    for path in pages:
        s=path.read_text(encoding='utf-8'); rel=path.relative_to(root).as_posix(); route='/'+rel[:-10]
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S): json.loads(block)
        if cfg['base_url']:
            canonical=re.findall(r'<link rel="canonical" href="([^"]+)">',s)
            assert canonical==[cfg['base_url']+route],(path,canonical,route)
        for href in re.findall(r'(?:href|src)="([^"]+)"',s):
            href=unescape(href)
            if href.startswith('/') and not href.startswith('//'):
                target=root/urlsplit(href).path.lstrip('/')
                assert target.is_file() or (target/'index.html').is_file(),(path,href)
    print(json.dumps({'verified_pages':len(pages),'verified_deals':len(offers),'sitemap_urls':len(urls),'canonical_mode':'production' if cfg['base_url'] else 'local-noindex'}))
if __name__=='__main__': verify()
