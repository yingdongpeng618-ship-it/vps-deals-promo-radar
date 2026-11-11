# ::ILANG
# [TYPE:test][PROJECT:vps-deals]
# ::ROLE{验证价格列选择 去重 过期失败隐藏 和I-Lang配置实际改变页面}
import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from config import ROOT, load_config
from scraper import extract
from build import fresh_offers, build

NOW=datetime.now(timezone.utc).isoformat()
TABLE='''Basic Droplets<table><tr><th>Memory</th><th>vCPU</th><th>Transfer</th><th>SSD</th><th>$/hr</th><th>$/mo</th></tr><tr><td>1 GiB</td><td>1 vCPU</td><td>1,000 GiB</td><td>25 GiB</td><td>$0.00893</td><td><a href="https://cloud.digitalocean.com/new?size=s-1vcpu-1gb">$6.00</a></td></tr></table>'''
class PipelineTests(unittest.TestCase):
    def setUp(self):self.cfg=load_config();self.p=self.cfg['providers'][0]
    def test_monthly_not_hourly_and_real_model(self):
        rows=extract(TABLE,self.p,NOW);self.assertEqual(rows[0]['price'],'6.00');self.assertEqual(rows[0]['model'],'s-1vcpu-1gb');self.assertNotIn('valid_until',rows[0])
    def test_ambiguous_monthly_is_rejected(self):
        self.assertEqual(extract(TABLE.replace('$6.00','Was $9.00 now $6.00'),self.p,NOW),[])
    def test_missing_model_is_rejected(self):
        self.assertEqual(extract(TABLE.replace('size=','wrong='),self.p,NOW),[])
    def test_unknown_table_fails_closed(self):
        with self.assertRaises(ValueError):extract(TABLE.replace('$/mo','Renewal'),self.p,NOW)
    def test_failure_stale_expiry_removed_and_deduped(self):
        row=extract(TABLE,self.p,NOW)[0]; data={'providers':[{'id':self.p['id'],'status':'ok'}],'offers':[row,row]}
        self.assertEqual(len(fresh_offers(self.cfg,data)),1)
        data['providers'][0]['status']='error';self.assertEqual(fresh_offers(self.cfg,data),[])
        data['providers'][0]['status']='ok';row['fetched_at']=(datetime.now(timezone.utc)-timedelta(hours=31)).isoformat();self.assertEqual(fresh_offers(self.cfg,data),[])
        row['fetched_at']=NOW;row['valid_until']=(datetime.now(timezone.utc)-timedelta(days=1)).isoformat();self.assertEqual(fresh_offers(self.cfg,data),[])
    def test_config_removal_changes_built_site(self):
        cfg=copy.deepcopy(self.cfg);cfg['providers']=cfg['providers'][1:]
        with tempfile.TemporaryDirectory() as td:
            config=Path(td)/'site.ilang';config.write_text('::ILANG\n::JSON_BEGIN\n'+json.dumps(cfg)+'\n::JSON_END',encoding='utf-8')
            output=Path(td)/'output'; report=build(config,output)
            self.assertEqual(report['providers'],2);self.assertEqual(report['deals'],0)
            self.assertFalse((output/'providers/digitalocean').exists());self.assertNotIn('digitalocean',(output/'index.html').read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
