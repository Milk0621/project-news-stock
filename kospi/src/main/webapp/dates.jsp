<%@page import="senti_result.SentiChartVO"%>
<%@page import="senti_result.SentiResultVO"%>
<%@page import="senti_result.SentiResultDAO"%>
<%@page import="com.fasterxml.jackson.databind.ObjectMapper"%>
<%@page import="chart.ChartVO"%>
<%@page import="chart.ChartDAO"%>
<%@page import="dates.DatesVO"%>
<%@page import="dates.DatesDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="header.jsp" %>
<%
	DatesDAO dao = new DatesDAO();
	List<DatesVO> dateAnalysisList = dao.getDateAnalysisData();
	
	ChartDAO chartdao = new ChartDAO();
	List<ChartVO> clist = chartdao.close();
	ObjectMapper mapper = new ObjectMapper();
	String jsonText = mapper.writeValueAsString(clist);
	
	SentiResultDAO sdao = new SentiResultDAO();
	List<SentiChartVO> slist = sdao.goodPercent();
	String sentiJsonText = mapper.writeValueAsString(slist);
%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Insert title here</title>
	<link rel="stylesheet" href="./resources/css/dates.css"></link>
</head>
<body>
	<div class="wrap">
		<div class="graph">
			<canvas id="chart" width="1200"></canvas>
		</div>
		<div class="datas">
			<table>
				<tr class="labels">
					<th>날짜</th>
					<th>종가</th>
					<th>예측값(익일)</th>
					<th>뉴스분석 결과</th>
					<th>주요 키워드</th>
				</tr>
				<tr class="margin"></tr>
				<%
					for(int i = 0; i < dateAnalysisList.size(); i ++){
						%>
							<tr class="data">
								<td><%= dateAnalysisList.get(i).getDates() %></td>
								<td><%= dateAnalysisList.get(i).getPrice() %></td>
								<% if(dateAnalysisList.get(i).getPredictPrice() == null){
									%>
										<td>장 마감 전</td>
									<%
								}else{ %>
									<td><%= dateAnalysisList.get(i).getPredictPrice() %></td>
								<%} %>
								<td><%= dateAnalysisList.get(i).getTopSentiment() %>(<%= dateAnalysisList.get(i).getTopSentimentPercentage() %>%)</td>
								<td><%= dateAnalysisList.get(i).getKeywords() %></td>
							</tr>
						<%
					}
				%>
			</table>
		</div>
	</div>
</body>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script type="text/javascript">
let chartData = <%= jsonText %>;
let goodData = <%= sentiJsonText %>;
console.log(goodData);

const labels = chartData.map(x => x.date);  // 종가 기준 날짜
const prices = chartData.map(x => Number(x.price));

// 긍정 비율 맵 구성
const sentimentMap = {};
goodData.forEach(x => {
  if (x.custom_day && x.good_ratio_percentage) {
    sentimentMap[x.custom_day] = Number(x.good_ratio_percentage);
  }
});

// 날짜 형식 맞춰서 매핑
const percentage = labels.map(date => {
  const key = date.substring(0, 10);  // 시간 제거
  return sentimentMap[key] ?? null;
});

console.log("labels:", labels);
console.log("sentimentMap:", sentimentMap);
console.log("percentage:", percentage);

const ctx = document.getElementById("chart").getContext('2d');
new Chart(ctx, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "코스피 종가",
            data: prices,
            borderWidth: 2,
            pointRadius: 1,
            tension: 0.2,
            yAxisID: 'y'  // 종가 축
        },{
			label: "날짜별 뉴스 긍정 비율",
			data: percentage,
			borderWidth: 2,
            pointRadius: 1,
            tension: 0.2,
            yAxisID: 'y1'  // 종가 축
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        	x: {
				ticks: {
				  callback: function(val, index, ticks) {
				    const raw = this.getLabelForValue(val);
				    return raw.substring(5, 10); // 'MM-DD'만 표시
				  },
				  maxRotation: 0,
				  minRotation: 0
				},
				title: {
				  display: true,
				  text: '날짜 (월-일)'
				}
			},
        	y: {               // 왼쪽 y축 (종가)
                beginAtZero: false,
                title: { display: true, text: '코스피 종가' }
            },
            y1: {              // 오른쪽 y축 (긍정 비율)
                position: 'right',
                beginAtZero: true,
                max: 100,
                ticks: { callback: val => `${val}%` },
                title: { display: true, text: '긍정 비율 (%)' }
            }
        }
    }
});
</script>
</html>