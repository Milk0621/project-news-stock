package user;

import db.DBManager;

public class UserDAO extends DBManager{
	
	//회원가입
	public void join(UserVO vo) {
		driverLoad();
		DBConnect();
		
		String sql = "";
		sql += "insert into user(id, pw, name, email, nick) ";
		sql += "values('"+vo.getId()+"', '"+vo.getPw()+"', '"+vo.getName()+"', '"+vo.getEmail()+"', '"+vo.getNick()+"')";
		executeUpdate(sql);
		
		DBDisConnect();
	}
	
	//로그인
	public UserVO login(UserVO uvo) {
		driverLoad();
		DBConnect();
		
		String sql = "select * from user where ";
		sql += "id='"+uvo.getId()+"' and pw='"+uvo.getPw()+"' and user_type!=99;";
		executeQuery(sql);
		
		if(next()) {
			UserVO vo = new UserVO();
			vo.setId(getString("id"));
			vo.setPw(getString("pw"));
			vo.setName(getString("name"));
			vo.setEmail(getString("email"));
			vo.setNick(getString("nick"));
			vo.setUser_type(getString("user_type"));
			
			DBDisConnect();
			return vo;
		}else {
			DBDisConnect();
			return null;
		}
	}
	
	//회원탈퇴
	public int userDelete(String id, String pw) {
		driverLoad();
		DBConnect();
		
		String sql = "select count(*) as cnt from user where id = '"+id+"' and pw = '"+pw+"'";
		executeQuery(sql);
		
		if(next()) {
			int cnt = getInt("cnt");
			if(cnt == 1) {
				sql = "update user set user_type = 99 where id = '"+id+"' and pw = '"+pw+"'";
				executeUpdate(sql);				
				DBDisConnect();
				return 1;
			}else {
				DBDisConnect();
				return 0;
			}
		}else {
			return 0;
		}
	}
}
