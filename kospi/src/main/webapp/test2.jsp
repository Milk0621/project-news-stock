<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
	<canvas id="chart"></canvas>
</body>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
	
	async function getToken(){

		/* fetch("https://api.kiwoom.com/oauth2/token", {
			  method: "POST",
			  headers: {
			    "Content-Type": "application/json;charset=UTF-8",
			  },
			  body: JSON.stringify({
				grant_type: 'client_credentials',
				appkey: "EdvswTLAI4wCzDwRbw3TjTLI5v0XkzL0OzW4_3zDcWo",
				secretkey: "gNy9Y9XHfEyJrjffeVhcfyt-nmQ2yEoTqAewQDWz_DI",
			  }),
			}).then(function(response){
				response.json()
			}).then(function(response){
				return response;
			}) */
		
		const response = await fetch("https://api.kiwoom.com/oauth2/token", {
		  method: "POST",
		  headers: {
		    "Content-Type": "application/json;charset=UTF-8",
		  },
		  body: JSON.stringify({
			grant_type: 'client_credentials',
			appkey: "EdvswTLAI4wCzDwRbw3TjTLI5v0XkzL0OzW4_3zDcWo",
			secretkey: "gNy9Y9XHfEyJrjffeVhcfyt-nmQ2yEoTqAewQDWz_DI",
		  })
		})
		
		const result = await response.json()
		return result
	}
	
	
	const socket = new WebSocket("wss://api.kiwoom.com:10000/api/dostk/websocket");
	console.log("?????")
	socket.onopen = async () => {
	    console.log("서버에 연결됨.");
	    
	    const token = await getToken()
	    console.log(token)
	    
	    const loginData ={
            'trnm': 'LOGIN',
            'token': token.token
       } 
	    
	    socket.send(JSON.stringify(loginData))
	};
	
	let chart = null;
	
	socket.onmessage = (event) => {
		//console.log(event.data)
		data = JSON.parse(event.data)
		if(data.trnm == "LOGIN"){
			if(data.return_msg != 0){
				console.log("로그인 실패")
				socket.close()				
			}else{
				console.log("로그인 성공")
				const data = {
				    	'trnm': 'REG',
				        'grp_no': '1',
				        'refresh': '1',
				        'data': [{
				            'item': ['001'],
				            'type': ['0J']
				        }]

					}
				socket.send(JSON.stringify(data))
			}
		}else if(data.trnm == "PING"){
			socket.send(event.data)
		}
		
		if(data.trnm == "REAL"){
			const prices = data.data[0].values["10"]
			const times = data.data[0].values["20"]
			price = prices.replace(/^[-+]/, "");
			time = String(Math.floor(times / 100));
			
			const ctx = document.getElementById("chart").getContext('2d');
			if(!chart){
				chart = new Chart(ctx, {
					type : "line",
					data : {
						labels : [time],
						datasets : [{
							responsive:false,
							label : "실시간 종가",
							data : [price],
							borderWidth : 2
						}]
					}
				})
			}else{
				chart.data.labels.push(time);
				chart.data.datasets[0].data.push(price);
				
				if (chart.data.labels.length > 30) {
	              chart.data.labels.shift();
	              chart.data.datasets[0].data.shift();
	            }
				chart.update();
			}
			
		}
    };
    
   /* const data = {
	    	'trnm': 'REG', //서비스명
	        'grp_no': '1', //그룹번호
	        'refresh': '1', //기존등록유지여부
	        'data': [{ //실시간 등록 리스트
	            'item': ['039490'], //실시간 등록 요소
	            'type': ['0B'] //실시간 항목
	        }]
		}
	socket.send(JSON.stringify(data)) */
</script>
</html>