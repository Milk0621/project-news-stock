package dates;
/**
 * 2025-05-03
 * 날짜별 분석 데이터 VO 클래스
 */
public class DatesVO {
	/* 그룹화된 날짜 */
	private String dates;
	
	/* 코스피 종가 */
	private String price;
	
	/* 코스피 예측 가격 */
	private String predictPrice;
	
	/* 날짜별 top5 키워드 */
	private String keywords;
	
	/* 날짜별 감성분석 결과 */
	private String topSentiment;
	
	/* 날짜별 감성분석 퍼센트 */
	private String topSentimentPercentage;

	public String getDates() {
		return dates;
	}

	public void setDates(String dates) {
		this.dates = dates;
	}

	public String getPrice() {
		return price;
	}

	public void setPrice(String price) {
		this.price = price;
	}

	public String getPredictPrice() {
		return predictPrice;
	}

	public void setPredictPrice(String predictPrice) {
		this.predictPrice = predictPrice;
	}

	public String getKeywords() {
		return keywords;
	}

	public void setKeywords(String keywords) {
		this.keywords = keywords;
	}

	public String getTopSentiment() {
		return topSentiment;
	}

	public void setTopSentiment(String topSentiment) {
		this.topSentiment = topSentiment;
	}

	public String getTopSentimentPercentage() {
		return topSentimentPercentage;
	}

	public void setTopSentimentPercentage(String topSentimentPercentage) {
		this.topSentimentPercentage = topSentimentPercentage;
	}
	
}
