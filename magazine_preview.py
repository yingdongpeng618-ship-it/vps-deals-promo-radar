"""Isolated visual preview for home and Hostinger only; a main-branch build is never restyled."""
from pathlib import Path
from datetime import datetime
from html import escape
import json
import os
import re


def apply_preview(output, cfg, data, offers):
    if os.environ.get('CF_PAGES_BRANCH', 'codex/magazine-theme-preview') != 'codex/magazine-theme-preview' or not offers:
        return
    root = Path(output)
    (root/'assets/magazine.css').write_text(STYLES, encoding='utf-8')
    (root/'assets/magazine.js').write_text(SCRIPT, encoding='utf-8')
    original_home=(root/'index.html').read_text(encoding='utf-8')
    old_host=(root/'pricing/hostinger-vps/index.html').read_text(encoding='utf-8')
    def head(original):
        h=re.search(r'<head>(.*?)</head>',original,re.S).group(1)
        h=re.sub(r'<link rel="stylesheet"[^>]*>', '<link rel="stylesheet" href="/assets/magazine.css">', h)
        h=re.sub(r'<script src="[^"]+"[^>]*></script>', '',h)
        return h+'<meta name="robots" content="noindex,nofollow"><meta name="color-scheme" content="light"><script src="/assets/magazine.js" defer></script>'
    def shell(original, content, active):
        return '<!doctype html><html lang="en-US"><head>'+head(original)+'</head><body class="'+active+'"><a class="skip" href="#main">Skip to content</a>'+HEADER+'<main id="main">'+content+'</main>'+FOOTER+'</body></html>'
    items=sorted(offers,key=lambda o:float(o['price']))
    first=items[0]
    checked=datetime.fromisoformat(data['fetched_at']).strftime('%d %b %Y, %H:%M UTC')
    money=lambda s: escape(str(s))
    first_url='/plans/'+escape(first['id'])+'/'
    hero='''<section class="home-hero"><div class="hero-copy"><h1>VPS prices,<br>in perspective.</h1></div><div class="cover-intro"><p>Compare official monthly prices with memory, compute and storage in the same place.</p><p>Then read the billing details: what you pay upfront, what renews, and what can change the bill.</p><a class="button primary" href="#plans">Explore verified plans '''+ARROW+'''</a></div><div class="price-brief"><div><p class="brief-name">DigitalOcean Basic</p><p class="brief-spec">Lowest listed monthly cap</p></div><p class="brief-price">USD '''+money(first['price'])+''' <span>/ month</span></p><p class="brief-spec">'''+escape(first['specs']['memory'])+' &middot; '+escape(first['specs']['cpu'])+' &middot; '+escape(first['specs']['disk'])+''' SSD</p><a href="'''+first_url+'''">Read the plan '''+ARROW+'''</a></div></section><div class="observation-line"><p>DigitalOcean observations checked <time datetime="'''+escape(data['fetched_at'])+'">'+checked+'''</time></p><a href="https://www.digitalocean.com/pricing/droplets">View the official source '''+ARROW+'''</a></div>'''
    rows=''
    for o in items:
        s=o['specs'];url='/plans/'+escape(o['id'])+'/'
        search=escape(' '.join([o['title'],o['model']]+list(s.values())),quote=True)
        rows+='<tr class="plan" data-price="'+escape(o['price'])+'" data-memory="'+escape(s['memory'])+'" data-search="'+search+'"><td><a class="plan-name" href="'+url+'">'+escape(s['memory'])+'</a><span class="row-detail">DigitalOcean Basic Regular</span></td><td>'+escape(s['cpu'])+'</td><td>'+escape(s['disk'])+'<span class="row-detail">SSD</span></td><td>'+escape(s['transfer'])+'</td><td class="numeric"><span class="money">$'+escape(o['price'])+'</span><span class="row-detail">USD / month cap</span></td><td><a class="inspect" href="'+url+'" aria-label="Inspect '+escape(o['title'])+'">Inspect '+ARROW+'</a></td></tr>'
    controls='''<form class="plan-controls" data-controls hidden role="search" aria-label="Filter verified plans"><label>Find a plan<input name="query" type="search" placeholder="Search memory or plan" autocomplete="off"></label><label>Monthly budget, USD<input name="budget" type="number" min="0" step="any" inputmode="decimal" placeholder="Any amount" aria-describedby="filter-error"></label><label>Sort by<select name="sort"><option value="price">Lowest monthly price</option><option value="memory">Most memory</option></select></label><button type="reset" class="button secondary" disabled>Reset</button><p id="filter-error" class="field-error" role="alert" hidden>Enter a monthly budget of 0 or more.</p></form>'''
    plans='<section id="plans" class="plan-section"><div class="section-heading"><div><h2>Published VPS prices</h2><p>Base prices from DigitalOcean. Taxes and optional services may add to the total.</p></div><a href="https://vpscostlens.com/compare/">Full comparison '+ARROW+'</a></div>'+controls+'<p class="results-label" data-result-count role="status" aria-live="polite">'+str(len(items))+' plans listed</p><div class="table-wrap plan-table" tabindex="0" role="region" aria-label="DigitalOcean monthly price table, scroll horizontally"><table><thead><tr><th scope="col">Memory & plan</th><th scope="col">Compute</th><th scope="col">Storage</th><th scope="col">Transfer</th><th scope="col" class="numeric">Monthly cap</th><th scope="col"><span class="sr-only">Details</span></th></tr></thead><tbody data-plan-list>'+rows+'</tbody></table></div><p class="mobile-table-hint">Scroll the table sideways to see all specifications.</p><div class="no-results" data-no-results hidden><h3>No plans match your filters.</h3><p>Increase the budget or clear the search to see the available plans.</p><button type="button" class="button secondary" data-clear>Clear filters</button></div><noscript><p>All verified plans are shown. Browser JavaScript is needed only for filtering and sorting.</p></noscript></section>'
    guides='''<section class="guides-section" id="guides"><div class="guides-intro"><h2>Look beyond the headline price.</h2><p>Different billing models need different questions. Open a guide to check the terms behind the number.</p></div><div class="guide-list"><a href="https://vpscostlens.com/pricing/vultr/"><div><h3>Vultr</h3><p>Plan rates, regional prices and backups</p></div>'''+ARROW+'''</a><a href="/pricing/hostinger-vps/"><div><h3>Hostinger VPS</h3><p>Prepaid totals and renewal cash flow</p></div>'''+ARROW+'''</a><a href="https://vpscostlens.com/pricing/azure-virtual-server/"><div><h3>Azure virtual server</h3><p>Region, SKU and the cost of a VM state</p></div>'''+ARROW+'''</a></div></section><section class="verification-section"><div><h2>Keep the source close.</h2><p>Each plan links to the provider’s own pricing page. We publish a price only when it can be mapped to a real plan.</p></div><div><p>Checks are scheduled every '''+str(cfg['update_hours'])+''' hours. Schedules can fail; use the check date and confirm the provider’s checkout.</p><a href="https://vpscostlens.com/methodology/">Read the verification method '''+ARROW+'''</a></div></section>'''
    (root/'index.html').write_text(shell(original_home,hero+plans+guides,'home-page'),encoding='utf-8')
    body=re.search(r'<main>(.*?)</main>',old_host,re.S).group(1)
    first_heading=re.match(r'(<h1>.*?</h1>)(<p>.*?</p>)(.*)',body,re.S)
    assert first_heading
    h1,answer,rest=first_heading.groups()
    h1=h1.replace('hostinger vps pricing','Hostinger VPS pricing')
    chunks=re.split(r'(?=<h2>)',rest)
    sections=[];toc=[]
    for i,chunk in enumerate(chunks):
        if not chunk:continue
        title=re.search(r'<h2>(.*?)</h2>',chunk,re.S)
        if not title:sections.append(chunk);continue
        sid='section-'+str(len(toc)+1)
        toc.append((sid,title.group(1)))
        chunk=chunk.replace('<div class="table-wrap">','<div class="table-wrap" tabindex="0" role="region" aria-label="'+escape(title.group(1),quote=True)+' table, scroll horizontally">')
        sections.append('<section class="article-section" id="'+sid+'">'+chunk+'</section>')
    contents='<aside class="article-index"><details class="contents"><summary>On this page</summary><nav aria-label="On this page">'+''.join('<a href="#'+sid+'">'+title+'</a>' for sid,title in toc)+'</nav></details><a class="back-home" href="/">All VPS prices '+ARROW+'</a></aside>'
    content='<section class="article-hero">'+h1+'<div class="article-answer">'+answer+'</div><p class="article-context">Prepaid pricing · Renewal cash flow · Official-source evidence</p></section><div class="article-layout">'+contents+'<article class="article-body">'+''.join(sections)+'</article></div>'
    new_host=shell(old_host,content,'article-page')
    # All original price occurrences, arithmetic, source strings and timestamps stay in the article.
    assert re.findall(r'\$[\d,.]+',new_host)==re.findall(r'\$[\d,.]+',old_host)
    for quote in re.findall(r'<q>(.*?)</q>',old_host,re.S):assert '<q>'+quote+'</q>' in new_host
    for time in re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC',old_host):assert time in new_host
    (root/'pricing/hostinger-vps/index.html').write_text(new_host,encoding='utf-8')
    (root/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf-8')
    headers=(root/'_headers').read_text(encoding='utf-8')
    (root/'_headers').write_text(headers.replace('/*\n','/*\n  X-Robots-Tag: noindex, nofollow\n',1),encoding='utf-8')


ARROW='<svg class="arrow" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
HEADER='''<header class="site-header"><a class="brand" href="/"><span>VPS Cost Lens</span></a><nav aria-label="Main navigation"><a href="/#plans">Prices</a><a href="/#guides">Pricing guides</a><a href="https://vpscostlens.com/methodology/">Methodology</a></nav><span class="preview-label">Magazine preview</span></header>'''
FOOTER='''<footer class="site-footer"><div><a class="brand" href="/">VPS Cost Lens</a><p>Independent VPS price observations.<br>Confirm costs and availability with the provider.</p></div><div class="preview-links"><p>This is a visual preview. The production site is unchanged.</p><a href="/">Homepage preview</a><a href="/pricing/hostinger-vps/">Hostinger preview</a></div></footer>'''

STYLES=Path(__file__).with_name('magazine.css').read_text(encoding='utf-8')

SCRIPT=r'''
/* Preview-only, local filtering; observations are rendered by the existing builder. */
(() => {
  const contents=document.querySelector('.contents');
  if(contents){const mq=matchMedia('(min-width:761px)');contents.open=mq.matches;mq.addEventListener('change',e=>contents.open=e.matches)}
  const form=document.querySelector('[data-controls]'),list=document.querySelector('[data-plan-list]');
  if(!form||!list)return;
  const plans=[...list.querySelectorAll('.plan')],query=form.elements.query,budget=form.elements.budget,sort=form.elements.sort;
  const reset=form.querySelector('[type="reset"]'),error=document.querySelector('#filter-error'),empty=document.querySelector('[data-no-results]'),count=document.querySelector('[data-result-count]');
  const memory=p=>{const s=p.dataset.memory.toLowerCase();return parseFloat(s)*(s.includes('gib')||s.includes('gb')?1024:1)};
  function update(){
    const invalid=!budget.validity.valid;error.hidden=!invalid;budget.setAttribute('aria-invalid',String(invalid));
    const limit=budget.value===''||invalid?Infinity:Number(budget.value),term=query.value.trim().toLowerCase();
    const ordered=[...plans].sort(sort.value==='memory'?(a,b)=>memory(b)-memory(a)||Number(a.dataset.price)-Number(b.dataset.price):(a,b)=>Number(a.dataset.price)-Number(b.dataset.price));
    let n=0;ordered.forEach(p=>{p.hidden=!(p.dataset.search.toLowerCase().includes(term)&&Number(p.dataset.price)<=limit);if(!p.hidden)n++;list.append(p)});
    empty.hidden=n!==0;count.textContent=`${n} of ${plans.length} plans shown`;reset.disabled=!query.value&&!budget.value&&sort.value==='price';
  }
  form.hidden=false;form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('input',update);form.addEventListener('change',update);
  form.addEventListener('reset',()=>setTimeout(update,0));document.querySelector('[data-clear]').addEventListener('click',()=>{form.reset();query.focus()});update();
})();
'''
