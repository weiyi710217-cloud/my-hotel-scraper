import json
import os
from playwright.sync_api import sync_playwright

def run_agoda_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("正在前往 Agoda 搜尋東京 2027/01/30 ~ 2027/01/31 四人房...")
        target_url = "https://www.agoda.com/zh-tw/search?city=14534&checkIn=2027-01-30&checkOut=2027-01-31&rooms=1&adults=4&children=0"
        
        try:
            page.goto(target_url, timeout=60000)
            page.wait_for_selector("[data-selenium='hotel-item']", timeout=20000)

            hotels = page.locator("[data-selenium='hotel-item']")
            count = hotels.count()
            print(f"找到約 {count} 筆飯店資訊...")

            results = []
            for i in range(min(count, 15)): # 抓前 15 筆
                hotel = hotels.nth(i)
                try:
                    name = hotel.locator("[data-selenium='hotel-name']").inner_text()
                    price = hotel.locator("[data-selenium='display-price']").inner_text()
                    # 抓取飯店圖片或連結（選填）
                    results.append({"name": name, "price": price})
                except Exception as e:
                    continue

            # 將結果寫入 hotels.json
            with open("hotels.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print("資料已成功儲存至 hotels.json")

        except Exception as e:
            print(f"爬取過程發生錯誤: {e}")
            # 如果被反爬擋住，可以寫入空的或預設錯誤提示
            with open("hotels.json", "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        browser.close()

if __name__ == "__main__":
    run_agoda_scraper()
