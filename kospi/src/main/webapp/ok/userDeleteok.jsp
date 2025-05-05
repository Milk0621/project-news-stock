<%@page import="user.UserDAO"%>
<%@page import="user.UserVO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%

	String pw = request.getParameter("pw");	
	UserVO user = (UserVO)session.getAttribute("user");
	
	String id = user.getId();

	
	if(id == null || pw == null){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	if(id.isEmpty() || pw.isEmpty()){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	UserDAO dao = new UserDAO();
	
	int result = dao.userDelete(id, pw);
	
	if (result == 1){
		session.invalidate();
		out.println("<script>alert('회원탈퇴가 완료되었습니다.'); location.href='../home.jsp'</script>");
	}else{
		out.println("<script>alert('비밀번호가 일치하지 않습니다.'); location.href='../home.jsp'</script>");
	}
	
%>