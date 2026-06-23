import urllib.request
import re
from datetime import datetime

def get_finance_data():
    try:
        # 네이버 금융 환율 정보 페이지
        url = "https://finance.naver.com/marketindex/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('euc-kr', 'ignore')
        
        # 원달러 환율 값을 정밀하게 찾기 (기존보다 더 정확한 방식)
        # 네이버 금융 환율 위치를 정확히 타격합니다
        match = re.search(r'매매기준율.*?value">([\d,.]+)', html, re.DOTALL)
        if match:
            return match.group(1)
        return "1,380.00" # 실패 시 대안값
    except:
        return "1,380.00"

def update_html():
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    new_rate = get_finance_data()
    
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. 날짜 업데이트
    content = re.sub(r'최근 업데이트: \d{4}-\d{2}-\d{2} \d{2}:\d{2}', f'최근 업데이트: {now}', content)
    # 2. 환율 업데이트 (숫자 부분만 교체)
    content = re.sub(r'[\d,.]+ 원', f'{new_rate} 원', content)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_html()
