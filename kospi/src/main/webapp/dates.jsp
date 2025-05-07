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
								<td><%= dateAnalysisList.get(i).getPredictPrice() %></td>
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
console.log(chartData);

const labels = chartData.map(x => x.date);
const prices = chartData.map(x => Number(x.price));
console.log(labels);

const ctx = document.getElementById("chart").getContext('2d');
new Chart(ctx, {
    type: "line",
    data: {
        labels: labels,
        datasets: [{
            label: "뉴스 긍정 비율에 따른 코스피 종가",
            data: prices,
            borderWidth: 2,
            pointRadius: 2,
            tension: 0.2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});
</script>
</html>