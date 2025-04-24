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
	<div class="icon">
		<span id="login-btn">로그인</span>
		<div class="img-box">
			<img src="./resources/img/chat.png">
			<img src="./resources/img/chat_hover.png">
		</div>
		<div class="img-box">
			<img src="./resources/img/alram.png">
			<img src="./resources/img/alram_hover.png">
		</div>
		<div class="img-box">
			<img src="./resources/img/user.png">
			<img src="./resources/img/user_hover.png">
		</div>
	</div>
	<div id="login-modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>로그인</h2>
            <input type="text" placeholder="아이디" name="id"><br>
            <input type="password" placeholder="비밀번호" name="pw">
            <div class="text-box">
                <p>아이디가 없으신가요?</p>
                <p id="join">회원가입</p>
            </div>
            <button type="submit">로그인</button>
        </div>
	</div>
    <div id="join-modal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>회원가입</h2>
            <input type="text" placeholder="아이디" name="id"><br>
            <input type="password" placeholder="비밀번호" name="pw"><br>
            <input type="text" placeholder="이름" name="name">
            <input type="text" placeholder="이메일" name="email">
            <div class="text-box">
                <p>이미 아이디가 있으신가요?</p>
                <p id="login">로그인</p>
            </div>
            <button type="submit">회원가입</button>
        </div>
   </div>
</header>
</body>
<script type="text/javascript">
$(document).ready(function () {
    // 로그인 버튼 클릭
    $("#login-btn").on("click", function () {
        $("#login-modal").fadeIn();
    });

    // 모달 닫기
    $(".close").on("click", function () {
        $(".modal").fadeOut();
    });

    // 배경 클릭 시 닫기
    $(window).on("click", function (event) {
        if ($(event.target).is("#login-modal")) {
            $("#login-modal").fadeOut();
        }
        if ($(event.target).is("#join-modal")) {
            $("#join-modal").fadeOut();
        }
    });

    // 회원가입 모달 띄우기
    $("#join").on("click", function () {
        $("#login-modal").fadeOut();
        $("#join-modal").fadeIn();
    });

    // 로그인 모달 띄우기
    $("#login").on("click", function () {
        $("#join-modal").fadeOut();
        $("#login-modal").fadeIn();
    });
});
</script>
</html>