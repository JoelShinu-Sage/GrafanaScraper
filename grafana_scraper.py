import os
import time
import logging
import configparser
from slack_sdk import WebClient
from selenium import webdriver

# Set up logging
logging.basicConfig(filename='grafana_scraper.log', level=logging.INFO)

# Read configuration values
config = configparser.ConfigParser()
config.read('config.ini')

grafana_url = config.get('Grafana', 'url')
api_key = config.get('Credentials', 'api_key')
slack_token = config.get('Credentials', 'slack_token')
output_dir = config.get('Screenshots', 'output_dir')
dashboard1_id = config.get('Dashboards', 'dashboard1_id')
dashboard2_id = config.get('Dashboards', 'dashboard2_id')
channel_id = config.get('Slack', 'channel_id')

# Set up the Slack client
slack_client = WebClient(token=slack_token)

# Set up the Selenium web driver
driver = webdriver.Chrome()

# Function to capture screenshots
def capture_screenshot(dashboard_id, output_file):
    dashboard_url = f"{grafana_url}/d/{dashboard_id}/"
    driver.get(dashboard_url)
    time.sleep(5)  # Wait for the dashboard to load completely
    driver.save_screenshot(output_file)
    logging.info(f"Screenshot captured: {output_file}")

# Function to post screenshot and error logs to Slack
def post_to_slack(image_file, error_logs):
    try:
        response = slack_client.files_upload(
            channels=channel_id,
            file=image_file,
            initial_comment="Screenshot from Grafana dashboard",
            title="Grafana Dashboard Screenshot"
        )
        logging.info("Screenshot posted to Slack")
    except Exception as e:
        logging.error(f"Error posting screenshot to Slack: {str(e)}")

    if error_logs:
        message = f"Error logs:\n{error_logs}"
        try:
            slack_client.chat_postMessage(channel=channel_id, text=message)
            logging.info("Error logs posted to Slack")
        except Exception as e:
            logging.error(f"Error posting error logs to Slack: {str(e)}")

# Capture screenshots and process the dashboards
try:
    # Capture screenshot for dashboard 1
    screenshot_file1 = os.path.join(output_dir, 'dashboard1.png')
    capture_screenshot(dashboard1_id, screenshot_file1)

    # Capture screenshot for dashboard 2
    screenshot_file2 = os.path.join(output_dir, '
