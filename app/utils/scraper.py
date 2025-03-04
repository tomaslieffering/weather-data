from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from utils.region import Region
import os
from dotenv import load_dotenv

class Scraper:
  """ A utitlity class which can scrap a webpage and return the appropriate data """
  
  driver = None
  site = None
  
  def __init__(self):
    self.driver = self.setup_driver()
    load_dotenv()
    self.site = os.getenv('TARGET_SITE')

  def setup_driver(self):
    """ Initialises the selenium webdriver with the appropriate options"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Chrome(options=options)
  
  def get_weather(self, position):
    """ Gets the page for the given position and pull the time, rain and wind data

    Args:
        position: The position(latitude, longitude) of which the closest weather data should be returned

    Returns:
        A dictionary containing the 64 hourly weather data for the given position
    """
    soup = self.get_page(position)
    metrics = soup.find_all("div", class_="ForecastSlider-container")
    
    times = self.get_text_metrics(metrics[0])
    rains = self.get_text_metrics(metrics[1])
    speeds, directions = self.get_wind_metrics(metrics[3])
    
    results = {}
    
    for index, (time, rain, speed, direction) in enumerate(zip(times, rains, speeds, directions)):
      results[index] = {
        "time": time,
        "rain": rain,
        "speed": speed,
        "direction": direction
      }
          
    return results
  
  def get_text_metrics(self, times_section):
    """ Pull text only metrics such as time and rainfall from the HTML

    Args:
        times_section: The section of the HTML that contains the text metrics

    Returns:
        An array of the metrics pulled from the HTML
    """
    output = []
    metrics = times_section.find_all("div", class_="ForecastSlider-item")
    for metric in metrics:
      output.append(metric.text)
      
    return output
  
  def get_wind_metrics(self, winds_section):
    """ Pulls the wind speed and direction from the HTML
    
    Args:
        winds_section: The section of the HTML that contains the wind metrics

    Returns:
        Two array of the of wind speed and wind direction metrics pulled from the HTML
    """
    speed = []
    direction = []
    winds = winds_section.find_all("div", class_="ForecastSlider-item")
    for wind in winds:
      wind_value = wind.text.replace(" ", "")
      direction_value = wind_value.rstrip('0123456789')
      direction.append(direction_value)
      speed.append(wind_value[len(direction_value):])
      
    return speed, direction
  
  def destroy_driver(self):
    """ Destroys the selenium web driver """
    self.driver.quit()
  
  def get_page(self, position):
    """ Get the weather page based on the current position

    Args:
        position: The position(latitude, longitude) of which the closest available weather page should be returned

    Returns:
        A Beautiful Soup parsed HTML document of the appropriate page
    """
    region = Region()
    closet = region.compute_closest(position)
    url = f'{self.site}{closet["name"]}' 
    
    self.driver.get(url)
    
    try:
      element_present = EC.presence_of_element_located((By.CLASS_NAME, 'Modal-Component--content-graph'))
      WebDriverWait(self.driver, 5).until(element_present)
    except TimeoutException:
      return 0
    
    return BeautifulSoup(self.driver.page_source, "html.parser")
