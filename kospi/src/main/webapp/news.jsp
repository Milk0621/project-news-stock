<%@page import="news.NewsVO"%>
<%@page import="java.util.List"%>
<%@page import="news.NewsDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="header.jsp" %>
<%
	NewsDAO dao = new NewsDAO();
	List<NewsVO> nlist = dao.newsList();
%>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>News</title>
	<link rel="stylesheet" href="./resources/css/news.css"></link>
</head>
<body>
	<div class="wrap">
		<div class="headline">
			<h1>주요 뉴스</h1>
			<div class="head_news">
				<div class="main_news">
					<div class="bg"></div>
					<img src="https://cphoto.asiae.co.kr/listimglink/1/2025042109380927353_1745195889.jpg">
					<div class="txt">
						<h2>코스피, 실적 앞두고 관망세…2490선 유지</h2>
						<span>아시아경제</span> · <span>2025-04-21</span>
					</div>
				</div>
				<div class="sub_news">
				<% for(int i = 0; i < 4; i++){ 
					NewsVO vo = nlist.get(i);
				%>
					<div>
						<div class="txt">
							<h2><%=vo.getTitle()%></h2>
							<span><%=vo.getDate()%></span> · <span><%=vo.getName()%></span>
						</div>
						<div class="news_img">
							<img src="<%=vo.getImg()%>">
						</div>
					</div>
				<%} %>
				</div>
			</div>
			<ul class="headline_page">
				<li><button type="button">1</button></li>
				<li><button type="button">2</button></li>
				<li><button type="button">3</button></li>
				<li><button type="button">&lt</button></li>
				<li><button type="button">&gt</button></li>
			</ul>
		</div>
		<div class="news">
			<h1>언론사별 뉴스</h1>
			<div class="media_news">
				<div class="media_category">
				    <button data-name="전체">전체</button>
				    <button data-name="이데일리">이데일리</button>
				    <button data-name="아시아경제">아시아경제</button>
				    <button data-name="매일경제">매일경제</button>
				    <button data-name="한국경제">한국경제</button>
				    <button data-name="머니투데이">머니투데이</button>
				</div>
				<% for(int i = 0; i < nlist.size(); i++){ 
					NewsVO vo = nlist.get(i);
				%>
					<div class="content" data-name="<%=vo.getName()%>" onclick="location.href='post.jsp?no=<%=vo.getNo()%>'">
				        <div class="content_img">
				            <img src="<%=vo.getImg()%>">
				        </div>
				        <div class="content_txt">
				            <h2><%=vo.getTitle()%></h2>
				            <p><%=vo.getContent()%></p>
				            <span><%=vo.getDate()%></span> · <span><%=vo.getName()%></span>
				        </div>
				    </div>
				<%} %>
			</div>
		</div>
	</div>
</body>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$(document).ready(function() {
    filterNews('전체');

    $('.media_category button').click(function() {
        let mediaName = $(this).data('name'); // 버튼의 data-name 가져오기
        filterNews(mediaName);

        // 클릭된 버튼만 active, 나머지는 제거
        $('.media_category button').removeClass('active');
        $(this).addClass('active');
    });
});

function filterNews(mediaName) {
    $('.content').each(function() {
        let name = $(this).data('name');
        if (mediaName === '전체' || name === mediaName) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}
</script>
</html>