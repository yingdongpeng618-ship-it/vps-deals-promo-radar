# ::ILANG
# [TYPE:code][PROJECT:vps-deals]
# ::ROLE{读取唯一I-Lang配置；校验厂商与URL；不维护备用硬编码清单}
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent

def load_config(path=None):
    text = Path(path or ROOT / '.ilang/site.ilang').read_text(encoding='utf-8-sig')
    match = re.search(r'::JSON_BEGIN\s*(.*?)\s*::JSON_END', text, re.S)
    if not match:
        raise ValueError('Missing I-Lang JSON configuration block')
    cfg = json.loads(match.group(1))
    if cfg['locale'] != 'en-US':
        raise ValueError('v1 templates support en-US only; add localized templates before changing locale')
    ids = [p['id'] for p in cfg['providers']]
    if len(ids) != len(set(ids)) or any(not re.fullmatch('[a-z0-9-]+', i) for i in ids):
        raise ValueError('Provider IDs must be unique URL-safe slugs')
    for p in cfg['providers']:
        for key in ('source', 'homepage', 'affiliate_url'):
            if p.get(key) and urlsplit(p[key]).scheme != 'https':
                raise ValueError('Provider URLs must use HTTPS')
    base = cfg['base_url'].rstrip('/')
    if base and (urlsplit(base).scheme != 'https' or not urlsplit(base).netloc):
        raise ValueError('base_url must be an actual HTTPS deployment URL')
    cfg['base_url'] = base
    return cfg
