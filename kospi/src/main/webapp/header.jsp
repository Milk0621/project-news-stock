<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Home</title>
	<link rel="stylesheet" href="./resources/css/header.css"></link>
	<script type="text/javascript" src="./resources/js/jquery-3.7.1.js"></script>
	<script>
	  (function(d) {
	    var config = {
	      kitId: 'ses4qhw',
	      scriptTimeout: 3000,
	      async: true
	    },
	    h=d.documentElement,t=setTimeout(function(){h.className=h.className.replace(/\bwf-loading\b/g,"")+" wf-inactive";},config.scriptTimeout),tk=d.createElement("script"),f=false,s=d.getElementsByTagName("script")[0],a;h.className+=" wf-loading";tk.src='https://use.typekit.net/'+config.kitId+'.js';tk.async=true;tk.onload=tk.onreadystatechange=function(){a=this.readyState;if(f||a&&a!="complete"&&a!="loaded")return;f=true;clearTimeout(t);try{Typekit.load(config)}catch(e){}};s.parentNode.insertBefore(tk,s)
	  })(document);
	</script>
</head>
<body>
<header class="wrap">
	<h1 onclick="location.href='home.jsp'">KOSPI NEWS</h1>
	<ul class="nav">
		<li onclick="location.href='home.jsp'">홈</li>
		<li onclick="location.href='news.jsp'">뉴스</li>
		<li onclick="location.href='datas.jsp'">날짜별 분석</li>
		<li onclick="location.href='model.jsp'">모델 평가</li>
	</ul>
	<ul class="icon">
		<li onclick="location.href=''"><img src="./resources/img/chat.png"></li>
		<li onclick="location.href=''"><img src="./resources/img/alram.png"></li>
		<li onclick="location.href=''"><img src="./resources/img/user.png"></li>
	</ul>
</header>
</body>
</html>