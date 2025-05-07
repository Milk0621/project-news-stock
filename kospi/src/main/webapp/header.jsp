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
	
	int alarmCheck = adao.alarmCheck(userId);
	
%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>KOSPI NEWS</title>
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
	</ul>
	<div class="icon">
		<% if(user == null){ %>
			<span id="login-btn">로그인</span>
		<% }else if(user != null){ %>
			<div class="img-box" id="chat-icon">
				<img src="./resources/img/chat.png">
			</div>
			<div class="img-box" id="alarm-icon">
				<% if(alarmCheck > 0){ %>
					<div class="dot"></div>
				<%} %>
				<img src="./resources/img/alram.png">
			</div>
			<div class="img-box" id="info-icon">
				<img src="./resources/img/user.png">
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
									<p class="id">닉네임 : <%=vo.getNick() %></p>
									<p class="msg-txt"><%=vo.getContent() %></p>
									<span><%=vo.getCreate_date() %></span>
								</div>
					<%		}else{ %>
								<div class="msg-con-right">
									<p class='id'>닉네임 : <%=vo.getNick() %></p>
									<p class="msg-txt"><%=vo.getContent() %></p>
									<span><%=vo.getCreate_date() %></span>
								</div>
					<%
							}
						} 
					%>
				</div>
				<div class="msg-input">
					<input type="text" id="messageInput" placeholder="메시지 입력">
				</div>
			</div>
		</div>
	<% } %>
	<div id="alarm">
		<div class="alarm-info">
			<span class="close" id="alarm-close">&times;</span>
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
			<% if(user != null){ %>
			<div id="info">
				<p>아이디 : <%= user.getId() %></p>
				<p>이름 : <%= user.getName() %></p>
				<p>닉네임 : <%= user.getNick() %></p>
				<p>이메일 : <%= user.getEmail() %></p>
			</div>
			<button class="delete-btn">회원탈퇴</button>
			<% } %>
		</div>
	</div>
	<div id="delete_user" class="delete_user">
		<form action="./ok/userDeleteok.jsp" method="post">
			<div class="delete_content">
				<h2>회원탈퇴</h2>
				<p>탈퇴를 원하시면 비밀번호를 입력해주세요.</p>
				<input type="password" placeholder="현재 비밀번호" name="pw"><br>
				<button type="submit">확인</button>
				<button type="button" class="cancel">취소</button>
			</div>
		</form>
	</div>
</header>
</body>
<script type="text/javascript">
$(document).ready(function () {
	const message = document.getElementById("messages");
	const messageBox = document.getElementById("messageInput");
	
	let userId = '<%= user != null ? user.getId() : "" %>';
	let userNick = '<%= user != null ? user.getNick() : "" %>';
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
    
    $("#messageInput").on("keyup", function(e) {
        if (e.key === "Enter" || e.keyCode === 13) {
            sendMessage();
        }
    });
	
    //회원탈퇴
    $(".delete-btn").click(function(){
    	$("#delete_user").fadeIn();
    });
    
    $(".cancel").click(function(){
    	$("#delete_user").fadeOut();
    });
    
    $(window).click(function(event){
    	if ($(event.target).is("#delete_user")){
    		$("#delete_user").fadeOut();
    	}
    })
    
    
    //날짜
    function getCurrentDateTime() {
        const now = new Date();
        const date = now.toISOString().split('T')[0];
        const time = now.toTimeString().split(' ')[0];
        return { date, time };
    }
	
    $("#alarm-icon").on("click", function() {
    	if(<%=alarmCheck %> > 0){
			$.ajax({
				url : "./ok/alarmCheckok.jsp",
				type : "post",
				data : {
					id : userId
				},
				success : function(result){
					console.log(result);
					if(result.trim() == "success"){
						$(".dot").css("display", "none");
					};
				},
				error : function(){
					console.log("에러 발생");
				}
			});
    	}
    });
    
    //챗
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
		
		if(msg.type && msg.type == "noti"){
			//알림창 갱신
			console.log(msg)
			$("#alarm-icon").prepend('<div class="dot"></div>')
			
			let alarmHtml = "";
			alarmHtml += '<div class="alarm-con">'
			alarmHtml += '<p>'+msg.message+'</p>'
			alarmHtml += '<p>'+msg.content+'</p>'
			alarmHtml += '<p>'+msg.date+'</p>'
			alarmHtml += '</div>'
			
			$("#alarms").prepend(alarmHtml)
			
		}else if(msg.type == "message"){
			let messageEl = "";
			if(msg.user == userId){
				messageEl += '<div class="msg-con-right">'
				messageEl += '<p class="id">닉네임 : '+msg.user+'</p>'
				messageEl += '<p class="msg-txt">'+msg.message+'</p>'
				messageEl += '<span>'+msg.date+'</span>'
				messageEl += '</div>'
			}else{
				messageEl += '<div class="msg-con">'
				messageEl += '<p class="id">닉네임 : '+msg.user+'</p>'
				messageEl += '<p class="msg-txt">'+msg.message+'</p>'
				messageEl += '<span>'+msg.date+'</span>'
				messageEl += '</div>'
			}
			
			$("#messages").append(messageEl);
			message.scrollTop = message.scrollHeight
		}
    };
    
    
   	//메시지 작성
    function sendMessage(){
		let chat = $("#messageInput");
		
		
		//"{user : uuid, message : hi}"
		
		const { date, time } = getCurrentDateTime();
		
		let msg = {
			user : userId,
			message : messageBox.value,
			type: "message",
			date : date
		}
		
		socket.send(JSON.stringify(msg));
		
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
					html +=		"<p class='id'>닉네임:"+userNick+"</p> ";
					html += 	"<p class='msg-txt'>"+chat.val()+"</p>";
					html += 	"<span>" +date + " " + time + "</span>"
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

$("#chat-icon > img").hover(function(){
    $(this).attr('src','./resources/img/chat_hover.png');
}, function() {
    $(this).attr('src','./resources/img/chat.png');
});

$("#alarm-icon > img").hover(function(){
    $(this).attr('src','./resources/img/alram_hover.png');
}, function() {
    $(this).attr('src','./resources/img/alram.png');
});

$("#info-icon > img").hover(function(){
    $(this).attr('src','./resources/img/user_hover.png');
}, function() {
    $(this).attr('src','./resources/img/user.png');
});

</script>
</html>