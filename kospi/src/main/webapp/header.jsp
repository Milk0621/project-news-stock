<%@page import="alarm.AlarmVO"%>
<%@page import="alarm.AlarmDAO"%>
<%@page import="chat.ChatVO"%>
<%@page import="java.util.List"%>
<%@page import="chat.ChatDAO"%>
<%@ page import="user.UserVO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
	UserVO user = (UserVO)session.getAttribute("user");

	ChatDAO cdao = new ChatDAO();
	List<ChatVO> list = cdao.chatList();
	
	AlarmDAO adao = new AlarmDAO();
	String userId = user != null ? user.getId() : "";
	List<AlarmVO> alist = adao.alarmList(userId);
	
%>
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
		<li onclick="location.href='dates.jsp'">날짜별 분석</li>
		<li onclick="location.href='model.jsp'">모델 평가</li>
	</ul>
	<div class="icon">
		<% if(user == null){ %>
			<span id="login-btn">로그인</span>
		<% }else if(user != null){ %>
			<div class="img-box" id="chat-icon">
				<img src="./resources/img/chat.png">
				<img src="./resources/img/chat_hover.png">
			</div>
			<div class="img-box" id="alarm-icon">
				<img src="./resources/img/alram.png">
				<img src="./resources/img/alram_hover.png">
			</div>
			<div class="img-box" id="info-icon">
				<img src="./resources/img/user.png">
				<img src="./resources/img/user_hover.png">
			</div>
			<span id="logout-btn" onclick="location.href='./ok/logout.jsp'">로그아웃</span>
		<% } %>
	</div>
	<div id="login-modal" class="modal">
		<form action="./ok/loginok.jsp" method="post">
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
		</form>
	</div>
    <div id="join-modal" class="modal">
		<form action="./ok/joinok.jsp" method="post">
	        <div class="modal-content">
	            <span class="close">&times;</span>
	            <h2>회원가입</h2>
	            <input type="text" placeholder="아이디" name="id"><br>
	            <input type="password" placeholder="비밀번호" name="pw"><br>
	            <input type="text" placeholder="이름" name="name">
	            <input type="text" placeholder="이메일" name="email">
	            <input type="text" placeholder="닉네임" name="nick">
	            <div class="text-box">
	                <p>이미 아이디가 있으신가요?</p>
	                <p id="login">로그인</p>
	            </div>
	            <button type="submit">회원가입</button>
	        </div>
		</form>
	</div>
	<% if(user != null){ %>
		<div id="chat">
			<div class="modal-chat">
				<span class="close">&times;</span>
				<h2>채팅</h2>
				<div id="messages">
					<%
						for(int i = 0; i < list.size(); i++){ 
							ChatVO vo = list.get(i);
							if(!vo.getId().equals(userId)){
					%>
								<div class="msg-con">
									<p><%=vo.getContent() %></p>
									<span><%=vo.getId() %></span>
									<span><%=vo.getCreate_date() %></span>
								</div>
					<%		}else{ %>
								<div class="msg-con-right">
									<p><%=vo.getContent() %></p>
									<span><%=vo.getId() %></span>
									<span><%=vo.getCreate_date() %></span>
								</div>
					<%
							}
						} 
					%>
				</div>
				<div class="msg-input">
					<input type="text" id="messageInput" placeholder="메시지 입력">
		    		<button id="sendMessageBtn">전송</button>
				</div>
			</div>
		</div>
	<% } %>
	<div id="alarm">
		<div class="alarm-info">
			<span class="close">&times;</span>
			<h2>알람</h2>
			<div id="alarms">
				<% 
					for(int i = 0; i < alist.size(); i++){
						AlarmVO avo = alist.get(i);
						
				%>
						<div class="alarm-con">
							<p><%= avo.getTitle() %></p>
							<p><%= avo.getContent() %></p>
							<p><%= avo.getDate() %></p>
						</div>
				<%
					}
				%>
			</div>
		</div>
	</div>
	<div id="mypage" class="modal">
		<div class="modal-info" onclick="t()">
			<span class="close">&times;</span>
			<h2>내정보</h2>
			<div id="info">
				<p>아이디 : hong1234</p>
				<p>이름 : 홍길동</p>
				<p>닉네임 : hgd</p>
				<p>이메일 : hong@example.com</p>
			</div>
			<a href="./ok/userDeleteok.jsp">회원 탈퇴</a>
		</div>
	</div>
</header>
</body>
<script type="text/javascript">
$(document).ready(function () {
	const message = document.getElementById("messages");
	const messageBox = document.getElementById("messageInput");
	
	let userId = '<%= user != null ? user.getId() : "" %>';
	if(userId != ""){
	message.scrollTop = message.scrollHeight
	}
	
    // 로그인 버튼 클릭
    $("#login-btn").on("click", function () {
        $("#login-modal").fadeIn();
    });

    // 모달 닫기
    $(".close").on("click", function () {
        $(".modal").fadeOut();
        //$("#chat").fadeOut();
        $("#chat").css("right", "-35%");
        $("#alarm").css("right", "-35%");
   		$("#mypage").fadeOut();
    });
    
    /* function modalFadeOut(elId){
    	if ($(event.target).is("#"+elId)) {
            $("#"+elId).fadeOut();
        }
	}
    
    modalFadeOut("login_modal") */

    // 배경 클릭 시 닫기
    $(window).on("click", function (event) {
        if ($(event.target).is("#login-modal")) {
            $("#login-modal").fadeOut();
        }
        else if ($(event.target).is("#join-modal")) {
            $("#join-modal").fadeOut();
        }
        else if ($(event.target).is("#mypage")) {
            $("#mypage").fadeOut();
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
    
    //채팅 모달 띄우기
    $("#chat-icon").on("click", function () {
		//$("#chat").fadeIn();
    	$("#chat").css("right", 0);
    });
	
    //알림 모달 띄우기
    $("#alarm-icon").on("click", function () {
		$("#alarm").css("right", 0);
    });
    
    //개인 정보 모달 띄우기
    $("#info-icon").on("click", function () {
		$("#mypage").fadeIn();
    });
    
    messageBox.addEventListener("keyup",function(key){
        if(key.keyCode==13) {
        	sendMessage()
        }
    });
	
    //날짜
    function getCurrentDateTime() {
        const now = new Date();
        const date = now.toISOString().split('T')[0];
        const time = now.toTimeString().split(' ')[0];
        return { date, time };
    }

    //챗
    let uuid = crypto.randomUUID();
	console.log(uuid)
	let sendMessageBtn = $("#sendMessageBtn");
	
	const socket = new WebSocket("ws://localhost:8765/chat");
	console.log("?????")
	socket.onopen = () => {
	    console.log("서버에 연결됨.");
	    //appendMessage("서버에 연결되었습니다.");
	    //socket.send("인원 접속")
	};
	
	socket.onerror = (error) => {
	    console.error("WebSocket 오류:", error);
	};
	
	socket.onmessage = (event) => {
		console.log(event)
        console.log("수신:", event.data);
		const msg = JSON.parse(event.data);
		console.log("수신 메시지:", msg);
		
		if(msg.type && msg.type == "stock"){
			console.log(msg.message.price)
		}else if(msg.type && msg.type == "noti"){
			//알림창 갱신
			for(let i = 0; i < msg.keys.length; i++){
				if(msg.keys[i].id == "나"){
					//알림창 표시
					no = msg.keys[i].key
				}
			}
			console.log(msg.message)
		}
		
        const message = document.getElementById("messages");
        //const sender = msg.user || userId;
        const { date, time } = getCurrentDateTime();
    };
    
    
   	
    function sendMessage(){
		let chat = $("#messageInput");
		
		let msg = {
			user : userId,
			message : messageBox.value
		}
		//"{user : uuid, message : hi}"
		socket.send(JSON.stringify(msg));
		
		const { date, time } = getCurrentDateTime();
		
	    $.ajax({
			url : "./ok/chatok.jsp",
			type : "post",
			data : {
				id : userId,
				chat : msg.message
			},
			success : function(result){
				console.log(result);
				if (result.trim() == "success"){
					let html = "";
					html += "<div class='msg-con-right'>";
					html += 	"<p>"+chat.val()+"</p>";
					html +=		"<span>"+msg.user+"</span> ";
					html += "<span>" +date + " " + time + "</span>"
					html += "</div>";
					message.innerHTML += html;
					message.scrollTop = message.scrollHeight
				};
			},
			error : function(){
				console.log("에러 발생");
			},
			complete : function(){
				chat.val("")
		   }
	    });
	}
    
	//실시간 채팅
	sendMessageBtn?.click(function(){
		sendMessage()
	});
});


</script>
</html>