# VPS优惠站进度与使用

更新时间：2026-11-12（北京时间）。状态：已上线，自动更新实跑通过；Google富媒体测试未取得结果。

## 可直接使用
- 正式站：https://vps-deals-promo-radar-3cx.pages.dev/
- 仓库：https://github.com/yingdongpeng618-ship-it/vps-deals-promo-radar
- 更新任务：https://github.com/yingdongpeng618-ship-it/vps-deals-promo-radar/actions/workflows/update.yml
- 最近成功运行：https://github.com/yingdongpeng618-ship-it/vps-deals-promo-radar/actions/runs/43062405691
- 本地工程：C:\Users\Administrator\Documents\ChatGPT\优惠站

打开正式站，查看官方价格、进入Compare对比规格，详情页可到官方来源。默认VPS / vps-deals / en-US。3家官方来源，当前7个DigitalOcean常规方案；Hetzner与OVHcloud只监测页面，未核实价格时不显示价格。不声称这些常规价格是折扣。

## 已验证事实
Cloudflare Pages项目vps-deals-promo-radar，真实域名带-3cx后缀；生产分支main，构建python build.py，输出site。GitHub应用安装时只选择本次新建仓库；本轮已从Cloudflare实际仓库列表确认连接完成，无需再读验证码。

.ilang/site.ilang已回写base_url和@SITE domain，远端提交21a4ff73；README正式网址提交11a983ba。最新Cloudflare Pages检查completed/success。Actions运行43062405691成功，并自动提交fe4ae922。

13个线上sitemap页面全部在Chrome实际打开，每页有正确h1与自指canonical；7个详情页有官方出口，JSON-LD均可解析。sitemap13条，其中7deal，域名全部正确；robots允许抓取且Sitemap行正确。主页noindex已移除。最近数据核验时间2026-11-11T16:51:27+00:00，即北京时间2026-11-12 00:51:27。

6项本地测试前轮通过；本轮按最新公开数据重建，verify.py再次通过13页/7deal/13sitemap。配置实际改变页面的测试已通过。

## 怎么维护
只改.ilang/site.ilang维护品牌、厂商、官方来源和获批联盟链接。每6小时运行，预计北京时间02:23、08:23、14:23、20:23，GitHub可能延迟。Actions页Run workflow可手动更新。数据提交后Cloudflare自动构建，不需要手动上传静态站。不使用运行时LLM或个人API密钥；Actions只使用GitHub自带短期令牌。

## 证据位置
work/evidence/online-pages.json：线上13页和结构化数据。
work/evidence/deployment-api.json：公开提交、Actions、Cloudflare检查结果。
work/evidence/live-site.jpg：正式站截图。
work/evidence/google-test-error.jpg：Google测试异常截图。

## 限制与下一步
Google富媒体URL测试返回“出了点问题，如果此问题仍然存在，请过几个小时再试”，没有返回成功或结构化数据错误判定；稍后需要重试。本机Python直接请求本站得到Cloudflare403/1010，Chrome正常；原因未确认，不能把浏览器可读当作所有爬虫可达。
联盟申请、跟踪链接及佣金均未启用，按MONETIZATION.md接入；X/FB暂缓。域名注册与绑定尚未做，pages.dev可免费使用；自有域名有利于品牌和迁移，不保证SEO排名。

下一步：请用户打开正式站验收；稍后重试Google富媒体测试并核查搜索抓取可达性，再按需申请联盟与绑定自有域名。没有未完成的验证码代填操作。
