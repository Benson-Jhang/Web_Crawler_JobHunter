#coding=utf-8
import urllib
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlencode
import json
import re
import csv
from time import strftime
import datetime
import os
import sys, time
import httplib2

count = 0
def get_web_page(url):
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print('Invalid url:', resp.url)
            return 'None'
        else:
            return resp.text
    except:
        print('Error:' + url)
        return 'None'


def get_list_data(dom, key, _patternlist):
    article = []
    first_level_job_data = []
    soup = BeautifulSoup(dom, 'html.parser')
    article = soup.findAll('article', 'b-block--top-bord job-list-item b-clearfix js-job-item ')
    for list in article:
        is_match = False
        company_name = list['data-cust-name']
        industry_name = list['data-indcat-desc']
        job_name = list['data-job-name']
        job_location = list.findAll('li')[3].text
        job_link = list.find('a', 'js-job-link')['href']
        job_link = 'https:' + job_link

        #print(company_name + industry_name + job_name +'@@')
        #test12 = company_name + industry_name + job_name
        #if test12.find("亞洲遊科技股份有限公司網際網路相關業Data Engineer"):
        #    test12 = '1'

        for pattern in _patternlist:
            if bool(pattern.search(job_name)):
                is_match = True
                break

        if is_match is True:
            # 用JOB LINK 取得 "工作內容"
            global count
            count = count + 1

            resp = get_web_page(job_link)
            job_content = ''
            job_other_content = ''
            if resp != 'None':
                soup = BeautifulSoup(resp, 'html.parser')

                try:
                    if soup.find('section', 'info').find('p') is not None:
                        job_content = soup.find('section', 'info').find('p').text
                except:
                    print(job_link)
                    continue

                job_other = soup.find('div', 'grid-left').text
                if bool(re.search(r"(其他條件.*).*(公司福利)", job_other, re.DOTALL)):
                    job_other_content = re.search(r"(其他條件.*).*(公司福利)", job_other, re.DOTALL).group(1)
                elif bool(re.search(r"(其他條件.*).*(聯絡方式)", job_other, re.DOTALL)):
                    job_other_content = re.search(r"(其他條件.*).*(聯絡方式)", job_other, re.DOTALL).group(1)
                else:
                    print(job_link, '#2')

            first_level_job_data.append({
                'company_name': company_name,
                'industry_name': industry_name,
                'job_name': job_name,
                'job_location': job_location,
                'job_qualification': job_content.strip(),
                'job_other_qualification': job_other_content.strip(),
                'job_link': job_link
            })

        # first_level_job_data.append({
        #     'company_name': company_name,
        #     'industry_name': industry_name,
        #     'job_name': job_name,
        #     'job_location': job_location
        #     'job_link': job_link,
        # })

    return first_level_job_data


def get_total_page(dom):
    total_page = 1
    soup = BeautifulSoup(dom, 'html.parser')
    res = soup.findAll('script')[3].text
    # menu = json.loads(re.search(r"var initFilter\s*=\s*(.*);", res).group(1))
    try:
        s = json.loads(re.search(r"var initFilter\s*=\s*(.*);", res).group(1))
        if s is None:
            pass
        else:
            total_page = s['totalPage']
    except:
        pass
    return total_page


def traceback(err):
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    traceback = sys.exc_info()[2]
    errmsg = str(err) + 'exception in line' + str(traceback.tb_lineno)
    return errmsg

if __name__ == '__main__':
    job_data_list = []
    payload = {
        'ro': '0',
        'jobcat': '2007000000',
        #'area': '6001008000,6001006000',  # 台中,新竹
        #'area': '6001001000,6001002000',   # 台北,新北
        'area': '6001001000',
        'order': '1',
        'asc': '0',
        'kwop': '7',
        'page': '1',
        'mode': 's',
        'jobsource': 'n104bank1'
    }
    para_str = urllib.parse.urlencode(payload)
    url = 'https://www.104.com.tw/jobs/search/'
    param_keyword = {'Big Data', 'Data Scientist', 'Data Analyst', 'Data Engineer', 'Data Analysis', '大數據',
                     '數據分析', '數據工程師'}
    pattern_list = []
    pattern1 = re.compile(r'.*(big).*\s*(data)', re.I)  # Big Data
    pattern2 = re.compile(r'.*(data).*\s*(scientist|analyst|Engineer|Analysis)', re.I)  # Data Scientist
    pattern3 = re.compile(r'(數據|大數據)')  # 大數據
    pattern_list.append(pattern1)
    pattern_list.append(pattern2)
    pattern_list.append(pattern3)

    for k in param_keyword:
        param_page = 1
        bool_next_page = True
        while bool_next_page:
            main_url = '{address}?{parameter}&keyword={keyword}&page={page}'.format(address=url, parameter=para_str,
                                                                                    keyword=quote(k), page=param_page)
            resp = get_web_page(main_url)

            if param_page == 1:
                page_number = get_total_page(resp) # 抓總共有幾頁資料

            if param_page <= page_number:
                data_list = get_list_data(resp, k, pattern_list)
                job_data_list.extend(data_list)
                param_page += 1
            else:
                bool_next_page = False

    # 輸出CSV檔案
    try:
        keys = job_data_list[0].keys()
        with open('job.csv',  'w', encoding='utf_8_sig', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            for row in job_data_list:
                dict_writer.writerow(row)
    except Exception as e:
        if not os.path.exists('log.txt'):
            f = open('log.txt', 'w', encoding='UTF-8')
        with open("log.txt", "a") as file:
            file.write('Error:' + str(datetime.datetime.now()) + str(traceback(e)) + '\r\n')

