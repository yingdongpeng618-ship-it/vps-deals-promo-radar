"""Publish a dated, official-source Hetzner editorial check and the pricing directory."""
from linode_article import publish_document

CHECKED = '2026-11-13T07:39:52.145Z'
CHECK_LABEL = '2026-11-13 07:39'
PRICES = 'https://www.hetzner.com/cloud/regular-performance/'
COST_PRICES = 'https://www.hetzner.com/cloud/cost-optimized/'
BILLING = 'https://docs.hetzner.com/cloud/billing/faq/'
IPS = 'https://docs.hetzner.com/general/infrastructure-and-availability/ipv4-pricing/'

def table(headers, rows, label):
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="'+label+', scroll horizontally"><table><thead><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def body():
    cx_plans = [
        ('CX23','NBG1 / HEL1',2,4,40,'5.99','0.0096'),
        ('CX33','NBG1 / HEL1',4,8,80,'8.99','0.0144'),
        ('CX43','NBG1 / HEL1',8,16,160,'16.49','0.0264'),
        ('CX53','NBG1 / HEL1',16,32,320,'29.99','0.0481'),
    ]
    plans = [
        ('CPX02','HEL1',1,1,20,'5.49','0.0088'),
        ('CPX12','HEL1',1,2,40,'9.99','0.0160'),
        ('CPX22','HEL1',2,4,80,'16.99','0.0272'),
        ('CPX32','HEL1',4,8,160,'30.49','0.0489'),
        ('CPX42','HEL1',8,16,320,'59.49','0.0953'),
        ('CPX52','HEL1',12,24,480,'85.49','0.1370'),
        ('CPX62','HEL1',16,32,640,'110.99','0.1779'),
        ('CPX11','ASH1 / HIL1',2,2,40,'17.99','0.0288'),
        ('CPX21','ASH1 / HIL1',3,4,80,'32.49','0.0521'),
        ('CPX31','ASH1 / HIL1',4,8,160,'62.99','0.1009'),
        ('CPX41','ASH1 / HIL1',8,16,240,'120.99','0.1939'),
        ('CPX51','ASH1 / HIL1',16,32,360,'238.49','0.3822'),
    ]
    result = '''<h1>Hetzner pricing: CX and CPX €5.49 to €238.49/month</h1>
<p><strong>The checked Hetzner Cloud cards range from €5.99 to €29.99/month for CX and from €5.49 to €238.49/month for CPX, including Primary IPv4 and excluding VAT.</strong> Across both families the observed range is €5.49–€238.49/month. The entry CPX02 in Helsinki is €5.49/month or €0.0088/hour; the entry CX23 is €5.99/month or €0.0096/hour on the NBG1/HEL1 card. At capture time every CX card was labelled “not available” and its Create control said “This product is currently unavailable. Please check back later.”; the prices are the displayed card quotes, not a stock guarantee. Turning a server off does not stop billing; deletion does. <a href="https://www.hetzner.com/cloud/cost-optimized/">Official CX cards</a> · <a href="https://www.hetzner.com/cloud/regular-performance/">Official CPX cards</a>.</p>
<h2>Hetzner Cloud pricing: CX (Cost-Optimized) full lineup</h2>
<p>Scope: shared Cost-Optimized, EUR, the website's 0% VAT selection. The CX card lists NBG1 and HEL1 at the same monthly price. Every CX row below carried the label “not available” at capture time; availability for a new order is <strong>Not obtained</strong>. Prices are copied from the card's monthly and hourly cells.</p>'''
    result += table(['SKU','Quote location','vCPU','RAM GB','NVMe GB','EUR/month cap, IPv4 included','EUR/hour displayed','Checked (UTC)'],[[p[0],p[1],p[2],p[3],p[4],'€'+p[5],'€'+p[6],CHECK_LABEL] for p in cx_plans],'Cost-Optimized CX prices')
    result += '''<p>Data from <a href="https://www.hetzner.com/cloud/cost-optimized/">Hetzner official Cost-Optimized page → CX rows: CPU, RAM, drive, from/month and /hour cells</a>. Checked 2026-11-13 07:39 UTC. The card's detail price is tied to <code>location="NBG1,HEL1"</code>; the Create link uses <code>location=hel1</code>. VAT excluded. These are card observations, not a converted currency or a monthly price divided by assumed hours.</p>
<h2>Hetzner Cloud pricing: CPX (Regular Performance) full lineup</h2>
<p>Scope: shared AMD Regular Performance only, EUR, the website's 0% VAT selection. Each row preserves the location behind the displayed minimum. The US generation has different CPU and disk allocations; it is not a regional replacement price for the European SKU.</p>'''
    result += table(['SKU','Quote location','vCPU','RAM GB','NVMe GB','EUR/month cap, IPv4 included','EUR/hour displayed','Checked (UTC)'],[[p[0],p[1],p[2],p[3],p[4],'€'+p[5],'€'+p[6],CHECK_LABEL] for p in plans],'Regular Performance prices')
    result += '''<p>Data from <a href="https://www.hetzner.com/cloud/regular-performance/">Hetzner official Regular Performance page → CPX rows: CPU, RAM, drive, from/month and /hour cells</a>. Checked 2026-11-13 07:39 UTC. Footer on the matrix: “Price incl. IPv4”; VAT excluded. These are card observations, not a converted currency or a monthly price divided by assumed hours.</p>
<h2>CPX: same SKU, different location and traffic allowance</h2>'''
    result += table(['SKU','Network zone','Location labels on card','Monthly quote incl. IPv4','Included traffic','Difference from HEL1','Checked (UTC)'],[
        ['CPX02','eu-central','HEL1','€5.49','20 TB','€0.00 = €5.49 − €5.49',CHECK_LABEL],
        ['CPX02','eu-central','FSN1 / NBG1','€6.49','20 TB','€1.00 = €6.49 − €5.49',CHECK_LABEL],
        ['CPX02','ap-southeast','SIN1','€7.99','0.5 TB','€2.50 = €7.99 − €5.49',CHECK_LABEL],
        ['CPX11 (different SKU)','us-east','ASH1','€17.99','1 TB','Not a same-SKU comparison',CHECK_LABEL],
        ['CPX11 (different SKU)','us-west','HIL1','€17.99','1 TB','Not a same-SKU comparison',CHECK_LABEL],
    ],'Regional quotes and included traffic')
    result += '''<p>Data from <a href="https://www.hetzner.com/cloud/regular-performance/">Hetzner official Regular Performance page → expanded CPX02 and CPX11 location rows</a>. Checked 2026-11-13 07:39 UTC. Difference cells are our subtraction of the linked monthly inputs. Labels above reproduce the public card's uppercase labels; the Console may use lower-case identifiers. Availability for a new order: <strong>Not obtained</strong>; a successful location-specific order check is needed. The official <a href="https://docs.hetzner.com/cloud/general/locations/">Locations → Which cloud products are available?</a> warns that instances can be unavailable.</p>
<p>The allowance changes with the selected plan and location; it is not a global allowance quoted identically everywhere. A cross-server or cross-zone shared allowance pool was <strong>Not obtained</strong>; explicit pooling documentation is needed before offsetting one server's usage with another server's unused allowance. The <a href="https://docs.hetzner.com/cloud/billing/faq/">Billing FAQ → How do you bill for traffic?</a> distinguishes outgoing traffic from free incoming/internal traffic and counts public traffic between different network zones as outgoing.</p>
<h2>Three location-sensitive checks before ordering</h2>
<section data-authored-calculation="regional"><p><strong>Our assumption:</strong> one CPX02 exists through twelve complete capped months, unchanged rates, no tax or optional services. Helsinki: 12 × <a href="https://www.hetzner.com/cloud/regular-performance/">€5.49</a> = €65.88. German location: 12 × <a href="https://www.hetzner.com/cloud/regular-performance/">€6.49</a> = €77.88. Singapore: 12 × <a href="https://www.hetzner.com/cloud/regular-performance/">€7.99</a> = €95.88. Location alone changes this model by €12.00 or €30.00 per year relative to Helsinki. This compares the same SKU, not the US CPX11.</p>
<p><strong>Our assumption:</strong> a full-month server sends 0.6 TB of chargeable outgoing traffic. Using the <a href="https://www.hetzner.com/cloud/regular-performance/">CPX02 location allowances</a>, Helsinki's excess = max(0, 0.6 − 20) = 0 TB; Singapore's excess = max(0, 0.6 − 0.5) = 0.1 TB. The current region-specific overage rate is <strong>Not obtained</strong>; a current official EUR/TB quote for each zone is needed to turn that excess into money. Do not copy a dedicated-server rate into a Cloud calculation.</p>
<p>The <a href="https://docs.hetzner.com/robot/general/traffic/">Traffic → Exceeding traffic</a> section specifies 100 MB = 0.0001 TB billing blocks. With the <a href="https://docs.hetzner.com/cloud/billing/faq/">Billing FAQ's upward-rounding rule</a>, the formula is ceil(max(0, outgoing TB − allowance TB) / 0.0001) × 0.0001 × regional EUR/TB. In our Singapore scenario: ceil(0.1 / 0.0001) = 1,000 blocks. The missing rate remains a missing input, not zero.</p></section>
<h2>IPv4, backups and retained resources</h2>'''
    result += table(['Resource','Official rate / basis','Evidence location'],[
        ['Primary IPv4','€0.50/month; separately billed','IP pricing → Cloud'],
        ['Primary IPv6','Free','IP pricing → Cloud'],
        ['Floating IPv4','€3.00/month','IP pricing → Cloud'],
        ['Floating IPv6','€1.00/month','IP pricing → Cloud'],
        ['Server backups','20% of server price; 7 slots','Billing FAQ → Snapshots and Backups'],
        ['Snapshot stored data','€0.0143/GB-month','Regular Performance → Snapshots add-on'],
        ['Volume storage','Not obtained: conflicting unit text and calculator; consistent quote needed','Block Storage → Volumes'],
    ],'Separate resources and backup basis')
    result += '''<p>Data from Hetzner official pages: <a href="https://docs.hetzner.com/general/infrastructure-and-availability/ipv4-pricing/">IP pricing → Cloud table</a>, <a href="https://docs.hetzner.com/cloud/billing/faq/">Billing FAQ → How do you bill for Snapshots and Backups?</a>, <a href="https://www.hetzner.com/cloud/regular-performance/">Regular Performance → Snapshots</a> and <a href="https://www.hetzner.com/cloud/block-storage/">Block Storage → Volumes unit text and calculator</a>. Checked 2026-11-13 07:39 UTC. The IPv4 fee is already included in the plan cards above; do not add it again. Primary IPv4 and Floating IPv4 are different resources.</p>
<section data-authored-calculation="backup"><p>Backup formula: B = P × 20%, where P is the chargeable server-price basis confirmed for the chosen order. <strong>Our assumption:</strong> P = €10.00, purely to illustrate the rule, not a published plan quote. B = €10.00 × 0.20 = €2.00/month. The percentage comes from <a href="https://docs.hetzner.com/cloud/billing/faq/">Billing FAQ → Snapshots and Backups, second paragraph</a>. The public page's backup starting widget does not resolve the separately billed IPv4 basis, so the exact CPX02 backup invoice amount is <strong>Not obtained</strong>; a selected-order backup quote is needed.</p>
<p><strong>Our assumption:</strong> retain 20 GB of compressed snapshot data for a complete month, plus one unassigned Primary IPv4 and one Floating IPv4. Snapshot = 20 × <a href="https://www.hetzner.com/cloud/regular-performance/">€0.0143</a> = €0.286; IPs = <a href="https://docs.hetzner.com/general/infrastructure-and-availability/ipv4-pricing/">€0.50 + €3.00</a> = €3.50; subtotal = €3.786 before invoice rounding and tax. Deleting the VM alone does not mean these retained resources disappear. Check their deletion separately. The <a href="https://docs.hetzner.com/cloud/billing/faq/">Billing FAQ → Primary IPs</a> expressly bills unassigned IPs; its snapshot section charges compressed stored size. Retaining an allocated volume adds an unquoted charge, and <a href="https://docs.hetzner.com/cloud/volumes/overview/">Volumes → Resources and attributes</a> excludes attached volumes from server backups and snapshots.</p></section>
<h2>Short runs and year-one versus year-two budgets</h2>
<section data-authored-calculation="duration"><p>For the server resource, C = min(monthly cap, hourly rate × ceil(existence hours)). The <a href="https://docs.hetzner.com/cloud/billing/faq/">Billing FAQ → How do you bill your servers?</a> supplies the minimum and rounding rules. A lower bill requires fewer billable existence hours; stopping the OS does not shorten existence. A location-specific compute-only hourly and cap quote was <strong>Not obtained</strong> separately from the IPv4-inclusive public card, so we do not present the latter as a server-only invoice.</p>
<p><strong>Our assumption:</strong> a server-only quote has an hourly rate h and cap M. A job retained for 24 hours and one minute has ceil(24 + 1/60) = 25 billed hours, so C = min(M, 25h). It stays below the cap exactly when 25h &lt; M. The duration is our scenario; h and M must come from the same selected configuration. The symbols deliberately avoid inventing a missing quote.</p>
<p><strong>No first-year discount is shown in the checked CX or CPX cards.</strong> This describes the observed offer, not a promise about every account or future campaign. Our assumption of twelve full capped months at the unchanged Helsinki IPv4-inclusive card rate gives year one = 12 × <a href="https://www.hetzner.com/cloud/regular-performance/">€5.49</a> = €65.88; year two under the same assumption = €65.88; difference = €0.00. A guaranteed future renewal tariff is <strong>Not obtained</strong>; future official pricing is needed. Do not treat our unchanged-rate scenario as a renewal quote.</p></section>
<h2>Who should use this Hetzner VPS pricing guide?</h2>
<p>Use the CX table when the lowest shared monthly cap is the priority and the Cost-Optimized generation fits; use the CPX table when newer shared AMD performance matters and you can choose where it runs. Check other families separately for dedicated CPU or ARM requirements. If you need an exact tax-inclusive checkout total, an assured in-stock order, a current overage invoice or volume budget, the missing inputs below must be resolved before ordering.</p>
<h2>What was not obtained</h2>
<ul><li>CX availability: every CX card was labelled “not available” at capture time; a successful selected-location order check is required.</li><li>Live order availability: requires a successful selected-location stock check.</li><li>Regional traffic overage unit prices and allowance-pooling rules: require current explicit Cloud billing terms for the selected zone.</li><li>Consistent volume unit price: requires reconciliation of the official unit text and calculator. No volume amount is included in our totals.</li><li>Exact CPX02 backup billing basis and compute-only hourly/cap quote: require the selected-order breakdown.</li><li>Future renewal tariff and account-specific tax/credit total: require future rates and the account checkout.</li></ul>
<p>Every item in this list is <strong>Not obtained</strong>, rather than N/A or an assumed zero. No third-party number fills these gaps.</p>
<h2>Official sources and check date</h2>
<p>Official public prices and documentation checked 2026-11-13 07:39 UTC. CX prices were read from <a href="https://www.hetzner.com/cloud/cost-optimized/">Hetzner Cloud Cost-Optimized</a>; CPX prices from <a href="https://www.hetzner.com/cloud/regular-performance/">Hetzner Cloud Regular Performance</a>. This is a dated editorial observation, not an automatically refreshed feed. Source sections are linked at each table and calculation. Arithmetic results are our calculations; hypothetical inputs are labelled our assumption.</p>
<p><a href="/">Home</a> · <a href="/pricing/">Pricing guide index</a> · <a href="/compare/">Compare published plans</a></p>'''
    return result

GUIDES = [('vultr','Vultr'),('hostinger-vps','Hostinger VPS'),('azure-virtual-server','Azure virtual server'),('digitalocean','DigitalOcean'),('linode','Linode / Akamai'),('aws-lightsail','AWS Lightsail'),('hetzner','Hetzner')]

def publish_hetzner(output, cfg):
    return publish_document(output,cfg,'/pricing/hetzner/','Hetzner pricing: CX and CPX €5.49–€238.49/month','Official Hetzner Cloud CX and CPX monthly and hourly quotes, regional prices, traffic allowances, IPv4, backups and retained-resource calculations.',body(),CHECKED)

def publish_pricing_index(output,cfg):
    content='<section class="page-head"><h1>Provider pricing guides</h1><p>Choose a provider to check the official source, the observation date and the billing details behind its headline rate.</p></section><section class="prose"><ul>'+''.join('<li><a href="/pricing/'+slug+'/">'+name+' pricing</a></li>' for slug,name in GUIDES)+'</ul><p>Each guide keeps its own source-check date. This directory was updated when the Hetzner guide was added.</p><p><a href="/">Home</a> · <a href="/compare/">Compare published plans</a></p></section>'
    return publish_document(output,cfg,'/pricing/','Provider pricing guides','Official-source cloud pricing guides and worked billing checks.',content,CHECKED)
