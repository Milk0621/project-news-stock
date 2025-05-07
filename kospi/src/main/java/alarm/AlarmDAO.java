package alarm;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

public class AlarmDAO extends DBManager{
	
	//알람조회
	public List<AlarmVO> alarmList(String id){
		List<AlarmVO> list = new ArrayList<AlarmVO>();
		if(id.isEmpty()) {
			return list;
		}
		
		driverLoad();
		DBConnect();
		
		String sql = "select * from alarm where id = '"+id+"' order by checked, date desc";
		executeQuery(sql);
		
		while(next()) {
			AlarmVO vo = new AlarmVO();
			vo.setNo(getString("no"));
			vo.setId(getString("id"));
			vo.setTitle(getString("title"));
			vo.setContent(getString("content"));
			vo.setDate(getString("date"));
			vo.setCheck(getString("checked"));
			list.add(vo);
		}
		
		DBDisConnect();
		return list;
	}
	
	//알람확인
	public void alarmChecked(String id) {
		driverLoad();
		DBConnect();
		
		String sql = "update alarm set checked = 1 where id = '"+id+"' and checked = 0";
		executeUpdate(sql);
		
		DBDisConnect();
	}
	
	//읽지 않은 알림 조회
	public int alarmCheck(String id) {
		driverLoad();
		DBConnect();
		
		String sql = "select count(*) as cnt from alarm where id = '"+id+"' and checked = 0";
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
