package senti_result;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class SentiResultDAO extends DBManager{
	
	//상세페이지 감성결과 조회
	public SentiResultVO sentiList(String no){		
		driverLoad();
		DBConnect();
		
		String sql = "select * from senti_result where no = "+no+"";
		executeQuery(sql);
		
		SentiResultVO vo = new SentiResultVO();
		if(next()) {
			vo.setNo(getString("no"));
			vo.setSno(getString("sno"));
			vo.setGood(getString("good"));
			vo.setMid(getString("mid"));
			vo.setBad(getString("bad"));
			vo.setResult(getString("result"));
			DBDisConnect();
			return vo;
		}else {			
			DBDisConnect();
			return null;
		}
	}
	
	//날짜별 긍정 비율(차트용)
	public List<SentiChartVO> goodPercent(){		
		List<SentiChartVO> list = new ArrayList<>();
		driverLoad();
		DBConnect();
		
		String sql = "WITH adjusted_date AS (";
		sql += " SELECT CASE ";
		sql += "   WHEN TIME(n.date) >= '15:30:00' THEN DATE_ADD(DATE(n.date), INTERVAL 1 DAY) ";
		sql += "   ELSE DATE(n.date) ";
		sql += " END AS custom_day, ";
		sql += " CAST(sr.good AS DECIMAL(5,2)) AS good ";
		sql += " FROM news n JOIN senti_result sr ON n.no = sr.no ";
		sql += ") ";
		sql += "SELECT custom_day, ";
		sql += " COUNT(*) AS total_news, ";
		sql += " COUNT(CASE WHEN good > 50 THEN 1 END) AS good_count, ";
		sql += " ROUND(100 * COUNT(CASE WHEN good > 50 THEN 1 END) / COUNT(*), 2) AS good_ratio_percentage ";
		sql += "FROM adjusted_date ";
		sql += "GROUP BY custom_day ";
		sql += "ORDER BY custom_day;";
		executeQuery(sql);
		
		while(next()) {
			SentiChartVO vo = new SentiChartVO();
			vo.setCustom_day(getString("custom_day"));
			vo.setGood_ratio_percentage(getString("good_ratio_percentage"));
			list.add(vo);
		}
		DBDisConnect();
		return list;
	}

}
