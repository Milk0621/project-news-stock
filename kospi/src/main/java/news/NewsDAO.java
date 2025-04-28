package news;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class NewsDAO extends DBManager{
	
	//뉴스 목록 조회
	public List<NewsVO> newsList() {
		driverLoad();
		DBConnect();
		
		String sql = "select * from news order by date desc";
		executeQuery(sql);
		
		List<NewsVO> list = new ArrayList<NewsVO>();
		
		while(next()) {
			NewsVO nvo = new NewsVO();
			nvo.setName(getString("name"));
			nvo.setTitle(getString("title"));
			nvo.setLink(getString("link"));
			nvo.setContent(getString("content"));
			nvo.setImg(getString("img"));
			nvo.setDate(getString("date"));
			nvo.setSenti_score(getString("senti_score"));
			nvo.setNo(getString("no"));
			list.add(nvo);
		}
		
		DBDisConnect();
		return list;
	}
	
	//뉴스 상세 조회
	public NewsVO newsPost(String no) {
		driverLoad();
		DBConnect();
		
		String sql = "select * from news where no = '"+no+"'";
		executeQuery(sql);
		
		NewsVO vo = new NewsVO();
		if(next()) {
			vo.setNo(getString("no"));
			vo.setName(getString("name"));
			vo.setTitle(getString("title"));
			vo.setLink(getString("link"));
			vo.setContent(getString("content"));
			vo.setImg(getString("img"));
			vo.setDate(getString("date"));
			vo.setSenti_score(getString("senti_score"));
			DBDisConnect();
			return vo;
		}else {
			DBDisConnect();
			return null;
		}
		
	}
}
