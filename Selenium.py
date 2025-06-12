from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Cấu hình trình duyệt
options = Options()
# options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)


usernames = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]
password = "secret_sauce"
url = "https://www.saucedemo.com"

all_data = []

for username in usernames:
    print(f"\n Đang kiểm tra user: {username}")
    driver.get(url)

    try:
        wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        driver.find_element(By.ID, "user-name").clear()
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        if "inventory" in driver.current_url:
            print(f"[✓] Đăng nhập thành công với user: {username}")

            try:
                items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
                print(f"    ➤ Tìm thấy {len(items)} sản phẩm.")

                for item in items:
                    name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                    price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                    all_data.append({
                        "Username": username,
                        "Product Name": name,
                        "Price": price
                    })

            except TimeoutException:
                print(f"    ✗ Không thể tìm thấy sản phẩm với user: {username}")
                driver.save_screenshot(f"screenshot_{username}.png")
                print(f"    ➤ Đã chụp màn hình: screenshot_{username}.png")

        
            try:
                driver.find_element(By.ID, "react-burger-menu-btn").click()
                time.sleep(1.5)
                logout_btn = wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
                logout_btn.click()
                time.sleep(1)
            except TimeoutException:
                print(f"    Không thể đăng xuất với user: {username}")
        else:
            print(f"[✗] Đăng nhập thất bại với user: {username}")
            try:
                error_msg = driver.find_element(By.CLASS_NAME, "error-message-container").text
                print(f"    Thông báo lỗi: {error_msg}")
            except:
                print("    Không có thông báo lỗi.")
    except Exception as e:
        print(f"   Lỗi không xác định: {str(e)}")
        
driver.quit()


file_name = "saucedemo_products.xlsx"

if os.path.exists(file_name):
    existing_df = pd.read_excel(file_name)
    df = pd.concat([existing_df, pd.DataFrame(all_data)], ignore_index=True)
else:
    df = pd.DataFrame(all_data)

df.to_excel(file_name, index=False)
print(f"\n Đã lưu dữ liệu vào '{file_name}'")
