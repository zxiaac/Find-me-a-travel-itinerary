import java.sql.*;
import java.util.Arrays;

public class Choose {
	// MySQL 8.0 ���°汾 - JDBC �����������ݿ� URL
	
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";  
    static final String DB_URL = "jdbc:mysql://cs336.cxonjz7sctxh.us-east-2.rds.amazonaws.com:3306/Travel";
 
    // MySQL 8.0 ���ϰ汾 - JDBC �����������ݿ� URL
    //static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";  
    //static final String DB_URL = "jdbc:mysql://localhost:3306/RUNOOB?useSSL=false&serverTimezone=UTC";
 
 
    // ���ݿ���û��������룬��Ҫ�����Լ�������
    static final String USER = "Esther";
    static final String PASS = "938991Lsx";
    
    public static boolean checkAllVisited(Attraction[] ll) {
    	for(int i=0;i<ll.length;i++) {
    		if(ll[i].visited==false) return false;
    	}
    	return true;
    }
 
    public static void main(String[] args) {
        Connection conn = null;
        Statement stmt = null;
        Attraction[] attrList = new Attraction[80];
        int i = 0;
        try{
            // ע�� JDBC ����
            Class.forName(JDBC_DRIVER);
        
            // ������
            System.out.println("�������ݿ�...");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
        
            // ִ�в�ѯ
            System.out.println(" ʵ����Statement����...");
            stmt = conn.createStatement();
            String sql;
            sql = "SELECT id, name, duration,price,startTime,endTime,popularity,nature,history,culture,outdoor,amusementPark,shopping,acitivity,other FROM BeijingAttr";
            ResultSet rs = stmt.executeQuery(sql);
        
            // չ����������ݿ�
            while(rs.next() && i<80){
                // ͨ���ֶμ���
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
    
                // �������
            	Attraction temp = new Attraction(id,name,duration,price,starttime,endtime,popularity,nature,history,culture,outdoor,amuse,shopping,activity,other);
            	attrList[i] = temp;
                i++;
            }
            // ��ɺ�ر�
            rs.close();
            stmt.close();
            conn.close();
        }catch(SQLException se){
            // ���� JDBC ����
            se.printStackTrace();
        }catch(Exception e){
            // ���� Class.forName ����
            e.printStackTrace();
        }finally{
            // �ر���Դ
            try{
                if(stmt!=null) stmt.close();
            }catch(SQLException se2){
            }// ʲô������
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
        //��ȡ����
        for(int j=0;j<totalattr;j++) {
        	attrList[j].position=GetPosition.getLngAndLat("������"+attrList[j].name);
        	//System.out.println(attrList[j].name+' '+attrList[j].position);
        }
        
        //�����������
        Attraction[] chosenList = new Attraction[totalattr];
        for(int j=0;j<totalattr;j++) {
        	chosenList[j] = new Attraction(attrList[j]);
        }
        
        //����һ��������Ϊ��㣬���ϳ���ʱ��Ϊ8��
        Attraction[][] forDays = new Attraction[totaldays][tt.schel*2];
        int curr = 0;
        int n = 0;
        int m = 0;
        //while(checkAllVisited(chosenList)==false) {
        while(m<totaldays) {
        	n = 0;
        	int currHour = 8;
        	while(n<tt.schel*2) {
        		chosenList[curr].visited=true;
        		forDays[m][n]=chosenList[curr];
        		currHour +=chosenList[curr].duration;
        		//if(currHour>20) {
        		//	break;
        		//}
        		int bestweight = 1000;
        		int travelling =0;
        		for(int j=0;j<totalattr;j++) {
        			if(chosenList[j].visited) continue;
        			else {
        				int travellingTime= GetPosition.getDrive(chosenList[curr].position.get("lng").toString(), chosenList[curr].position.get("lat").toString(), chosenList[j].position.get("lng").toString(), chosenList[j].position.get("lat").toString());
        				int weight = travellingTime/60/60+currHour-chosenList[j].duration;
        				if(bestweight>weight) {
        					bestweight = weight;
        					travelling = travellingTime;
        					curr = j;
        				}
        			}
        		}
        		
        		//System.out.println(forDays[m][n].name);
        		n++;
        		
        		currHour+=travelling/60/60;
        		if(currHour>24) {
        			break;
        		}
        	}
        	//System.out.println(" ");
        	m++;
        }
        
        for(m=0;m<totaldays;m++) {
        	for (n=0;n<tt.schel*2;n++) {
        		if(forDays[m][n]!=null)
        			System.out.println(forDays[m][n].name);
        	}
        	System.out.println(" ");
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
