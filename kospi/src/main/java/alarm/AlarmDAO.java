package alarm;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class AlarmDAO extends DBManager{
	
	//알람조회
	public List<AlarmVO> alarmList(String id){
		List<AlarmVO> list = new ArrayList<AlarmVO>();
		
		driverLoad();
		DBConnect();
		
		String sql = "select * from alarm where id = '"+id+"' and check = 1";
		executeQuery(sql);
		
		while(next()) {
			AlarmVO vo = new AlarmVO();
			vo.setNo(getString("no"));
			vo.setId(getString("id"));
			vo.setTitle(getString("title"));
			vo.setContent(getString("content"));
			vo.setDate(getString("date"));
			vo.setCheck(getString("check"));
			list.add(vo);
		}
		
		DBDisConnect();
		return list;
	}
}
