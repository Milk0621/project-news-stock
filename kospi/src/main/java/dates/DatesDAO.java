package dates;

import java.util.ArrayList;
import java.util.List;

import db.DBManager;

/**
 * 2025-05-03
 * 날짜별 분석 데이터 DAO 클래스
 */
/*
 * -- chart 테이블에서 날짜별 가장 마지막(최신) 가격(price) 가져오기 (주말 제외)
WITH real_price AS (
    SELECT
        DATE(date) AS date_only,  -- datetime형식 date 컬럼을 date(연-월-일)로 변환
        price,  -- 실제 종가(price)
        ROW_NUMBER() OVER (PARTITION BY DATE(date) ORDER BY date DESC) AS rn  -- 날짜별 마지막(최신) 데이터를 1등으로 랭크
    FROM
        chart
    WHERE
        WEEKDAY(date) NOT IN (5, 6)  -- 날짜가 토요일(5), 일요일(6)인 경우 제외 (평일만)
),
-- predict 테이블에서 날짜별 가장 마지막(최신) 예측값(predict) 가져오기 (주말 제외)
predict_price AS (
    SELECT
        DATE(date) AS date_only,  -- datetime형식 date 컬럼을 date(연-월-일)로 변환
        predict,  -- 예측한 종가(predict)
        ROW_NUMBER() OVER (PARTITION BY DATE(date) ORDER BY date DESC) AS rn  -- 날짜별 마지막(최신) 데이터를 1등으로 랭크
    FROM
        predict
    WHERE
        WEEKDAY(date) NOT IN (5, 6)  -- 토요일, 일요일은 제외
),
-- news 테이블 날짜를 기준으로 주말(토, 일) 및 15:30 이후 뉴스는 다음 거래일로 넘기기
news_with_group AS (
    SELECT
        n.no,  -- 뉴스 번호 (기본키)
        STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s') AS news_datetime,  -- 뉴스 등록일을 datetime으로 변환
        CASE
            -- 토요일(5) 뉴스는 다음주 월요일로 날짜 이동
            WHEN WEEKDAY(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')) = 5
                THEN DATE_ADD(DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')), INTERVAL 2 DAY)
            -- 일요일(6) 뉴스는 다음주 월요일로 날짜 이동
            WHEN WEEKDAY(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')) = 6
                THEN DATE_ADD(DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')), INTERVAL 1 DAY)
            -- 평일이지만 오후 3:30 이후 뉴스는 다음 거래일로 날짜 이동
            WHEN TIME(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')) >= '15:30:00'
                THEN DATE_ADD(DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')), INTERVAL 1 DAY)
            -- 그 외 경우 (평일 15:30 이전 뉴스)는 해당 날짜 그대로 사용
            ELSE DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s'))
        END AS group_date  -- 뉴스별 실제 반영할 기준 날짜
    FROM
        news n
),
-- 뉴스 기준 그룹 날짜별로 키워드 추출
all_keywords AS (
    SELECT
        nwg.group_date,  -- 뉴스의 그룹핑된 날짜
        k.keyword  -- 해당 뉴스의 키워드
    FROM
        news_with_group nwg
    JOIN
        keyword k ON nwg.no = k.no  -- 뉴스 번호(no) 기준으로 키워드 테이블과 JOIN
),
-- 그룹 날짜별로 키워드 출현 빈도수를 세고 순위를 매김
keyword_count AS (
    SELECT
        group_date,  -- 그룹핑된 날짜
        keyword,  -- 키워드
        COUNT(*) AS keyword_freq,  -- 키워드 출현 빈도수
        ROW_NUMBER() OVER (PARTITION BY group_date ORDER BY COUNT(*) DESC, keyword ASC) AS rn  -- 날짜별로 빈도수 많은 순서로 랭크 (동점시 알파벳순)
    FROM
        all_keywords
    GROUP BY
        group_date, keyword  -- 날짜 + 키워드 조합별로 그룹화
),
-- 날짜별로 상위 5개의 키워드만 모아서 쉼표로 연결
keywords_grouped AS (
    SELECT
        group_date,  -- 그룹핑된 날짜
        GROUP_CONCAT(keyword ORDER BY keyword_freq DESC, keyword ASC SEPARATOR ', ') AS top_keywords  -- 상위 5개 키워드를 쉼표로 연결
    FROM (
        SELECT
            group_date,
            keyword,
            keyword_freq
        FROM
            keyword_count
        WHERE
            rn <= 5  -- 상위 5개 키워드만 필터링
    ) ranked_keywords
    GROUP BY
        group_date
),
-- 그룹 날짜별로 감성분석 결과(result)의 개수를 집계
senti_summary AS (
    SELECT
        nwg.group_date,  -- 뉴스 그룹핑 날짜
        sr.result,  -- 감성 결과 (positive, neutral, negative)
        COUNT(*) AS cnt  -- 감성 결과별 뉴스 개수
    FROM
        news_with_group nwg
    JOIN
        senti_result sr ON nwg.no = sr.no  -- 뉴스 번호(no) 기준으로 감성 결과 테이블과 JOIN
    GROUP BY
        nwg.group_date, sr.result
),
-- 그룹 날짜별 총 뉴스 개수를 계산
total_news_per_group AS (
    SELECT
        group_date,  -- 그룹핑된 날짜
        SUM(cnt) AS total_cnt  -- 총 뉴스 개수
    FROM
        senti_summary
    GROUP BY
        group_date
),
-- 감성 결과 중 가장 많은 결과(result)와 비율(percentage) 계산
senti_ranked AS (
    SELECT
        ss.group_date,  -- 그룹핑된 날짜
        ss.result,  -- 감성 결과
        ss.cnt,  -- 해당 감성 결과 개수
        tn.total_cnt,  -- 날짜별 총 뉴스 개수
        ROUND((ss.cnt / tn.total_cnt) * 100, 2) AS percentage,  -- 감성 결과 비율 (소수점 둘째 자리까지)
        ROW_NUMBER() OVER (PARTITION BY ss.group_date ORDER BY ss.cnt DESC) AS rn  -- 날짜별로 감성 개수 많은 순서 랭크
    FROM
        senti_summary ss
    JOIN
        total_news_per_group tn ON ss.group_date = tn.group_date
)
-- 최종 결과: 날짜별 가격, 예측가격, 상위 키워드, 상위 감성 결과, 감성 비율
SELECT
    r.date_only AS dates,  -- 날짜
    r.price AS price,  -- 실제 종가
    p.predict AS predict_price,  -- 예측한 종가
    kg.top_keywords AS keywords,  -- 상위 키워드 5개
    sr.result AS top_sentiment,  -- 가장 많은 감성 결과
    sr.percentage AS top_sentiment_percentage  -- 가장 많은 감성 결과의 비율(%)
FROM
    real_price r
LEFT JOIN
    predict_price p ON r.date_only = p.date_only AND p.rn = 1  -- 날짜 기준 예측 가격 LEFT JOIN (있으면 연결, 없으면 NULL)
LEFT JOIN
    keywords_grouped kg ON r.date_only = kg.group_date  -- 날짜 기준 키워드 그룹 LEFT JOIN
LEFT JOIN
    senti_ranked sr ON r.date_only = sr.group_date AND sr.rn = 1  -- 날짜 기준 감성 결과 LEFT JOIN (가장 많은 감성만 연결)
WHERE
    r.rn = 1  -- 실제 가격에서 날짜별 마지막 데이터만 필터링
ORDER BY
    dates ASC;  -- 날짜 오름차순 정렬
 * 
 */
public class DatesDAO extends DBManager{
	
	/* 
	 * 날짜별로 그룹화 한 뒤, 종가, 예측가, top-5키워드, 감성분석결과, 비율을 가져오는 메서드
	 * 별도 쿼리는 docs/date_query.txt 참조   
	 */
	public List<DatesVO> getDateAnalysisData() {
		
		List<DatesVO> list = new ArrayList<>();
		
		DBConnect();
		
		String sql = "";
		sql += "WITH real_price AS (";
		sql += " SELECT DATE(date) AS date_only,";
		sql += " price,";
		sql += " ROW_NUMBER() OVER (PARTITION BY DATE(date) ORDER BY date DESC) AS rn";
		sql += " FROM chart";
		sql += " WHERE WEEKDAY(date) NOT IN (5, 6)";
		sql += "),";
		sql += "predict_price AS (";
		sql += " SELECT DATE(date) AS date_only,";
		sql += " predict,";
		sql += " ROW_NUMBER() OVER (PARTITION BY DATE(date) ORDER BY date DESC) AS rn";
		sql += " FROM predict";
		sql += " WHERE WEEKDAY(date) NOT IN (5, 6)";
		sql += "),";
		sql += "news_with_group AS (";
		sql += " SELECT";
		sql += " n.no,";
		sql += " STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s') AS news_datetime,";
		sql += " CASE";
		sql += " WHEN WEEKDAY(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')) = 5 THEN DATE_ADD(DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')), INTERVAL 2 DAY)";
		sql += " WHEN WEEKDAY(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')) = 6 THEN DATE_ADD(DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')), INTERVAL 1 DAY)";
		sql += " WHEN TIME(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')) >= '15:30:00' THEN DATE_ADD(DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s')), INTERVAL 1 DAY)";
		sql += " ELSE DATE(STR_TO_DATE(n.date, '%Y-%m-%d %H:%i:%s'))";
		sql += " END AS group_date";
		sql += " FROM news n";
		sql += "),";
		sql += "all_keywords AS (";
		sql += " SELECT";
		sql += " nwg.group_date,";
		sql += " k.keyword";
		sql += " FROM news_with_group nwg";
		sql += " JOIN keyword k ON nwg.no = k.no";
		sql += "),";
		sql += "keyword_count AS (";
		sql += " SELECT";
		sql += " group_date,";
		sql += " keyword,";
		sql += " COUNT(*) AS keyword_freq,";
		sql += " ROW_NUMBER() OVER (PARTITION BY group_date ORDER BY COUNT(*) DESC, keyword ASC) AS rn";
		sql += " FROM all_keywords";
		sql += " GROUP BY group_date, keyword";
		sql += "),";
		sql += "keywords_grouped AS (";
		sql += " SELECT";
		sql += " group_date,";
		sql += " GROUP_CONCAT(keyword ORDER BY keyword_freq DESC, keyword ASC SEPARATOR ', ') AS top_keywords";
		sql += " FROM (";
		sql += " SELECT";
		sql += " group_date,";
		sql += " keyword,";
		sql += " keyword_freq";
		sql += " FROM keyword_count";
		sql += " WHERE rn <= 5";
		sql += " ) ranked_keywords";
		sql += " GROUP BY group_date";
		sql += "),";
		sql += "senti_summary AS (";
		sql += " SELECT";
		sql += " nwg.group_date,";
		sql += " sr.result,";
		sql += " COUNT(*) AS cnt";
		sql += " FROM news_with_group nwg";
		sql += " JOIN senti_result sr ON nwg.no = sr.no";
		sql += " GROUP BY nwg.group_date, sr.result";
		sql += "),";
		sql += "total_news_per_group AS (";
		sql += " SELECT";
		sql += " group_date,";
		sql += " SUM(cnt) AS total_cnt";
		sql += " FROM senti_summary";
		sql += " GROUP BY group_date";
		sql += "),";
		sql += "senti_ranked AS (";
		sql += " SELECT";
		sql += " ss.group_date,";
		sql += " ss.result,";
		sql += " ss.cnt,";
		sql += " tn.total_cnt,";
		sql += " ROUND((ss.cnt / tn.total_cnt) * 100, 2) AS percentage,";
		sql += " ROW_NUMBER() OVER (PARTITION BY ss.group_date ORDER BY ss.cnt DESC) AS rn";
		sql += " FROM senti_summary ss";
		sql += " JOIN total_news_per_group tn ON ss.group_date = tn.group_date";
		sql += ")";
		sql += "SELECT";
		sql += " r.date_only AS dates,";
		sql += " r.price AS price,";
		sql += " p.predict AS predict_price,";
		sql += " kg.top_keywords AS keywords,";
		sql += " sr.result AS top_sentiment,";
		sql += " sr.percentage AS top_sentiment_percentage";
		sql += " FROM real_price r";
		sql += " LEFT JOIN predict_price p ON r.date_only = p.date_only AND p.rn = 1";
		sql += " LEFT JOIN keywords_grouped kg ON r.date_only = kg.group_date";
		sql += " LEFT JOIN senti_ranked sr ON r.date_only = sr.group_date AND sr.rn = 1";
		sql += " WHERE r.rn = 1";
		sql += " ORDER BY dates ASC;";
		
		executeQuery(sql);
		while(next()) {
			DatesVO vo = new DatesVO();
			vo.setDates(getString("dates"));
			vo.setPrice(getString("price"));
			vo.setPredictPrice(getString("predict_price"));
			vo.setKeywords(getString("keywords"));
			vo.setTopSentiment(getString("top_sentiment"));
			vo.setTopSentimentPercentage(getString("top_sentiment_percentage"));
			list.add(vo);
		}
		DBDisConnect();
		
		return list;
	}
}
