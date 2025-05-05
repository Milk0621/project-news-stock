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
			<%	int maxNews = 20; // 4페이지(20개)의 뉴스만 보여줌
				int slideSize = 5; //한 슬라이드에 뉴스 5개
				int totalSlides = (int)Math.ceil(Math.min(nlist.size(), maxNews) / (double)slideSize); //전체 슬라이드 개수 (20 / 5 = 4)
				
				for(int slide = 0; slide < totalSlides; slide++){
					int start = slide * slideSize; //현재 슬라이드에 들어갈 뉴스 시작 인덱스
					int end = Math.min(start + slideSize, maxNews); //Math.min() -> 입력 변수 중 가장 작은 수 반환 -> 전체 뉴스 개수
				%>
					<div class="head_news slide<%=slide+1%>" style='<%= slide == 0 ? "" : "display:none;" %>'>
						<% NewsVO main = nlist.get(start); %>
						<div class="main_news" onclick="location.href='post.jsp?no=<%=main.getNo()%>'">
							<div class="bg"></div>
							<img src="<%=main.getImg()%>">
							<div class="txt">
								<h2><%=main.getTitle() %></h2>
								<span><%=main.getName() %></span> · <span><%=main.getDate() %></span>
							</div>
						</div>
						<div class="sub_news">
						<% for(int i = start + 1; i < end; i++){ 
							NewsVO vo = nlist.get(i);
						%>
							<div onclick="location.href='post.jsp?no<%=vo.getNo() %>'">
								<div class="txt">
									<h2><%=vo.getTitle()%></h2>
									<span><%=vo.getName()%></span> · <span><%=vo.getDate()%></span>
								</div>
								<div class="news_img">
									<img src="<%=vo.getImg()%>">
								</div>
							</div>
						<%} %>
						</div>
					</div>
				<%} %>
			<ul class="headline_page">
				<% for(int i = 0; i < totalSlides; i++){ %>
					<li><button type="button" class="slide-btn" data-slide="<%=i+1%>"><%=i+1%></button></li>
				<%} %>
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
	//상단 뉴스
	$('.slide-btn').click(function() {
	    const index = $(this).data('slide'); // 누른 버튼의 슬라이드 번호

	    $('.head_news').hide();             // 모든 슬라이드 감추고
	    $('.slide' + index).show();          // 선택한 슬라이드만 보여줌

	    $('.slide-btn').removeClass('top_btn');
	    $(this).addClass('top_btn');          // 클릭된 버튼 강조
 	});
	
	//하단 뉴스
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