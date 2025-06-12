from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Cấu hình Selenium
options = Options()
options.add_argument("--headless")  # Bỏ dòng này nếu muốn xem trình duyệt
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# Truy cập trang
url = "https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep"
driver.get(url)
time.sleep(2)  # Chờ trang load

excel_writer = pd.ExcelWriter("masothue.xlsx", engine="openpyxl")
page_number = 1

while True:
    print(f"🟢 Đang xử lý trang {page_number}...")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-item")))
    companies = driver.find_elements(By.CSS_SELECTOR, ".list-item")

    data = []
    for company in companies:
        try:
            name = company.find_element(By.CSS_SELECTOR, ".title-company").text.strip()
            mst = company.find_element(By.CSS_SELECTOR, ".tax-code span").text.strip()
            date = company.find_element(By.CSS_SELECTOR, ".date span").text.strip()
            data.append({
                "Tên doanh nghiệp": name,
                "Mã số thuế": mst,
                "Ngày cấp": date
            })
        except:
            continue

    # Ghi vào sheet
    df = pd.DataFrame(data)
    sheet_name = f"Trang_{page_number}"
    df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Tìm nút trang kế tiếp
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination li a[aria-label='Next']")
        parent_li = next_button.find_element(By.XPATH, "./..")
        if "disabled" in parent_li.get_attribute("class"):
            print("🔚 Đã đến trang cuối.")
            break
        else:
            next_button.click()
            page_number += 1
            time.sleep(2)
    except:
        print(" Không tìm thấy nút kế tiếp.")
        break

# Lưu file Excel
excel_writer.close()
driver.quit()
print(" Đã lưu dữ liệu vào 'masothue.xlsx'")
