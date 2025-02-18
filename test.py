from pytrends.request import TrendReq

pytrends = TrendReq()
pytrends.build_payload(["Tesla"], timeframe="now 7-d")
trend_data = pytrends.interest_over_time()

print(trend_data)
