<!-- 
=====================================
网站分析工具配置
=====================================
使用说明：
1. 注册百度统计：https://tongji.baidu.com/
2. 获取你的统计 ID（替换下面的 YOUR_BAIDU_TONGJI_ID）
3. 在所有 HTML 页面的 <head> 标签内添加引用
4. 示例：<script src="js/analytics.js"></script>
=====================================
-->

<script>
// 百度统计配置
var _hmt = _hmt || [];
(function() {
  // 替换为你的百度统计 ID
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?YOUR_BAIDU_TONGJI_ID";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>

<!-- 
其他分析工具可选：

1. 友盟+：https://www.umeng.com/
2. 51.la：https://www.51.la/
3. 腾讯云分析：https://cloud.tencent.com/product/mta

选择其中一个即可，不要同时添加多个，会影响网站速度
-->
