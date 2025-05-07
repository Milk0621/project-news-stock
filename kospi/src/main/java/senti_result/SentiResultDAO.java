package senti_result;

import db.DBManager;

public class SentiResultDAO extends DBManager{
	
	//감성결과 조회
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

}
