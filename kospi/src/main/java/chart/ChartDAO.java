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
		
		String sql = "select * from chart order by date desc";
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
