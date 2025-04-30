package chart;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class ChartDAO extends DBManager{
	
	//차트 전체 조회
	public List<ChartVO> chart() {
		List<ChartVO> list = new ArrayList<ChartVO>();
		driverLoad();
		DBConnect();
		
		//String date = "2025-04-30-10:33";
		//자바로 현재 날짜 시간 구해오기 datetime
		//현재 날짜 시간이 15:30분이 넘었으면 15:30분으로 고정 
		
		//만약 다음날 새벽 12 ~ 9시사이면 현재날짜는 전날 15:30
		
		String sql = "select date_format(c1.date, '%Y-%m-%d %H:%i') as date, c1.price from chart c1 ";
		sql += "join(select date_format(date, '%Y-%m-%d %H:%i') as minute, ";
		sql += "max(date) as max_date from chart group by minute) ";
		sql += "c2 on c1.date = c2.max_date order by c1.date asc";
		//limit 필요
		executeQuery(sql);
		
		while(next()) {
			ChartVO vo = new ChartVO();
			vo.setDate(getString("date"));
			vo.setPrice(getString("price"));
			list.add(vo);
		}
		
		DBDisConnect();
		return list;
	}
}
