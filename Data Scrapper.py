
import bs4 as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

year = '2023'
start_date = pd.to_datetime('01/01/'+year, format='%d/%m/%Y')
end_date = pd.to_datetime('31/07/'+year, format='%d/%m/%Y')

main_url = 'https://www.supremecourt.vic.gov.au/daily-hearing-list'


driver = webdriver.Chrome(options=Options())
driver.get(main_url)



current_date = start_date
all_data = []
while True:
    datestr = current_date.strftime('%d/%m/%Y')
    print(datestr)
    # datepicker = driver.find_element(By.ID,'ui-datepicker-input')
    # driver.execute_script('argument[0].clear();',datepicker)
    while True:
        try:
            picker = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ui-datepicker-input")))
            time.sleep(0.2)
            picker.clear()
            time.sleep(0.2)
            break
        except:
            print('.')
    # datepicker.clear()
    # datepicker = driver.find_element(By.ID,'ui-datepicker-input').send_keys(datestr)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ui-datepicker-input"))).send_keys(datestr)
    time.sleep(0.5)
    # submit = driver.find_element(By.ID,'edit-submit-scv-hearing-list')
    # driver.execute_script('argument[0].click();', submit)
    while True:
        try:
            submit = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "edit-submit-scv-hearing-list")))
            time.sleep(0.2)
            submit.click()
            break
        except:
            print('/')

    while True:
        time.sleep(0.2)

        soup = bs.BeautifulSoup(driver.page_source, 'lxml')

        # Verify loaded page has correct date
        a = soup.find('div', class_='form-header')
        page_date = a.find('h2').text
        day = page_date.split(' ')[0]
        if day == 'Invalid':
            print('--- ERROR LOADING PAGE Invalid---', current_date)
        elif int(day) != current_date.day:
            print('--- ERROR LOADING PAGE Wrong day---', current_date)
        else:
            break

    time.sleep(1)
    groups = soup.find_all('div', class_='schedule group')
    for g in groups:
        court = g.find('h3').text
        tables = g.find_all('table', class_='cols-0')
        for t in tables:
            justices = t.find('caption').text
            b = t.find('tbody')
            TR = b.find_all('tr')
            for tr in TR:
                _time_ = tr.find('td', class_='views-field views-field-field-time').text
                case_number = tr.find('td', class_='views-field views-field-field-case-number').text
                location = tr.find('td', class_='views-field views-field-field-court-address').text
                matter = tr.find('td', class_='views-field views-field-field-body-content-simple').text
                hearing = tr.find('td', class_='views-field views-field-field-teaser').text
                row = [datestr, court, justices, _time_, case_number, location, matter, hearing]
                all_data.append(row)

    current_date += datetime.timedelta(days=1)
    # current_date = pd.to_datetime(current_date)

    # print(current_date , end_date, (current_date - end_date).days)
    if current_date > end_date:
        break

df = pd.DataFrame(data=all_data,
                  columns=['Date', 'Court', 'Justices', 'Time', 'Case number', 'Location', 'Matter', 'Hearing'])
df.to_csv('D:\Desktop\SCV\data.csv', index=False)













