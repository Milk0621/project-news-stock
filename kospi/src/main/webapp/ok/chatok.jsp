<%@page import="chat.ChatVO"%>
<%@page import="chat.ChatDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
	String id = request.getParameter("id");
	String chat = request.getParameter("chat");
	
	if(id == null || chat == null){
		out.print("fail");
		return;
	}
	
	if(id.isEmpty() || chat.isEmpty()){
		out.print("fail");
		return;
	}
	
	
	ChatVO vo = new ChatVO();
	
	vo.setId(id);
	vo.setContent(chat);
	
	ChatDAO dao = new ChatDAO();
	dao.write(vo);
	out.print("success");
%>