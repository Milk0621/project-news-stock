package news;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class NewsDAO extends DBManager{
	
	//뉴스 목록 조회
	public List<NewsVO> news_list(NewsVO vo) {
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
}
