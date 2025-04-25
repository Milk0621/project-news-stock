package senti_result;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class SentiResultDAO extends DBManager{
	
	//감성결과 조회
	public List<SentiResultVO> sentiList(){
		List<SentiResultVO> list = new ArrayList<SentiResultVO>();
		
		driverLoad();
		DBConnect();
		
		String sql = "select * from senti_result";
		executeQuery(sql);
		
		while(next()) {
			SentiResultVO vo = new SentiResultVO();
			vo.setNo(getString("no"));
			vo.setDate(getString("date"));
			vo.setResult(getString("result"));
			vo.setGood(getString("good"));
			vo.setBad(getString("bad"));
			list.add(vo);
		}
		
		DBDisConnect();
		
		return list;
	}

}
