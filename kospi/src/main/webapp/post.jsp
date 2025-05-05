<%@page import="news.NewsVO"%>
<%@page import="news.NewsDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="header.jsp" %>
<%
	String no = request.getParameter("no");
	NewsDAO newsDao = new NewsDAO();
	NewsVO newsVO = new NewsVO();
	newsVO = newsDao.newsPost(no);
	
%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>POST</title>
	<link rel="stylesheet" href="./resources/css/post.css"></link>
</head>
<body>
	<div class="post_wrap">
		<div class="post-top">
			<h1><%= newsVO.getTitle() %></h1>
			<span><%= newsVO.getName() %> ·</span> <span><%= newsVO.getDate() %></span>
			<div><a href="<%= newsVO.getLink() %>"><%= newsVO.getLink() %></a></div>
		</div>
		<img src="<%= newsVO.getImg() %>">
		<p class="text">
			<%= newsVO.getContent() %>
		</p>
	</div>
</body>
</html>