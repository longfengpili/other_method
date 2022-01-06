<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 NOT FOUND</title>
</head>
<body>
    <div class="img_content">
        <img src="http://wechatapppro-1252524126.file.myqcloud.com/apppcHqlTPT3482/image/b_u_5b73e35149a67_ypMtbWtO/kq6ljay90fy6.png" id="error_img">
    </div>
    <div id="error_desc">为保护版权，已停止访问此页面。</div>
</body>
</html>
<script>
    function initStyle () {
        let desc_el = document.getElementById('error_desc')
        let img_el = document.getElementById('error_img')
        desc_el.style.fontSize = `${window.innerHeight * 0.025}px`
        img_el.style.width = `${window.innerHeight * 0.35}px`
        img_el.style.marginTop = '100px'
    }
    initStyle()
</script>
<style>
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
}
.img_content {
    display: flex;
    justify-content: center;
}
#error_desc {
    color: #888;
    margin: 0 auto;
    text-align: center;
}
</style>