<%@page import="news.NewsVO"%>
<%@page import="java.util.List"%>
<%@page import="news.NewsDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ include file="header.jsp" %>
<%
	String pageNum = request.getParameter("page");
	if(pageNum == null){
		pageNum = "1";
	}

	NewsDAO dao = new NewsDAO();
	List<NewsVO> nlist = dao.newsList();
	int currentPage = Integer.parseInt(pageNum);
	int startNum = (currentPage - 1) * 10;
	int limitperPage = 10;
	
	int pageGroupSize = 10;
	int startPage = ((currentPage - 1) / pageGroupSize) * pageGroupSize + 1;
	int totalCount = dao.getCount();
	int totalPage = (int)Math.ceil(totalCount / (double)limitperPage);
	int endPage = Math.min(startPage + pageGroupSize - 1, totalPage);
	
	String company = request.getParameter("company");
	if(company == null){
		company = "전체";
	}
	
	List<NewsVO> plist = dao.pageList(startNum, limitperPage, company);
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
						<div class="main_news" onclick="window.open('post.jsp?no=<%=main.getNo()%>')">
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
							<div onclick="window.open('post.jsp?no<%=vo.getNo() %>')">
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
				    <button onclick='location.href="news.jsp?page=<%=currentPage %>&company=전체"' data-name="전체">전체</button>
				    <button onclick='location.href="news.jsp?page=<%=currentPage %>&company=이데일리"' data-name="이데일리">이데일리</button>
				    <button onclick='location.href="news.jsp?page=<%=currentPage %>&company=아시아경제"' data-name="아시아경제">아시아경제</button>
				    <button onclick='location.href="news.jsp?page=<%=currentPage %>&company=매일경제"' data-name="매일경제">매일경제</button>
				    <button onclick='location.href="news.jsp?page=<%=currentPage %>&company=한국경제"' data-name="한국경제">한국경제</button>
				    <button onclick='location.href="news.jsp?page=<%=currentPage %>&company=머니투데이"' data-name="머니투데이">머니투데이</button>
				</div>
				<% for(int i = 0; i < plist.size(); i++){ 
					NewsVO vo = plist.get(i);
				%>
					<div class="content" data-name="<%=vo.getName()%>" onclick="window.open('post.jsp?no=<%=vo.getNo()%>')">
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
				<div class="page">
					<% if(currentPage  > 1){ %>
						<a href="news.jsp?page=1&company=<%=company %>">&lt;&lt;</a>
						<a href="news.jsp?page=<%=currentPage - 1 %>&company=<%=company %>">&lt;</a>
					<% } %>
					<% for(int i = startPage; i <= endPage; i++){ %>
					<% 		if(i == currentPage){ %>
								<a class="page-active" href="news.jsp?page=<%= i %>&company=<%=company %>"><%= i %></a>
						<% }else{ %>
							<a href="news.jsp?page=<%= i %>&company=<%=company %>"><%= i %></a>
						<% } %>
					<% } %>
					<% if(currentPage < totalPage) {%>
						<a href="news.jsp?page=<%=currentPage + 1 %>&company=<%=company %>">&gt;</a>
						<a href="news.jsp?page=<%=totalPage %>&company=<%=company %>">&gt;&gt;</a>
					<% } %>
				</div>
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
   /*  filterNews('전체');

    $('.media_category button').click(function() {
        let mediaName = $(this).data('name'); // 버튼의 data-name 가져오기
        filterNews(mediaName);

        // 클릭된 버튼만 active, 나머지는 제거
        $('.media_category button').removeClass('active');
        $(this).addClass('active');
    }); */
});

/* function filterNews(mediaName) {
    $('.content').each(function() {
        let name = $(this).data('name');
        if (mediaName === '전체' || name === mediaName) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
} */
</script>
</html>