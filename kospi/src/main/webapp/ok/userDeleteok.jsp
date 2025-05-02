<%@page import="user.UserDAO"%>
<%@page import="user.UserVO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
	String id = request.getParameter("id");
	String pw = request.getParameter("pw");
	
	if(id == null || pw == null){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	if(id.isEmpty() || pw.isEmpty()){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	UserVO vo = new UserVO();
	UserDAO dao = new UserDAO();
	
	vo.setId(id);
	vo.setPw(pw);
	
	dao.userDelete(vo);
	
	response.sendRedirect("../home.jsp");
%>