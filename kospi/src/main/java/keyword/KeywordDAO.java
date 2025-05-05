package keyword;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class KeywordDAO extends DBManager{
	
	//키워드 목록 조회
	public List<KeywordVO> keywordList(){
		List<KeywordVO> list = new ArrayList<KeywordVO>();
		
		driverLoad();
		DBConnect();
		
		String sql = "select * from keyword";
		//조건 = 날짜?
		executeQuery(sql);
		
		while(next()) {
			KeywordVO vo = new KeywordVO();
			vo.setNo(getString("no"));
			vo.setKno(getString("kno"));
			vo.setKeyword(getString("keyword"));
		}
		
		DBDisConnect();
		return list;
	}
}
