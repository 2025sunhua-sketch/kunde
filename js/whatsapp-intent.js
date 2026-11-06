/**
 * whatsapp-intent.js — 让安卓上的 WhatsApp 链接直接打开 App，而不是停在
 * api.whatsapp.com 的"打开应用 / 下载"中间页。
 *
 * 为什么要换机制：https://wa.me/<n> 只是 302 到 api.whatsapp.com/send/?…，
 * 由那个 225 KB 的网页再去尝试拉起 whatsapp://。中间任何一环被拦（浏览器拦自定义协议、
 * 在微信/Telegram 的内置 WebView 里打开、或本地网络只能半加载该页面），用户就停在下载页，
 * 明明装了 WhatsApp 也进不了对话。intent:// 由 Chrome 系浏览器在本地直接解析成 App 调用，
 * 不经过任何网络请求。
 *
 * 渐进增强：href 里保留 wa.me 原值。JS 不执行时（爬虫、禁脚本、老设备）行为与现在完全一致。
 * 只做两件事：安卓 Chrome 系 → intent://；安卓其他浏览器 → whatsapp://。
 * iOS 与桌面保持 wa.me（那条路径在 iOS 上工作正常，改成私有协议反而更容易失败）。
 */
(function () {
  'use strict';

  var ua = navigator.userAgent || '';
  var isAndroid = /Android\b/i.test(ua);
  if (!isAndroid) return;                                  // iOS / 桌面：不动

  var chromeish = /\b(CriOS|Chrome|Chromium|EdgA|SamsungBrowser|Brave)\b/i.test(ua)
    && !/\b(Firefox|OPR|OPiOS)\b/i.test(ua);

  function build(href) {
    var u;
    try { u = new URL(href, location.href); } catch (e) { return null; }
    if (u.hostname !== 'wa.me' && u.hostname !== 'api.whatsapp.com') return null;

    // 号码：wa.me/<n> 或 /send/<n> 在路径里；api.whatsapp.com/send/?phone=<n> 在查询里
    var phone = '';
    var m = u.pathname.match(/^\/(?:send\/?)?(\d{7,15})\/?$/);
    if (m) phone = m[1];
    if (!phone) {
      var p = u.searchParams.get('phone') || '';
      phone = p.replace(/\D/g, '');
    }
    if (phone.length < 7) return null;

    var text = u.searchParams.get('text') || '';
    var q = 'send?phone=' + phone + (text ? '&text=' + encodeURIComponent(text) : '');

    if (chromeish) {
      // package=com.whatsapp；只装 Business 或没装的用户由 browser_fallback_url 兜回 wa.me
      return 'intent://' + q + '#Intent;scheme=whatsapp;package=com.whatsapp;S.browser_fallback_url='
        + encodeURIComponent(href) + ';end';
    }
    return 'whatsapp://' + q;
  }

  function rewrite(root) {
    var list = (root || document).querySelectorAll('a[href*="wa.me/"], a[href*="api.whatsapp.com"]');
    var n = 0;
    for (var i = 0; i < list.length; i++) {
      var a = list[i];
      var href = a.getAttribute('href');
      if (/^intent:|^whatsapp:/.test(href)) continue;       // 幂等
      var next = build(href);
      if (next) { a.setAttribute('href', next); a.setAttribute('target', '_self'); n++; }
    }
    return n;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { rewrite(); });
  } else {
    rewrite();
  }
  window.__waRewrite = rewrite;                             // 供验收脚本调用与计数
})();
