import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.HashMap;
import java.util.Map;
import net.sf.json.JSONObject;
 

public class GetPosition {
	private static final  String AK = "o3OeuwE0Dlx2pMQ5W2ku78rIMRYmrV8u";
    
    public static String getDetailAddress(String lat, String lng) {	
        JSONObject obj = getLocationInfo(lat, lng).getJSONObject("result");
        return obj.getString("formatted_address");	
    }	
    
    
    public static String getCity(String lat, String lng) {	
        JSONObject obj = getLocationInfo(lat, lng).getJSONObject("result").getJSONObject("addressComponent");
        return obj.getString("city");	
    }

    public static JSONObject getLocationInfo(String lat, String lng) {
        String url = "http://api.map.baidu.com/geocoding/v3/?callback=renderReverse&location="+lat+","+lng+"&output=json&pois=0&ak="+AK;
        JSONObject obj = JSONObject.fromObject(loadJSON(url));
        System.out.println(obj);
        return obj;
	}
    

    public static Map<String,Double> getLngAndLat(String address){
        Map<String,Double> map=new HashMap<String, Double>();
        String url = "http://api.map.baidu.com/geocoding/v3/?address="+address+"&output=json&ak="+AK+"&callback=showLocation";
        String json = loadJSON(url);
        //System.out.println(json);
        JSONObject obj = JSONObject.fromObject(json);
        if(obj.get("status").toString().equals("0")){
            double lng=obj.getJSONObject("result").getJSONObject("location").getDouble("lng");
            double lat=obj.getJSONObject("result").getJSONObject("location").getDouble("lat");
            map.put("lng", lng);
            map.put("lat", lat);
            System.out.println("经度：" + lng + "--- 纬度：" + lat);
            //System.out.println(GetPosition.getCity(Double.toString(lat), Double.toString(lng)));
        }else{ 
            System.out.println("未找到相匹配的经纬度！");
        }
        return map;
    }

    public static String loadJSON (String url) {
           StringBuilder json = new StringBuilder();
           try {
               URL oracle = new URL(url);
               URLConnection yc = oracle.openConnection();
               BufferedReader in = new BufferedReader(new InputStreamReader(
                       yc.getInputStream(),"UTF-8"));
               String inputLine = null;
               while ( (inputLine = in.readLine()) != null) {
                   json.append(inputLine);
               }
               in.close();
           } catch (Exception e) {
           }
           int index1 = json.indexOf("(");
           int index2 = json.lastIndexOf(")");
           
           //System.out.println(json.toString());
           
           return json.substring(index1+1,index2).toString();
       }
}
