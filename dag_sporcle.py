from numpy import append
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
from os.path import expanduser
from pathlib import Path
from airflow.models import DAG
from datetime import datetime
from datetime import timedelta
from airflow.operators import BashOperator
from airflow.operators import PythonOperator
from sporcle import SporcleAutobot

default_args = {
    'owner': 'balany1',
    'depends_on_past': False,
    'email': ['andrewmcnamara@live.co.uk'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2023, 2, 8), # If you set a datetime previous to the curernt date, it will try to backfill
    'retry_delay': timedelta(minutes=5),
    'end_date': datetime(2024, 1, 1),
}

bot = SporcleAutobot()

with DAG(dag_id='sporcle_bot',
         default_args=default_args,
         schedule_interval='09 13 * * *',
         catchup=False,
         tags=['sporcle']
         ) as dag:
    # define tasks
    load_page = PythonOperator(
        task_id = 'load_page',
        python_callable = bot.load_page,
        )
    accept_cookies = PythonOperator(
        task_id = 'accept_cookies',
        python_callable = bot.accept_cookies,
        )
    login = PythonOperator(
        task_id = 'login',
        python_callable = bot.login,
        )
    play_game = PythonOperator(
        task_id = 'play_game',
        python_callable = bot.play_game,
        )
    find_answer = PythonOperator(
        task_id = 'find_answer',
        python_callable = bot.find_answer,
        )
    quit= PythonOperator(
        task_id = 'quit',
        python_callable = bot.driver.quit,
        )