<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
    <input type="text" id="messageInput" placeholder="메시지 입력">
    <button onclick="sendMessage()">전송</button>
    
    <div id="messages"></div>
</body>
<script>
	let uuid = crypto.randomUUID();
	console.log(uuid)
	
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
		msg = JSON.parse(event.data)
		
		if(msg.type && msg.type == "stock"){
			//주가 보는 화면 갱신
		}else if(msg.type && msg.type == "noti"){
			//알림창 갱신
		}
		
        const message = document.getElementById("messages");
        message.innerHTML += "<div style='text-align:left'>"+msg.message+"</div>"
    };
    
    function sendMessage(){
		const messageBox = document.getElementById("messageInput");
		
		let msg = {
			user : uuid,
			message : messageBox.value
		}
		//"{user : uuid, message : hi}"
		socket.send(JSON.stringify(msg));
		
		const message = document.getElementById("messages");
        message.innerHTML += "<div style='text-align:right'>"+messageBox.value+"</div>"
	}
	
</script>
</html>