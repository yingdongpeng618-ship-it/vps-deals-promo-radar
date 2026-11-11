::ILANG
[TYPE:instructions][PROJECT:vps-deals][LANG:zh]
::OBJECTIVE{维护可溯源的VPS官方价格与优惠静态站}
::STATE{@CONFIG, source:.ilang/site.ilang, role:唯一品牌厂商渲染配置}
::ALLOW{修改配置 维护确定性Python适配器 运行测试 修复页面 提交公开源码}
::RULE{先读README和配置；每个py头部保留职责边界；新增厂商必须核验官方来源与robots}
::RULE{抓取与构建必须读配置；错误价格宁缺毋滥；失败和过期不得冒充当前价}
::RULE{联盟链接仅在获批后配置；使用sponsored标记与可见披露；不编佣金}
::RULE{部署后核验真实域名 canonical sitemap robots；不得猜pages.dev域名}
::BOUNDARY{never:编价格 编优惠 刷量 cookie注入 品牌词竞价 提交认证秘密 绕反爬|scope:permanent}
::VERIFY{python -m unittest discover -s tests；python scraper.py；python build.py；python verify.py}
