package chat;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class ChatDAO extends DBManager{
	
	//글작성
	public void write(ChatVO vo) {
		
		String id = vo.getId();
		String content = vo.getContent();
		
		driverLoad();
		DBConnect();
		
		String sql = "insert into chat(id, content) ";
		sql += "values('"+id+"', '"+content+"')";
		executeUpdate(sql);
		
		DBDisConnect();
	}
	
	//채팅조회
	public List<ChatVO> chatList(){
		List<ChatVO> list = new ArrayList<>();
		
		driverLoad();
		DBConnect();
		
		String sql = "select * from chat";
		executeQuery(sql);
		
		while(next()) {
			ChatVO vo = new ChatVO();
			vo.setNo(getString("no"));
			vo.setId(getString("id"));
			vo.setContent(getString("content"));
			vo.setCreate_date(getString("create_date"));
			list.add(vo);
		}
		
		DBDisConnect();
		
		return list;
	}
}
