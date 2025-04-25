<%@page import="user.UserVO"%>
<%@page import="user.UserDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
	request.setCharacterEncoding("utf-8");

	String id = request.getParameter("id");
	String pw = request.getParameter("pw");
	String name = request.getParameter("name");
	String email = request.getParameter("email");
	String nick = request.getParameter("nick");
	
	if(id == null || pw == null || name == null || email == null || nick == null){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	if(id.isEmpty() || pw.isEmpty() || name.isEmpty() || email.isEmpty() || nick.isEmpty()){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	UserDAO dao = new UserDAO();
	UserVO vo = new UserVO();
	vo.setId(id);
	vo.setPw(pw);
	vo.setName(name);
	vo.setEmail(email);
	vo.setNick(nick);
	
	dao.join(vo);
	
	response.sendRedirect("../home.jsp");
%>