package news;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

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
			nvo.setNo(getString("no"));
			list.add(nvo);
		}
		
		DBDisConnect();
		return list;
	}
	
	//언론사별 뉴스 조회
	public List<NewsVO> pageList(int startNum, int limitSize, String name) {
		driverLoad();
		DBConnect();
		
		String sql = "select * from news ";
		if(!name.equals("전체")) {
			sql += "where name = '"+name+"' ";
		}
		sql += "order by date desc limit "+startNum+", "+limitSize+"";
		System.out.println("page : " + sql);

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
			nvo.setNo(getString("no"));
			list.add(nvo);
		}
		
		DBDisConnect();
		return list;
	}
	
	//최근 뉴스 분석
	public List<NewsVO> newsResultList() {
		driverLoad();
		DBConnect();
		
		String sql = "select n.no, n.name, n.title, n.link, n.content, n.img, n.date, ";
		sql += "k.keyword, s.good, s.bad, s.mid, s.result ";
		sql += "from news n ";
		sql += "left join keyword k on n.no = k.no ";
		sql += "left join senti_result s on n.no = s.no ";
		sql += "order by n.date desc ";
		
		executeQuery(sql);
		
		//중복 없이 저장할 Map 생성
		//이게 없을시 결과 -> 1 뉴스1 키워드1, 2 뉴스1 키워드2, 3 뉴스1 키워드3
		Map<String, NewsVO> newsMap = new LinkedHashMap<>();
		
		while (next()) {
	        String no = getString("no"); //현재 뉴스의 고유 번호 가져오기
	        NewsVO nvo = newsMap.get(no); //no 키 값을 기준으로 이미 저장된 뉴스인지 확인

	        if (nvo == null) {
	            nvo = new NewsVO();
	            nvo.setNo(no);
	            nvo.setName(getString("name"));
	            nvo.setTitle(getString("title"));
	            nvo.setLink(getString("link"));
	            nvo.setContent(getString("content"));
	            nvo.setImg(getString("img"));
	            nvo.setDate(getString("date"));
	            nvo.setKeywords(new ArrayList<>()); //키워드 리스트 초기화(선언)

	            nvo.setGood(getString("good"));
	            nvo.setBad(getString("bad"));
	            nvo.setMid(getString("mid"));
	            nvo.setResult(getString("result"));

	            newsMap.put(no, nvo); //Map에 저장 (중복 방지)
	        }
	        
	        //키워드가 있을 경우 뉴스VO의 키워드 리스트에 추가
	        String keyword = getString("keyword");
	        if (keyword != null && !nvo.getKeywords().contains(keyword)) {
	            nvo.getKeywords().add(keyword);
	        }
	    }

	    DBDisConnect();
	    
	    //Map에 저장된 NewsVO만 리스트로 변환
	    return new ArrayList<>(newsMap.values());
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
			DBDisConnect();
			return vo;
		}else {
			DBDisConnect();
			return null;
		}
		
	}
	
	//뉴스 갯수 조회
	public int getCount(String name) {
		driverLoad();
		DBConnect();
		
		String sql = "select count(*) as cnt from news ";
		if(!name.equals("전체")) {
			sql += "where name = '"+name+"' ";
		}
		System.out.println("count : " + sql);
		executeQuery(sql);
		
		if(next()) {
			int count = getInt("cnt");
			DBDisConnect();
			return count;
		}else {
			DBDisConnect();
			return 0;
		}
	}
}
