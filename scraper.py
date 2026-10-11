import os
from playwright.sync_api import sync_playwright

def run_agoda_scraper():
    with sync_playwright() as p:
        # 啟動無頭瀏覽器 (GitHub Actions 環境必須使用 headless=True)
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("正在前往 Agoda...")
        # 直接帶入搜尋條件的網址通常最快最準，或者手動輸入
        # 東京地區代碼通常可透過網址參數帶入，以下先進入首頁示範
        page.goto("https://www.agoda.com/", timeout=60000)
        
        # 處理可能的彈跳視窗 (Cookie 同意或登入宣傳)
        try:
            page.locator("button:has-text('Accept')").click(timeout=3000)
        except:
            pass

        print("設定搜尋條件：東京、2027-01-30 ~ 2027-01-31、4人房...")
        
        # 實務上 Agoda 網址結構支援直接用 URL Query 帶入參數搜尋，會比模擬點擊穩定非常多：
        # 參數說明：
        # text=東京 (搜尋關鍵字)
        # checkIn=2027-01-30
        # checkOut=2027-01-31
        # adults=4 (成人4人)
        target_url = "https://www.agoda.com/zh-tw/search?city=19741&checkIn=2027-01-30&checkOut=2027-01-31&rooms=1&adults=4&children=0"
        
        page.goto(target_url, timeout=60000)
        
        # 等待飯店列表載入
        print("等待搜尋結果載入...")
        page.wait_for_selector("[data-selenium='hotel-item']", timeout=20000)

        # 抓取前幾筆飯店資訊
        hotels = page.locator("[data-selenium='hotel-item']")
        count = hotels.count()
        print(f"找到約 {count} 筆飯店資訊，正在擷取前 10 筆...")

        results = []
        for i in range(min(count, 10)):
            hotel = hotels.nth(i)
            try:
                name = hotel.locator("[data-selenium='hotel-name']").inner_text()
                price = hotel.locator("[data-selenium='display-price']").inner_text()
                results.append(f"飯店名稱: {name} | 價格: {price}")
            except Exception as e:
                continue

        print("\n--- 爬取結果 ---")
        for r in results:
            print(r)

        browser.close()

if __name__ == "__main__":
    run_agoda_scraper()
