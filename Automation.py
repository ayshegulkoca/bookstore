
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class AyseBookStoreTester:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0

    def setup_driver(self):
        try:
            print("🔧 Setting up Chrome driver...")
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 15)
            self.driver.maximize_window()
            print("✅ Chrome driver setup successful!")
            return True
        except Exception as e:
            print(f"❌ Failed to setup driver: {str(e)}")
            return False

    def load_page(self):
        try:
            file_path = "file:///C:/Users/Aysegul%20Koca/OneDrive/Desktop/ITE368/ITE368FINALPROJECT.html"
            print(f"🌐 Loading page: {file_path}")
            self.driver.get(file_path)
            time.sleep(2)
            if "Ayse's Book Store" in self.driver.title:
                print("✅ Page loaded successfully!")
                return True
            else:
                print("❌ Page failed to load correctly")
                return False
        except Exception as e:
            print(f"❌ Failed to load page: {str(e)}")
            return False

    def log_test_result(self, test_name, passed, details=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f" Details: {details}")
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

    def test_valid_login(self):
        try:
            print(" Testing Valid Login...")
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_field.clear()
            email_field.send_keys("ayse@bookstore.com")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys("password123")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            success = False
            try:
                WebDriverWait(self.driver, 8).until(
                    lambda driver: not driver.find_element(By.ID, "loginSuccess").get_attribute("class").__contains__("hidden")
                )
                success_element = self.driver.find_element(By.ID, "loginSuccess")
                if "Login successful" in success_element.text:
                    success = True
            except:
                pass
            if not success:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.text_to_be_present_in_element((By.ID, "loginSuccess"), "Login successful")
                    )
                    success = True
                except:
                    pass
            if not success:
                time.sleep(3)
                success_element = self.driver.find_element(By.ID, "loginSuccess")
                if not success_element.get_attribute("class").__contains__("hidden") and "Login successful" in success_element.text:
                    success = True
            if success:
                self.log_test_result("Valid Login", True, "Login successful message displayed")
                return True
            else:
                self.log_test_result("Valid Login", False, "Login success message not displayed")
                return False
        except Exception as e:
            self.log_test_result("Valid Login", False, f"Exception: {str(e)}")
            return False

    def test_invalid_login(self):
        try:
            print(" Testing Invalid Login...")
            self.driver.get(self.driver.current_url)
            time.sleep(1)
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_field.clear()
            email_field.send_keys("wrong@email.com")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys("wrongpassword")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            time.sleep(2)
            error_element = self.driver.find_element(By.ID, "loginError")
            if "Invalid email or password" in error_element.text and not error_element.get_attribute("class").__contains__("hidden"):
                self.log_test_result("Invalid Login", True, "Error message displayed correctly for invalid credentials")
            else:
                self.log_test_result("Invalid Login", False, "Error message not displayed for invalid credentials")
                return False
            return True
        except Exception as e:
            self.log_test_result("Invalid Login", False, f"Exception: {str(e)}")
            return False

    def login_for_tests(self):
        try:
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_field.clear()
            email_field.send_keys("ayse@bookstore.com")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys("password123")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            time.sleep(4)
            return True
        except:
            return False

    def test_navigation_to_search(self):
        try:
            print(" Testing Navigation to Browse Books...")
            browse_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Browse Books')]")))
            browse_link.click()
            time.sleep(2)
            search_section = self.driver.find_element(By.ID, "searchSection")
            if not search_section.get_attribute("class").__contains__("hidden"):
                self.log_test_result("Navigation to Browse Books", True, "Successfully navigated to browse books section")
                return True
            else:
                self.log_test_result("Navigation to Browse Books", False, "Browse books section not visible")
                return False
        except Exception as e:
            self.log_test_result("Navigation to Browse Books", False, f"Exception: {str(e)}")
            return False

    def test_show_all_books(self):
        try:
            print("Testing Show All Books...")
            show_all_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show All')]")))
            show_all_button.click()
            time.sleep(2)
            book_cards = self.driver.find_elements(By.CLASS_NAME, "book-card")
            if len(book_cards) > 0:
                self.log_test_result("Show All Books", True, f"Successfully displayed {len(book_cards)} books")
                return True
            else:
                self.log_test_result("Show All Books", False, "No books displayed")
                return False
        except Exception as e:
            self.log_test_result("Show All Books", False, f"Exception: {str(e)}")
            return False

    def test_search_by_title(self):
        try:
            print("🔍 Testing Search by Title...")
            search_input = self.wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
            search_input.clear()
            search_input.send_keys("Winnie-the-Pooh")
            search_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
            search_button.click()
            time.sleep(2)
            book_cards = self.driver.find_elements(By.CLASS_NAME, "book-card")
            WinniethePooh_found = False
            for card in book_cards:
                if "Winnie-the-Pooh" in card.text:
                    WinniethePooh_found = True
                    break
            if WinniethePooh_found:
                self.log_test_result("Search by Title", True, "Successfully found 'Winnie-the-Pooh' by title search")
                return True
            else:
                self.log_test_result("Search by Title", False, "Could not find 'Winnie-the-Pooh' in search results")
                return False
        except Exception as e:
            self.log_test_result("Search by Title", False, f"Exception: {str(e)}")
            return False

    def test_search_by_author(self):
        try:
            print("🔍 Testing Search by Author...")
            search_input = self.wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
            search_input.clear()
            search_input.send_keys("Dr. Seuss")
            search_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
            search_button.click()
            time.sleep(2)
            book_cards = self.driver.find_elements(By.CLASS_NAME, "book-card")
            DrSeuss_books_found = 0
            for card in book_cards:
                if "Dr. Seuss" in card.text:
                   DrSeuss_books_found += 1
            if DrSeuss_books_found > 0:
                self.log_test_result("Search by Author", True, f"Successfully found {DrSeuss_books_found} books by Dr. Seuss") 
                return True
            else:
                self.log_test_result("Search by Author", False, "Could not find books by Dr. Seuss")
                return False
        except Exception as e:
            self.log_test_result("Search by Author", False, f"Exception: {str(e)}")
            return False

    def test_add_to_cart(self):
        try:
            print("🛒 Testing Add to Cart...")
            show_all_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show All')]")))
            show_all_button.click()
            time.sleep(2)
            add_to_cart_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
            if len(add_to_cart_buttons) > 0:
                cart_count_element = self.driver.find_element(By.ID, "cartCount")
                initial_count = int(cart_count_element.text)
                add_to_cart_buttons[0].click()
                time.sleep(1)
                new_count = int(cart_count_element.text)
                if new_count > initial_count:
                    self.log_test_result("Add to Cart", True, f"Cart count increased from {initial_count} to {new_count}")
                    return True
                else:
                    self.log_test_result("Add to Cart", False, "Cart count did not increase")
                    return False
            else:
                self.log_test_result("Add to Cart", False, "No 'Add to Cart' buttons found")
                return False
        except Exception as e:
            self.log_test_result("Add to Cart", False, f"Exception: {str(e)}")
            return False

    def test_cart_functionality(self):
        try:
            print("🛒 Testing Cart Functionality...")
            cart_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Cart')]")))
            cart_link.click()
            time.sleep(2)
            cart_section = self.driver.find_element(By.ID, "cartSection")
            if not cart_section.get_attribute("class").__contains__("hidden"):
                cart_items = self.driver.find_elements(By.CLASS_NAME, "cart-item")
                if len(cart_items) > 0:
                    self.log_test_result("Cart Display", True, f"Cart displays {len(cart_items)} items correctly")
                    return True
                else:
                    cart_container = self.driver.find_element(By.ID, "cartItems")
                    if "empty" in cart_container.text.lower():
                        self.log_test_result("Cart Display", True, "Empty cart message displayed correctly")
                        return True
                    else:
                        self.log_test_result("Cart Display", False, "Cart display issue")
                        return False
            else:
                self.log_test_result("Cart Display", False, "Cart section not visible")
                return False
        except Exception as e:
            self.log_test_result("Cart Display", False, f"Exception: {str(e)}")
            return False

    def test_checkout_process(self):
        try:
            print("💳 Testing Checkout Process...")
            cart_section = self.driver.find_element(By.ID, "cartSection")
            if cart_section.get_attribute("class").__contains__("hidden"):
                cart_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Cart')]")
                cart_link.click()
                time.sleep(2)
            try:
                checkout_button = self.driver.find_element(By.ID, "checkoutBtn")
                checkout_button.click()
                time.sleep(2)
                checkout_message = self.driver.find_element(By.ID, "checkoutMessage")
                if not checkout_message.get_attribute("class").__contains__("hidden"):
                    if "Order Successful" in checkout_message.text:
                        self.log_test_result("Checkout Process", True, "Checkout completed successfully with order confirmation")
                        return True
                    else:
                        self.log_test_result("Checkout Process", False, "Checkout message displayed but no success confirmation")
                        return False
                else:
                    self.log_test_result("Checkout Process", False, "No checkout confirmation message displayed")
                    return False
            except Exception as e:
                if "empty" in str(e).lower():
                    self.log_test_result("Checkout Process", True, "Checkout properly handled empty cart")
                    return True
                else:
                    raise e
        except Exception as e:
            self.log_test_result("Checkout Process", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        print(" Starting Ayse's Book Store Automated Tests...")
        print("=" * 50)
        if not self.setup_driver():
            return False
        if not self.load_page():
            return False
        self.test_valid_login()
        time.sleep(1)
        self.test_invalid_login()
        time.sleep(1)
        if self.login_for_tests():
            print("\n🔑 Logged in for feature testing...")
            self.test_navigation_to_search()
            self.test_show_all_books()
            self.test_search_by_title()
            self.test_search_by_author()
            self.test_add_to_cart()
            self.test_cart_functionality()
            self.test_checkout_process()
        else:
            print("❌ Could not login for feature tests")
        self.print_final_report()
        return True

    def print_final_report(self):
        print("\n" + "=" * 50)
        print(" FINAL TEST REPORT")
        print("=" * 50)
        total_tests = len(self.test_results)
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        if self.failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['passed']:
                    print(f" • {result['test']}: {result['details']}")
        print("\n✅ PASSED TESTS:")
        for result in self.test_results:
            if result['passed']:
                print(f" • {result['test']}")
        print("=" * 50)

    def cleanup(self):
        if self.driver:
            print("🧹 Cleaning up...")
            self.driver.quit()

def main():
    tester = AyseBookStoreTester()
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    finally:
        tester.cleanup()
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
