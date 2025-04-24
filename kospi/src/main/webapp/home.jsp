<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file = "header.jsp" %>
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
/* 
	a = {
		b : "hi"
	}
	
	console.log(a.b.c)
	result = a.b.c
	console.log(a.c?.c)
 */
 var a;
 let result = a?.b?.c
console.log(result)
	/* async function a(){
		return "hi"
	}

	window.onload = async function() {
		result = await a()
		a().then(function(result){
		})
		console.log(result)
		
	} */
	
	/* function a(){
	}
	a()
	
	let a = function(){
	}
	a()
	
	let a = () =>{
	}
	
	a() */
	
	/* fetch("http://192.168.0.120:5000/stock/^KS11")
	//1. async await -> 비동기를 동기로
	//2. then -> 비동기로...
	
	
	
	
	$.ajax({
		url : "http://192.168.0.120:5000/stock/^KS11",
		type: "get",
		success : function(result){
		}
	}) */
	
	let chart;
	
	function fetchAndUpdate(){
		fetch("http://localhost:5000/stock/^KS11")
			.then(function(res){
				return res.json()
			}).then(function(data){
				console.log(data.labels)
				if(!chart){
					const ctx = document.getElementById("chart").getContext('2d');
					chart = new Chart(ctx, {
						type : "line",
						data : {
							labels : data.labels,
							datasets : [{
								responsive:false,
								label : "실시간 종가",
								data : data.close,
								borderWidth : 2
							}]
						}
					})
				}else{
					chart.data.labels = data.labels;
					chart.data.datasets[0].data = data.close;
					chart.update();
				}
			})
			/* .then(data => {
				console.log(data)
				if(!chart){
					const ctx = document.getElementById("chart").getContext('2d');
					chart = new Chart(ctx, {
						type : "line",
						data : {
							labels : data.labels,
							datasets : [{
								label : "실시간 종가",
								data : data.close,
								borderWidth : 2
							}]
						}
					})
				}else{
					chart.data.labels = data.labels;
					chart.data.datasets[0].data = data.close;
					chart.update();
				}
			}) */
	}
	
	fetchAndUpdate()
	
	setInterval(fetchAndUpdate, 30000);
</script>
</html>