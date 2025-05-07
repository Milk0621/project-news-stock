<%@page import="alarm.AlarmDAO"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%
	String id = request.getParameter("id");

	if(id == null || id.isEmpty()){
		response.sendRedirect("../home.jsp");
		return;
	}
	
	AlarmDAO dao = new AlarmDAO();
	dao.alarmChecked(id);
	
	
	out.print("success");
%>