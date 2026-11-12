# ::ILANG
# [TYPE:code][PROJECT:vps-deals]
# ::ROLE{读取I-Lang与真实数据生成静态页面；只输出当前、未过期、已配置厂商的方案}
# ::BOUNDARY{never:编优惠幅度 截止日期 库存 评分 域名}
import argparse
import hashlib
import html
import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from string import Template
from decimal import Decimal, ROUND_HALF_UP
from xml.sax.saxutils import escape as xml_escape
from config import ROOT, load_config
from vultr_article import publish_vultr_article

def esc(x): return html.escape(str(x), quote=True)
def cost_analysis(o):
    price=Decimal(o['price']); hourly=Decimal(o['hourly_price'])
    def money(x): return format(x.quantize(Decimal('.01'),rounding=ROUND_HALF_UP),'.2f')
    docs='https://docs.digitalocean.com/products/droplets/details/pricing/'
    return '<section class="cost-scenarios"><h2>Our reproducible cost scenarios</h2><p>Authored calculations for this exact plan, not measured invoices or provider quotations. USD, before tax; no credits or other resources. Recalculate with the linked rates if terms change.</p><ol>'+''.join([
        '<li><h3>Monthly backup budget</h3><p>Base '+esc(o['price'])+' × 20% = '+money(price*Decimal('.2'))+' extra for basic weekly backups; total '+money(price*Decimal('1.2'))+'/month. Basic daily backups at 30% give '+money(price*Decimal('1.3'))+'/month. Usage-based backups are a separate option.</p><p>Source: <a href="https://docs.digitalocean.com/products/backups/details/pricing/#basic-plans">Backups Pricing, Basic Plans, paragraph 1 and Weekly/Daily table rows</a>; base: <a href="'+esc(o['source_url'])+'">Basic Regular table, model '+esc(o['model'])+'</a>.</p></li>',
        '<li><h3>Transfer overage budget</h3><p>Scenario: the team exceeds its accrued included outbound pool by 100 GiB. 100 × USD 0.01/GiB = USD 1.00 extra; this plan’s full base plus that charge = USD '+money(price+1)+'. This is team-level excess, not 100 GiB above an isolated VM allowance.</p><p>Source: <a href="'+docs+'#bandwidth-billing">Bandwidth Billing, paragraphs 1–2</a>; included transfer for this plan: '+esc(o['specs']['transfer'])+'.</p></li>',
        '<li><h3>Power-off is not cancellation</h3><p>Scenario: a newly created instance stays reserved but powered off for 24 hours, then is destroyed. 24 × USD '+esc(o['hourly_price'])+'/hour = approximately USD '+money(min(hourly*24,price))+', within the monthly base cap USD '+esc(o['price'])+'. The provider bills by seconds; the displayed hourly rate and cent rounding make this a budget estimate. Powering off saves no reserved compute charge; destroying ends future instance billing. Separate backups or other resources are outside this example.</p><p>Source: <a href="'+docs+'#bundled-cpu-droplet-billing">Bundled CPU Droplet Billing, paragraphs 1–2</a>; hourly input: <a href="'+esc(o['source_url'])+'">Basic Regular table, '+esc(o['model'])+', $/hr column</a>.</p></li>'
    ])+'</ol><p>Price observation: <time>'+esc(o['fetched_at'])+'</time>. Terms review: <time>'+esc(o['billing']['reviewed_at'])+'</time>. Section paragraph counts exclude headings and navigation.</p></section>'
def fresh_offers(cfg, data, now=None):
    now = now or datetime.now(timezone.utc)
    providers = {p['id'] for p in cfg['providers']}
    good = {p['id'] for p in data['providers'] if p['status']=='ok'}
    result = {}
    for o in data['offers']:
        date = datetime.fromisoformat(o['fetched_at'])
        if o['provider_id'] not in providers & good or not o.get('model'): continue
        if not 0 <= (now-date).total_seconds() <= cfg['max_age_hours']*3600: continue
        if o.get('valid_until') and datetime.fromisoformat(o['valid_until'].replace('Z','+00:00')) <= now: continue
        if not o.get('price') or float(o['price']) <= 0: continue
        result[(o['provider_id'],o['model'],o['currency'])] = o
    return list(result.values())

def build(config_path=None, output=None):
    cfg = load_config(config_path); data = json.loads((ROOT/'data/offers.json').read_text(encoding='utf-8'))
    offers = fresh_offers(cfg,data); base = cfg['base_url']; out = Path(output or ROOT/'site')
    # Only rebuild the explicit generated output, never touch source or unrelated directories.
    if out.resolve() == ROOT.resolve() or out.resolve() not in (ROOT.resolve()/'site',) and output is None:
        raise ValueError('Unsafe build output')
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT/'assets',out/'assets')
    asset_version = hashlib.sha256((ROOT/'assets/style.css').read_bytes()+(ROOT/'assets/ui.js').read_bytes()).hexdigest()[:12]
    month = datetime.now(timezone.utc).strftime('%B %Y'); checked = data['fetched_at']
    statuses = {p['id']:p for p in data['providers']}
    pages = []
    def url(path): return base + path
    def schema_offer(o):
        result = {'@type':'Offer','name':o['title'],'price':o['price'],'priceCurrency':o['currency'],
                  'url':url('/plans/'+o['id']+'/'), 'seller':{'@type':'Organization','name':next(p['name'] for p in cfg['providers'] if p['id']==o['provider_id'])}}
        if o.get('valid_until'): result['priceValidUntil'] = o['valid_until'][:10]
        # OnlineOnly describes the official purchase channel, not regional inventory.
        if o.get('billing'): result['availability'] = 'https://schema.org/OnlineOnly'
        return result
    def itemlist(items):
        return {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'url':url('/plans/'+o['id']+'/'),'name':o['title']} for i,o in enumerate(items)]}
    def template(filename,**values):
        return Template((ROOT/'templates'/filename).read_text(encoding='utf-8')).substitute(values)
    def page(path,title,desc,body,schemas=(),crumb=None,lastmod=checked):
        graph = list(schemas)
        if crumb:
            graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':url('/')},{'@type':'ListItem','position':2,'name':crumb,'item':url(path)}]})
        canonical = '<link rel="canonical" href="'+esc(url(path))+'">' if base else '<meta name="robots" content="noindex">'
        ld = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
        content = template('base.html',asset_version=asset_version,title=esc(title),description=esc(desc),brand=esc(cfg['brand']),body=body,
                           canonical=canonical,schema=ld,url=esc(url(path)),image=esc(url('/assets/og.png')),repository=esc(cfg['repository_url']))
        target = out / (path.strip('/')+'/index.html' if path!='/' else 'index.html')
        target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding='utf-8')
        pages.append((path,lastmod))
    def cards(items):
        if not items: return '<p class="empty">No current price verified. Check the official provider page.</p>'
        return ''.join(template('card.html',title=esc(o['title']),price=esc(o['price']),currency=esc(o['currency']),
                    specs=esc(' · '.join(o['specs'].values())),href='/plans/'+esc(o['id'])+'/',kind='Official list price',provider=esc(next(p['name'] for p in cfg['providers'] if p['id']==o['provider_id'])),model=esc(o['model']),memory=esc(o['specs']['memory']),cpu=esc(o['specs']['cpu']),disk=esc(o['specs']['disk']),transfer=esc(o['specs']['transfer'])) for o in items)
    active_providers = [p for p in cfg['providers'] if any(o['provider_id']==p['id'] for o in offers)]
    providers_html = ''.join('<a class="provider-chip" href="/providers/'+esc(p['id'])+'/">'+esc(p['name'])+' <span>'+str(sum(o['provider_id']==p['id'] for o in offers))+' prices</span></a>' for p in active_providers)
    maximum = max((float(o['price']) for o in offers), default=1)
    readout = ''.join('<li><span>'+esc(o['specs']['memory'])+'</span><meter min="0" max="'+str(maximum)+'" value="'+esc(o['price'])+'" aria-label="'+esc(o['title'])+': '+esc(o['currency'])+' '+esc(o['price'])+' per month">'+esc(o['price'])+'</meter><span>'+esc(o['currency'])+' '+esc(o['price'])+'</span></li>' for o in sorted(offers,key=lambda o:float(o['price'])))
    if not readout: readout = '<li class="readout-empty">Open a provider page to check current official prices.</li>'
    checked_label = datetime.fromisoformat(checked).strftime('%d %b %Y, %H:%M UTC')
    index_body = template('index.html',count=len(offers),provider_count=len(active_providers),checked=esc(checked),checked_label=esc(checked_label),providers=providers_html,cards=cards(offers),hours=cfg['update_hours'],readout=readout)
    page('/',f"{cfg['brand']} — VPS prices & cost analysis | {month}",f"Compare {len(offers)} source-linked VPS plans from official provider pages. Checked {month}; with source-linked billing terms.",index_body,[itemlist(offers)])
    for p in active_providers:
        items = [o for o in offers if o['provider_id']==p['id']]; status = statuses.get(p['id'],{})
        text = 'Current official prices verified.' if items else 'No current price verified. '+status.get('message','Provider has not been fetched yet.')
        body = template('provider.html',name=esc(p['name']),region=esc(p['region']),source=esc(p['source']),status=esc(text),checked=esc(status.get('checked_at','Not checked')),cards=cards(items))
        service = {'@type':'Service','name':p['name']+' VPS hosting','provider':{'@type':'Organization','name':p['name']},'url':url('/providers/'+p['id']+'/')}
        if items:
            prices = [float(o['price']) for o in items]
            service['offers'] = {'@type':'AggregateOffer','priceCurrency':items[0]['currency'],'lowPrice':str(min(prices)),'highPrice':str(max(prices)),'offerCount':len(items),'offers':[schema_offer(o) for o in items]}
        page('/providers/'+p['id']+'/',f"{p['name']} VPS prices — {len(items)} verified plans | {month}",f"{p['name']} official VPS pricing, source and verification status for {month}. Includes published monthly caps and billing scope.",body,[service],p['name'],status.get('checked_at',checked))
    for o in offers:
        p = next(p for p in cfg['providers'] if p['id']==o['provider_id'])
        image_path='/assets/plans/'+o['id']+'.svg'
        picture=out/image_path.lstrip('/'); picture.parent.mkdir(exist_ok=True)
        picture.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#f3f6f6"/><g fill="#142d26" font-family="sans-serif"><text x="64" y="110" font-size="38">'+esc(p['name'])+' · '+esc(o['model'])+'</text><text x="64" y="235" font-size="64">'+esc(o['specs']['memory'])+' · '+esc(o['specs']['cpu'])+'</text><text x="64" y="330" font-size="38">'+esc(o['specs']['disk'])+' SSD · '+esc(o['specs']['transfer'])+' transfer</text><text x="64" y="460" font-size="64">'+esc(o['currency'])+' '+esc(o['price'])+' / month cap</text><text x="64" y="555" font-size="30">Authored specification summary · not a hardware photograph</text></g></svg>',encoding='utf-8')
        sponsored = bool(p.get('affiliate_url')); target = p.get('affiliate_url') or o['offer_url']
        specs = ''.join('<div><dt>'+esc(k.title())+'</dt><dd>'+esc(v)+'</dd></div>' for k,v in o['specs'].items())
        billing = o.get('billing',{})
        billing_html = '<section><h2>Billing scope and evidence</h2><dl class="billing-list">'+''.join('<div><dt>'+esc(label)+'</dt><dd>'+esc(billing.get(key,'Not verified; confirm with provider.'))+'</dd></div>' for key,label in [('basis','Usage and monthly cap'),('tax','Tax'),('ipv4','Public IPv4'),('backup','Backups')])+'</dl><p>Terms reviewed: <time>'+esc(billing.get('reviewed_at','Not reviewed'))+'</time>. Paragraph numbers below are counted within the named section, excluding headings.</p><ul>'+''.join('<li><a href="'+esc(s['url'])+'">'+esc(s['location'])+'</a></li>' for s in billing.get('sources',[]))+'</ul></section>'
        body = template('deal.html',title=esc(o['title']),price=esc(o['price']),currency=esc(o['currency']),specs=specs,region=esc(o['region']),checked=esc(o['fetched_at']),
                        billing=billing_html+cost_analysis(o),plan_image=esc(image_path),
                        source=esc(o['source_url']),target=esc(target),rel='sponsored noopener' if sponsored else 'noopener',
                        disclosure='Affiliate link: we may earn a commission if you purchase.' if sponsored else 'Direct official link. No affiliate commission is configured for this provider.',provider_url='/providers/'+esc(p['id'])+'/')
        product = {'@type':'Product','name':o['title'],'image':[url(image_path)],'description':f"{p['name']} {o['model']}, {o['currency']} {o['price']} per month. Official list price; confirm checkout terms.",'brand':{'@type':'Brand','name':p['name']},'offers':schema_offer(o)}
        page('/plans/'+o['id']+'/',f"{o['title']} — {o['currency']} {o['price']}/mo | {month}",f"{o['title']}: {o['currency']} {o['price']}/month, official list price checked {month}. See specs, conditions and original source.",body,[product],o['model'],o['fetched_at'])
    rows = ''.join('<tr><td><a href="/plans/'+esc(o['id'])+'/">'+esc(o['title'])+'</a></td><td>'+esc(o['currency'])+' '+esc(o['price'])+'</td><td>'+esc(o['specs']['memory'])+'</td><td>'+esc(o['specs']['cpu'])+'</td><td>'+esc(o['specs']['disk'])+'</td></tr>' for o in sorted(offers,key=lambda o:float(o['price'])))
    page('/compare/',f"Compare official VPS prices | {month}",f"Compare source-linked VPS monthly prices and specifications, checked {month}. Taxes and optional services may add to the total.",template('compare.html',rows=rows),[itemlist(offers)],'Compare')
    method = '<section class="page-head"><h1>How we check prices</h1><p>We monitor official public pricing pages. This index records base prices and specifications, with separately labelled cost scenarios.</p></section><section class="prose"><h2>Verification and freshness</h2><p>The pipeline checks robots.txt, fetches the configured public page and maps a named plan to its monthly price. Unknown markup, fetch errors and ambiguous prices produce no current priced plan. Prices older than '+str(cfg['max_age_hours'])+' hours are removed at the next build. An already deployed static site cannot update if the schedule stops; read the timestamp and verify checkout.</p><h2>Costs and eligibility</h2><p>Amounts are provider list prices, not guaranteed quotes. Billing caps, hourly usage, location, tax, IPv4, backups and transfer overages can affect your bill. No account-specific credits are included in the estimates.</p><h2>Affiliate disclosure</h2><p>No affiliate approval or income is claimed. Direct links are used until an approved tracking link is configured. Sponsored links are labelled where shown.</p><h2>Privacy</h2><p>This site sets no analytics cookies and contains no tracking scripts. Filtering and sorting run on your device without sending your input to a server. Hosting and outbound providers process requests under their own policies.</p><h2>Corrections and source code</h2><p>Review public data, fetch statuses or report a problem in the <a href="'+esc(cfg['repository_url'])+'">GitHub project</a>.</p></section>'
    page('/methodology/',f"Methodology, disclosure & privacy | {cfg['brand']}",'How we verify official VPS prices, handle stale data and disclose affiliate links.',method,crumb='Methodology')
    error_body = '<section class="page-head"><h1>This page could not be found.</h1><p>The address may have changed. Return to the current plan list to continue comparing.</p><a class="button primary" href="/">View current plans</a></section>'
    (out/'404.html').write_text(template('base.html',asset_version=asset_version,title='Page not found | '+esc(cfg['brand']),description='Return to current verified VPS plans.',brand=esc(cfg['brand']),body=error_body,canonical='<meta name="robots" content="noindex">',schema='{"@context":"https://schema.org","@graph":[]}',url=esc(url('/404.html')),image=esc(url('/assets/og.png')),repository=esc(cfg['repository_url'])),encoding='utf-8')
    (out/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+base+'/sitemap.xml\n' if base else 'Disallow: /\n'),encoding='utf-8')
    pages.append(publish_vultr_article(out))
    entries = ''.join('<url><loc>'+xml_escape(url(path))+'</loc><lastmod>'+xml_escape(date)+'</lastmod></url>' for path,date in pages) if base else ''
    (out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+entries+'</urlset>',encoding='utf-8')
    (out/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n  Content-Security-Policy: default-src \'self\'; script-src \'self\' \'unsafe-inline\'; style-src \'self\'; img-src \'self\' data:; frame-ancestors \'none\'\n',encoding='utf-8')
    summary = {'pages':len(pages),'deals':len(offers),'providers':len(cfg['providers']),'base_url':base,'data_fetched_at':checked}
    (ROOT/'data/build-report.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary)); return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--config'); parser.add_argument('--output'); args=parser.parse_args(); build(args.config,args.output)
