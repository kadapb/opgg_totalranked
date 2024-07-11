import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_chrome_driver():
    # Configure Selenium to use Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")

    # Setting to run in headless mode for speed
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    if getattr(sys, 'frozen', False):
        # If running as a bundle, the chromedriver is in the same directory as the executable
        chromedriver_path = os.path.join(sys._MEIPASS, "venv", "Scripts", "chromedriver.exe")
    else:
        # If running as a script, use the chromedriver in the current directory
        chromedriver_path = os.path.join("venv", "Scripts", "chromedriver.exe")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def iterate_through_seasons(player_name):
    driver = None
    total_sum = 0
    try:
        # Initialize the WebDriver
        driver = get_chrome_driver()
        actions = ActionChains(driver)  # Initialize ActionChains

        # Open the OP.GG page for the summoner
        url = f"https://www.op.gg/summoners/euw/{player_name}/champions"
        driver.get(url)

        # Handle privacy pop-up
        try:
            privacy_pop_up = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-47sehv'))
            )
            privacy_pop_up.click()  
        except Exception as e:
            print(f"Privacy pop-up not found or not clickable: {e}")

        # Click on the Ranked tab
        try:
            ranked_total = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ranked Total')]"))
            )
            ranked_total.click()  # click the ranked tab
        except Exception as e:
            print(f"Ranked tab not found or not clickable: {e}")

        # Function to reveal the season list
        def reveal_season_list():
            show_seasons_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-17jvkpw.ede2q241"))
            )
            show_seasons_button.click()

        reveal_season_list()

        # Iterate through each season
        for i in range(16):  # Assuming there are 16 seasons
            try:
                # Re-find the season buttons
                season_buttons = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".css-w2p1w6.ede2q243"))
                )

                # Select the season button
                season_button = season_buttons[i]
                season_name = season_button.text.strip()
                print(f"Season: {season_name}")
                season_button.click()
                try:
                    # Check for the presence of the champion-container div
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".champion-container"))
                    )
                    # Find win and loss elements
                    win_elements = driver.find_elements(By.CSS_SELECTOR, ".winratio-graph__text.left")
                    loss_elements = driver.find_elements(By.CSS_SELECTOR, ".winratio-graph__text.right")
                    # Extract numbers from win/loss/played elements and sum them
                    season_sum = 0

                    for win_element in win_elements:
                        wins = int(re.findall(r'\d+', win_element.text)[0])
                        season_sum += wins

                    for loss_element in loss_elements:
                        losses = int(re.findall(r'\d+', loss_element.text)[0])
                        season_sum += losses

                    if season_sum == 0:
                        played_elements = driver.find_elements(By.CSS_SELECTOR, ".css-1amolq6.eyczova1")
                        for played_element in played_elements:
                            played_text = played_element.text.strip()
                            played_match = re.match(r'(\d+)Played', played_text)
                            if played_match:
                                played_games = int(played_match.group(1))
                                season_sum += played_games

                    total_sum += season_sum  # Add season sum to total sum
                except:
                    print("Champion container not found.")            
                try:
                    ranked_total_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Ranked Total')]"))
                    )
                    actions.move_to_element(ranked_total_button).perform()
                except Exception as e:
                    print(f"Ranked Total button not found or not clickable: {e}")
                # Re-open the season list for the next iteration
                reveal_season_list()

            except Exception as e:
                print(f"Error clicking season button: {e}")

    except Exception as e:
        print(f"Error initializing WebDriver: {e}")

    finally:
        if driver:
            driver.quit()

        print(f"Total sum of wins and losses: {total_sum}")
        return total_sum

# Example usage
# player_name = "player-EUW"
# iterate_through_seasons(player_name)
