<%@page import="user.UserVO"%>
<%@page import="user.UserDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
	String id = request.getParameter("id");
	String pw = request.getParameter("pw");
	
	if(id == null || id.isEmpty()){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	if(pw == null || pw.isEmpty()){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	UserDAO dao = new UserDAO();
	UserVO vo = new UserVO();
	vo.setId(id);
	vo.setPw(pw);
	
	UserVO user = dao.login(vo);
	if(user == null){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	session.setAttribute("user", user);
	
	response.sendRedirect("../home.jsp");
	
%>