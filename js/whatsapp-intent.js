/**
 * whatsapp-intent.js — 安卓点 WhatsApp 链接时先尝试直接唤起 App，失败就一定回落。
 *
 * 为什么不用 intent://：VIVO / OPPO / 小米 / UC 等国产浏览器的 UA 里都带 "Chrome/"，
 * 按 UA 判断会把它们误认成支持 intent 的 Chrome 系。它们不认 intent://，导航被静默丢弃，
 * 用户点了没有任何反应 —— 比改之前停在 api.whatsapp.com 下载页更糟（这是 30050b7 造成的回退）。
 *
 * 现在的策略（保证不劣于改动前）：
 *   1) href 里始终保留原始 wa.me 链接，不做任何改写 —— 爬虫、禁用 JS、中间件失败时行为与从前一致；
 *   2) 安卓上点击时先尝试 whatsapp://send?…（用户手势发起，Chrome 与多数国产浏览器都放行）；
 *   3) 1.2 秒后如果页面仍在最前面，说明没唤起成功 → 主动导航回原 wa.me 链接，
 *      即使用户看到的仍是那个"打开应用/下载"页，也绝不会是"点了没反应"。
 * iOS 与桌面完全不改：wa.me 在那两处工作正常，换成私有协议反而更容易失败。
 */
(function () {
  'use strict';

  var ua = navigator.userAgent || '';
  var isAndroid = /Android\b/i.test(ua);
  if (!isAndroid) return;

  var WAIT_MS = 1200;

  function parse(href) {
    var u;
    try { u = new URL(href, location.href); } catch (e) { return null; }
    if (u.hostname !== 'wa.me' && u.hostname !== 'api.whatsapp.com') return null;
    var phone = '';
    var m = u.pathname.match(/^\/(?:send\/?)?(\d{7,15})\/?$/);
    if (m) phone = m[1];
    if (!phone) phone = (u.searchParams.get('phone') || '').replace(/\D/g, '');
    if (phone.length < 7) return null;
    return { phone: phone, text: u.searchParams.get('text') || '' };
  }

  /* encodeURIComponent 不转义 ' ! ( ) * ~ 这些字符；scheme URL 里留裸字符，
     部分安卓浏览器会截断参数或直接放弃导航。深链与兜底都用严格编码。 */
  function enc(s) {
    return encodeURIComponent(s).replace(/[!'()*~]/g, function (c) {
      return '%' + c.charCodeAt(0).toString(16).toUpperCase();
    });
  }

  function deepLink(p) {
    return 'whatsapp://send?phone=' + p.phone + (p.text ? '&text=' + enc(p.text) : '');
  }

  /* 兜底用长链而不是 wa.me：wa.me 只是 302 到 api.whatsapp.com/send/?phone=…，
     多一跳，且 wa.me 这个域名在部分安卓浏览器/部分网络下本身就连不上（店主反馈的正是这类）。
     号码一律取纯数字：phone= 参数不接受加号与空格。 */
  function longLink(p) {
    return 'https://api.whatsapp.com/send/?phone=' + p.phone
      + (p.text ? '&text=' + enc(p.text) : '');
  }

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest
      ? e.target.closest('a[href*="wa.me/"], a[href*="api.whatsapp.com"]')
      : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href) return;
    var p = parse(href);
    if (!p) return;                                    // 解析不了就完全不干预，走浏览器默认行为

    e.preventDefault();
    var t0 = Date.now();
    var deep = deepLink(p);
    var fallback = longLink(p);
    window.__waAttempt = { deep: deep, fallback: fallback, at: t0 };   // 供验收脚本读取，不改变行为

    try {
      window.location.href = deep;
    } catch (err) {
      window.location.href = fallback;                 // 连赋值都抛异常（极罕见）→ 立刻兜底
      return;
    }

    setTimeout(function () {
      // 页面仍在最前台 = App 没被拉起来 → 走长链，绝不留"点了没反应"
      var stillHere = !document.hidden && document.visibilityState !== 'hidden';
      if (stillHere && Date.now() - t0 >= WAIT_MS - 200) window.location.href = fallback;
    }, WAIT_MS);
  }, true);
})();
