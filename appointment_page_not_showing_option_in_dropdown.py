import requests
from parsel import Selector
import pygame
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_form_and_alarm():
    try:
        # Send a request to the URL
        url = "https://service2.diplo.de/rktermin/extern/appointment_showForm.do?locationCode=isla&realmId=108&categoryId=1600"
        payload = {}
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=isla&realmId=108&categoryId=1600',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the response content using parsel (Scrapy-like CSS selectors)
        selector = Selector(response.text)

        # Check if the form with ID "appointment_newAppointmentForm" exists
        select_options = selector.css('select#appointment_newAppointmentForm_fields_3__content option').extract()
        if len(select_options) > 6:
            logging.info("!!!!!!!!! The Appointment is Now Open ! Playing alarm sound...")
            # Initialize pygame mixer
            pygame.mixer.init()
            # Load the alarm sound
            pygame.mixer.music.load('wake_up.mp3')
            # Play the alarm sound for at least 5 minutes
            start_time = time.time()
            while time.time() - start_time < 80:  # 300 seconds = 5 minutes
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
                time.sleep(1)
            return True
        else:
            logging.info("Form not found.")
            return False

    except requests.RequestException as e:
        logging.error(f"Error occurred while making the request: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False


def main():
    while True:
        if check_form_and_alarm():
            break
        time.sleep(10)


if __name__ == "__main__":
    main()
