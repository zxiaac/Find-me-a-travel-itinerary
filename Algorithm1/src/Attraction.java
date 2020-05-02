import java.util.Map;

public class Attraction implements Comparable{
	String name;
	int id;
	int duration;
	int price;
	int starttime;
	int endtime;
	double popularity;
	int nature;
	int history;
	int culture;
	int outdoor;
	int amuse;
	int shopping;
	int activity;
	int other;
	
	double score=0;
	boolean visited = false;
	Map<String,Double> position;
	
	public Attraction(int id,String name,int duration, int price, int starttime, int endtime,double popularity, int nature,int history, int culture, int outdoor, int amuse, int shopping, int activity, int other) {
		this.id = id;
		this.name=name;
		this.duration = duration;
		this.price=price;
		this.starttime=starttime;
		this.endtime=endtime ;
		this.popularity=popularity;
		this.nature=nature;
		this.history=history;
		this.culture=culture;
		this.outdoor=outdoor;
		this.amuse=amuse;
		this.shopping=shopping;
		this.activity=activity;
		this.other=other;
	}
	
	public Attraction(Attraction a) {
		this.id = a.id;
		this.name=a.name;
		this.duration = a.duration;
		this.price=a.price;
		this.starttime=a.starttime;
		this.endtime=a.endtime ;
		this.popularity=a.popularity;
		this.nature=a.nature;
		this.history=a.history;
		this.culture=a.culture;
		this.outdoor=a.outdoor;
		this.amuse=a.amuse;
		this.shopping=a.shopping;
		this.activity=a.activity;
		this.other=a.other;
		this.position = a.position;
		this.visited=a.visited;
		this.score=a.score;
	}
	
	public int compareTo(Object o) {
		
		Attraction a = (Attraction) o;
		int result = score<a.score ? 1: (score==a.score ? 0:-1);
		if(result==0) {
			result = id<a.id ? 1: -1;
		}
		return result;
	}
}
