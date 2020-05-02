import java.sql.*;
import java.util.Arrays;

public class Choose {
	// MySQL 8.0 以下版本 - JDBC 驱动名及数据库 URL
	
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";  
    static final String DB_URL = "jdbc:mysql://cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com:3306/Travel";
 
    // MySQL 8.0 以上版本 - JDBC 驱动名及数据库 URL
    //static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";  
    //static final String DB_URL = "jdbc:mysql://localhost:3306/RUNOOB?useSSL=false&serverTimezone=UTC";
 
 
    // 数据库的用户名与密码，需要根据自己的设置
    static final String USER = "Esther";
    static final String PASS = "938991Lsx";
 
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        Attraction[] attrList = new Attraction[80];
        int i = 0;
        try{
            // 注册 JDBC 驱动
            Class.forName(JDBC_DRIVER);
        
            // 打开链接
            System.out.println("连接数据库...");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
        
            // 执行查询
            System.out.println(" 实例化Statement对象...");
            stmt = conn.createStatement();
            String sql;
            sql = "SELECT id, name, duration,price,startTime,endTime,popularity,nature,history,culture,outdoor,amusementPark,shopping,acitivity,other FROM BeijingAttr";
            ResultSet rs = stmt.executeQuery(sql);
        
            // 展开结果集数据库
            while(rs.next() && i<80){
                // 通过字段检索
                int id  = rs.getInt("id");
                String name = rs.getString("name");
                int duration=rs.getInt("duration");
            	int price=rs.getInt("price");
            	int starttime=rs.getInt("startTime");
            	int endtime=rs.getInt("endTime");
            	double popularity=rs.getDouble("popularity");
            	int nature=rs.getInt("nature");
            	int history=rs.getInt("history");
            	int culture=rs.getInt("culture");
            	int outdoor=rs.getInt("outdoor");
            	int amuse=rs.getInt("amusementPark");
            	int shopping=rs.getInt("shopping");
            	int activity=rs.getInt("acitivity");
            	int other=rs.getInt("other");
    
                // 输出数据
            	Attraction temp = new Attraction(id,name,duration,price,starttime,endtime,popularity,nature,history,culture,outdoor,amuse,shopping,activity,other);
            	attrList[i] = temp;
                i++;
            }
            // 完成后关闭
            rs.close();
            stmt.close();
            conn.close();
        }catch(SQLException se){
            // 处理 JDBC 错误
            se.printStackTrace();
        }catch(Exception e){
            // 处理 Class.forName 错误
            e.printStackTrace();
        }finally{
            // 关闭资源
            try{
                if(stmt!=null) stmt.close();
            }catch(SQLException se2){
            }// 什么都不做
            try{
                if(conn!=null) conn.close();
            }catch(SQLException se){
                se.printStackTrace();
            }
        }
        //for(int j=0;j<100;j++) {
        	//System.out.println(attrList[j].name);
        //}
        //System.out.println("Goodbye!");
        int totaldays = 5;
        User tt = new User(2,1000,1,0,0,1,1,1,0,0);
        int totalattr = tt.schel*totaldays*2;
        //System.out.println(totalattr);
        long startst = System.currentTimeMillis();
        for(int j=0;j<80;j++) {
        	double score = 0;
        	double pop;
        	//if(attrList[j].popularity-1<0.001) {
        	//	pop= 0;
        	//}
        	//else {
        		//pop=Math.pow(attrList[j].popularity,0.2);
        	pop = attrList[j].popularity;
        	//}
        	score = Math.pow(pop,0.2)*1.25+0.5*Math.pow((attrList[j].nature*tt.nature+attrList[j].history*tt.history+attrList[j].culture*tt.culture+attrList[j].outdoor*tt.outdoor+attrList[j].amuse*tt.amuse+attrList[j].shopping*tt.shopping+attrList[j].activity*tt.activity+attrList[j].other*tt.other),0.5);
        	attrList[j].score=score;
        }
        Arrays.sort(attrList);
        //for(int j=0;j<totalattr;j++) {
        	//System.out.println(attrList[j].name);
        //}
        for(int j=0;j<totalattr;j++) {
        	attrList[j].position=GetPosition.getLngAndLat(attrList[j].name);
        	System.out.println(attrList[j].name+' '+attrList[j].position);
        }
        
        //int totalprice = 0;
        //for(int j=0;j<totalattr;j++) {
        //	totalprice+=attrList[j].price;
        //}
        
        //double best = 0;
        //double totalroute = 0;
        //for(int j=0;j<totalattr;j++) {
        //	double routeScore = (1-0.5)*Math.pow(tt.budget/(1+tt.budget*0.5+totalprice), 0.5)+Math.pow((attrList[j].nature*tt.nature+attrList[j].history*tt.history+attrList[j].culture*tt.culture+attrList[j].outdoor*tt.outdoor+attrList[j].amuse*tt.amuse+attrList[j].shopping*tt.shopping+attrList[j].activity*tt.activity+attrList[j].other*tt.other+attrList[j].popularity), 0.5);
        //	totalroute+=routeScore;
        //	if(routeScore>best) best = routeScore;
        //}
        //double avg = totalroute/totalattr;
        //System.out.println(best);
        //System.out.println(avg);
        //long endend = System.currentTimeMillis();
        //System.out.println(endend-startst);
    }
}
