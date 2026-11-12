# ::ILANG
# [TYPE:test][PROJECT:vps-deals]
# ::ROLE{验证价格列选择 去重 过期失败隐藏 和I-Lang配置实际改变页面}
import copy
import json
import tempfile
import unittest
import shutil
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
from pathlib import Path
from config import ROOT, load_config
from scraper import extract
from build import fresh_offers, build, cost_analysis

NOW=datetime.now(timezone.utc).isoformat()
TABLE='''Basic Droplets<table><tr><th>Memory</th><th>vCPU</th><th>Transfer</th><th>SSD</th><th>$/hr</th><th>$/mo</th></tr><tr><td>1 GiB</td><td>1 vCPU</td><td>1,000 GiB</td><td>25 GiB</td><td>$0.00893</td><td><a href="https://cloud.digitalocean.com/new?size=s-1vcpu-1gb">$6.00</a></td></tr></table>'''
class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.cfg=load_config()
        # Synthetic parser fixture, independent of the live provider list.
        self.p={'id':'fixture','name':'Fixture Cloud','source':'https://example.com/prices',
                'adapter':'monthly_table','start':'Basic Droplets','plan_query':'size',
                'label':'Basic Droplet','currency':'USD','period':'month','region':'Test only'}
    def test_monthly_not_hourly_and_real_model(self):
        rows=extract(TABLE,self.p,NOW);self.assertEqual(rows[0]['price'],'6.00');self.assertEqual(rows[0]['model'],'s-1vcpu-1gb');self.assertNotIn('valid_until',rows[0])
    def test_ambiguous_monthly_is_rejected(self):
        self.assertEqual(extract(TABLE.replace('$6.00','Was $9.00 now $6.00'),self.p,NOW),[])
    def test_missing_model_is_rejected(self):
        self.assertEqual(extract(TABLE.replace('size=','wrong='),self.p,NOW),[])
    def test_unknown_table_fails_closed(self):
        with self.assertRaises(ValueError):extract(TABLE.replace('$/mo','Renewal'),self.p,NOW)
    def test_cost_scenarios_use_hourly_rate_and_monthly_base(self):
        row=extract(TABLE,self.p,NOW)[0];row['billing']={'reviewed_at':NOW}
        result=cost_analysis(row)
        for amount in ['7.20/month','7.80/month','USD 7.00','approximately USD 0.21']:
            self.assertIn(amount,result)
        self.assertIn('team-level excess',result)
    def test_failed_provider_has_no_page_link_or_sitemap_entry(self):
        data=json.loads((ROOT/'data/offers.json').read_text(encoding='utf-8'))
        for provider in data['providers']: provider['status']='error'
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'data').mkdir()
            (root/'data/offers.json').write_text(json.dumps(data),encoding='utf-8')
            for folder in ['templates','assets']:shutil.copytree(ROOT/folder,root/folder)
            with patch('build.ROOT',root):build(ROOT/'.ilang/site.ilang',root/'site')
            self.assertFalse((root/'site/providers').exists())
            self.assertNotIn('/providers/',(root/'site/index.html').read_text(encoding='utf-8'))
            self.assertNotIn('/providers/',(root/'site/sitemap.xml').read_text(encoding='utf-8'))
    def test_failure_stale_expiry_removed_and_deduped(self):
        row=extract(TABLE,self.p,NOW)[0]; data={'providers':[{'id':self.p['id'],'status':'ok'}],'offers':[row,row]}
        cfg=copy.deepcopy(self.cfg);cfg['providers']=[self.p]
        self.assertEqual(len(fresh_offers(cfg,data)),1)
        data['providers'][0]['status']='error';self.assertEqual(fresh_offers(cfg,data),[])
        data['providers'][0]['status']='ok';row['fetched_at']=(datetime.now(timezone.utc)-timedelta(hours=31)).isoformat();self.assertEqual(fresh_offers(cfg,data),[])
        row['fetched_at']=NOW;row['valid_until']=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat();self.assertEqual(fresh_offers(cfg,data),[])
    def test_config_removal_changes_built_site(self):
        cfg=copy.deepcopy(self.cfg);removed=cfg['providers'][0]['id'];cfg['providers']=cfg['providers'][1:]
        with tempfile.TemporaryDirectory() as td:
            config=Path(td)/'site.ilang';config.write_text('::ILANG\n::JSON_BEGIN\n'+json.dumps(cfg)+'\n::JSON_END',encoding='utf-8')
            output=Path(td)/'output'; report=build(config,output)
            data=json.loads((ROOT/'data/offers.json').read_text(encoding='utf-8'))
            self.assertEqual(report['providers'],len(self.cfg['providers'])-1);self.assertEqual(report['deals'],len(fresh_offers(cfg,data)))
            self.assertFalse((output/'providers'/removed).exists());self.assertNotIn('/providers/'+removed+'/',(output/'index.html').read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
