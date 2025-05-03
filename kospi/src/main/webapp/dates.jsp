<%@page import="dates.DatesVO"%>
<%@page import="dates.DatesDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="header.jsp" %>
<%
	DatesDAO dao = new DatesDAO();
	List<DatesVO> dateAnalysisList = dao.getDateAnalysisData();
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
			
		</div>
		<div class="datas">
			<table>
				<tr class="labels">
					<th>날짜</th>
					<th>종가</th>
					<th>예측값</th>
					<th>뉴스분석 결과</th>
					<th>주요 키워드</th>
				</tr>
				<tr class="margin"></tr>
				<%
					for(int i = 0; i < dateAnalysisList.size() ; i ++){
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
</html>