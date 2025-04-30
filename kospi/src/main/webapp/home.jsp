<%@page import="com.fasterxml.jackson.databind.ObjectMapper"%>
<%@page import="java.util.List"%>
<%@page import="chart.ChartVO"%>
<%@page import="chart.ChartDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file = "header.jsp" %>
<%
	ChartDAO dao = new ChartDAO();
	List<ChartVO> list = dao.chart();
	ObjectMapper mapper = new ObjectMapper();
	String jsonText = mapper.writeValueAsString(list);
%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
<link rel="stylesheet" href="./resources/css/home.css"></link>
</head>
<body>
	<div class="chart-container">
		<canvas id="chart"></canvas>
	</div>
</body>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>

let chartData = <%= jsonText %>
console.log(chartData)
const date = chartData.map(x => x.date);
const price = chartData.map(x => x.price);


const ctx = document.getElementById("chart").getContext('2d');
chart = new Chart(ctx, {
	type : "line",
	data : {
		labels : date,
		datasets : [{
			responsive:false,
			label : "실시간 종가",
			data : price,
			borderWidth : 2
		}]
	}
})

async function getToken(){	
	const keyRes = await fetch("http://localhost:5000/api/keys");
	const keyData = await keyRes.json();
	const appKey = keyData.appkey;
	const secretKey = keyData.secretkey;
	const response = await fetch("https://api.kiwoom.com/oauth2/token", {
	  method: "POST",
	  headers: {
	    "Content-Type": "application/json;charset=UTF-8",
	  },
	  body: JSON.stringify({
		grant_type: 'client_credentials',
		appkey: appKey,
		secretkey: secretKey,
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
    /* console.log(token) */
    
    const loginData ={
        'trnm': 'LOGIN',
        'token': token.token
   } 
    
    socket.send(JSON.stringify(loginData))
};

let chart = null;
let lastMinute = null;

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
		minute = time.slice(0, 4);
		
		if (minute !== lastMinute){
			lastMinute = minute;
			console.log(minute)
			console.log(lastMinute)
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
	}
};
</script>
</html>