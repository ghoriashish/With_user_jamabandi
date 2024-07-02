# -*- coding: utf-8 -*-
# Script developed by Ashish Ghori
# Version 1.0

import csv
import html
import os
import random
import re
import time
import zipfile
import math
import unicodedata
from lxml import html
from selenium.webdriver.common.by import By
import sys


class WithUserJamabandi:
    def __init__(self):
        self.output_file = 'Output'
        self.current_path = os.path.dirname(os.path.abspath(__file__) + "/")
        self.current_path = '\\'.join(self.current_path.split('\\')[:-1]) + '\\'

    def Initiate(self):
        try:
            print(self.current_path)
            #text output headers name
            self.puse_data_to_file("district_name\tdistrict_code\ttehsil_name\ttehsil_code\tvillage_name\tvillage_code\tjamabandi_Year\tkhasra_number\tkhewat_no\tkhatoni_no\thtml_link\tinner_details\n")
            """--below csv code coments--"""
            self.input_url = 'https://jamabandi.nic.in/land%20records/NakalRecord'
            # with open('test.csv', mode='a', newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerows([['district_name','district_code','tehsil_name','tehsil_code','village_name','village_code','jamabandi_Year','khewat_no','khatoni_no','html_link','inner_details']])
            self.Hitting_url(self.input_url, False, False)
        except Exception as e:
            print(e)

    def Hitting_url(self, url, Main, is_paginated):
        self.retries = 0
        driver = None
        while True:
            try:
                self.close_diver()
                self.diver = self.get_prox_driver()
                self.diver.get(url)
                time.sleep(2)
                by_khasra_clik = self.diver.find_element(By.XPATH, "//*[contains(text(),'By Khasra/Survey No')]")
                by_khasra_clik.click()
                time.sleep(2)
                district_name = ''
                district_code = ''
                tehsil_name = ''
                tehsil_code = ''
                village_name = ''
                village_code = ''

                '''------district--------'''
                try:
                    tree_district = html.fromstring(self.diver.page_source)
                    check_total_district = tree_district.xpath("//*[contains(text(),'Select District')]//..//select//option")
                    print('-------district_name and district_code print in below------------------')
                    for i in range(2,len(check_total_district)):
                        district_name = tree_district.xpath(f"//*[contains(text(),'Select District')]//..//select//option[{i}]//text()")[0]
                        district_code = tree_district.xpath(f"//*[contains(text(),'Select District')]//..//select//option[{i}]//@value")[0]
                        print(district_name,'------>',district_code)

                    num_district_code = int(input("-----Enter a above district_code any one--: "))
                    select_district_clik = self.diver.find_element(By.XPATH, f"//*[contains(text(),'Select District')]//..//select//option[@value={str(num_district_code)}]")
                    select_district_clik.click()
                    time.sleep(2)
                except Exception as e:
                    print('Please enter valid  district_code ')
                    continue

                """------tehsil----"""
                try:
                    tree_tehsil = html.fromstring(self.diver.page_source)
                    check_total_tehsil = tree_tehsil.xpath("//*[contains(text(),'Select Tehsil/ Sub-Tehsil')]//..//select//option")
                    print(f'-------The tehsil_name and tehsil_number in {district_name} district are given below-----------------')
                    for j in range(2, len(check_total_tehsil)):
                        tehsil_name = tree_tehsil.xpath(f"//*[contains(text(),'Select Tehsil/ Sub-Tehsil')]//..//select//option[{j}]//text()")[0]
                        tehsil_code = tree_tehsil.xpath(f"//*[contains(text(),'Select Tehsil/ Sub-Tehsil')]//..//select//option[{j}]//@value")[0]
                        print(tehsil_name,'-------->',tehsil_code)
                    num_tehsil_code = int(input("-----Enter a above tehsil_code any one--: "))
                    select_tehsil_clik = self.diver.find_element(By.XPATH,f"//*[contains(text(),'Select Tehsil/ Sub-Tehsil')]//..//select//option[@value={str(num_tehsil_code)}]")
                    select_tehsil_clik.click()
                    time.sleep(2)
                except Exception as e:
                    print('Please enter valid tehsil_code ')
                    continue

                """--------village-----------"""
                try:
                    tree_village = html.fromstring(self.diver.page_source)
                    check_total_village = tree_village.xpath("//*[contains(text(),'Select Village')]//..//select//option")
                    print(f'-------The village_name and village_number in {tehsil_name} tehsil are given below-----------------')
                    for k in range(2, len(check_total_village)):
                        village_name = tree_village.xpath(f"//*[contains(text(),'Select Village')]//..//select//option[{k}]//text()")[0]
                        village_code = tree_village.xpath(f"//*[contains(text(),'Select Village')]//..//select//option[{k}]//@value")[0]
                        print(village_name,'---------->',village_code)
                    num_village_code = int(input("-----Enter a above village_code any one--: "))
                    select_village_clik = self.diver.find_element(By.XPATH,f"//*[contains(text(),'Select Village')]//..//select//option[@value={str(num_village_code)}]")
                    select_village_clik.click()
                    time.sleep(2)
                except Exception as e:
                    print('Please enter valid village_code ')
                    continue
                """-------click year--"""

                select_year_clik = self.diver.find_element(By.XPATH,"//*[contains(text(),'Jamabandi Year')]//..//select//option[2]")
                select_year_clik.click()
                tree_year = html.fromstring(self.diver.page_source)
                year = tree_year.xpath("//*[contains(text(),'Jamabandi Year')]//..//select//option[2]//text()")[0]
                time.sleep(2)
                tree_khasra = html.fromstring(self.diver.page_source)
                check_khasra_total = tree_khasra.xpath("//*[contains(text(),'Khasra')]//..//select//option")
                for l in range(2, len(check_khasra_total)):
                    try:
                        data_list =[]
                        khasra_number = tree_khasra.xpath(f"//*[contains(text(),'Khasra')]//..//select//option[{l}]//text()")[0]
                        select_khasra_clik = self.diver.find_element(By.XPATH, f"//*[contains(text(),'Khasra')]//..//select//option[{l}]")
                        select_khasra_clik.click()
                        time.sleep(2)

                        select_nakal_clik = self.diver.find_element(By.XPATH,"//td//a[contains(text(),'Nakal')]")
                        select_nakal_clik.click()
                        tree = html.fromstring(self.diver.page_source)
                        khewat_no = tree.xpath("//td//a[contains(text(),'Nakal')]//..//following-sibling::td[1]//text()")[0]
                        khatoni_no = tree.xpath("//td//a[contains(text(),'Nakal')]//..//following-sibling::td[2]//text()")[0]
                        html_url = 'https://jamabandi.nic.in/land%20records/Nakal_khewat'
                        inner_details_list = []
                        hadbast_no = tree.xpath("//div[contains(text(),'Hadbast No.')]//following-sibling::div//span//text()")[0]

                        inner_details_list.append(f'village(गांव) : {village_name}')
                        inner_details_list.append(f'hadbastNo(हदब):{hadbast_no}')
                        inner_details_list.append(f'tehsil(तहसील):{tehsil_name}')
                        inner_details_list.append(f'district(िजला):{district_name}')
                        inner_details_list.append(f'year (साल):{year}')
                        inner_details = ' | '.join(inner_details_list)
                        if khasra_number != '':
                            data_list.append(district_name)
                            data_list.append(district_code)
                            data_list.append(tehsil_name)
                            data_list.append(tehsil_code)
                            data_list.append(village_name)
                            data_list.append(village_code)
                            data_list.append(year)
                            data_list.append(khasra_number)
                            data_list.append(khewat_no)
                            data_list.append(khatoni_no)
                            data_list.append(html_url)
                            data_list.append(inner_details)
                            out_data = '\t'.join(data_list)+'\n'
                            self.puse_data_to_file(out_data)
                            print('data insert in output.txt file')
                    except Exception as e:
                        print('next khasra')

            except Exception as e:
                print('please check in selection district_name,tehsil_name,village_name,jamabandi_Year')
                self.close_diver()
                break


    def close_diver(self):
        try:
            self.diver.close()
            self.diver.quit()
        except Exception as e:
            pass

    def remove_junk(self, text):
        text = re.sub('\s+|\\\\t|\\t', ' ', str(text).strip())
        text = re.sub('\\\\n|\\\\r|\\n|\\r', '', text.strip())
        text = str(text).replace('\r', ' ').replace('\n', '').replace('\t', ' ')
        text = text.replace('    ', ' ').replace('  ', ' ')
        text = text.replace(';', '')
        text = text.strip()
        return text

    def puse_data_to_file(self, data):
        with open(self.current_path + self.output_file + ".txt", "a", encoding='utf-8') as f:
            f.write(data)

    def puse_data_to_csv(self, data):
        with open('Output.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([data])


    def get_user_agent(self):
        temp = [
            "Mozilla/5.0 (Linux; Android 12; SM-A137F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; 2201117SY) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.61 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 7.0; SM-G920F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; DN2103) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
            "yacybot (/global; amd64 Linux 5.10.113; java 1.8.0_242; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.10.0-17-cloud-amd64; java 11.0.16; Europe/en) http://yacy.net/bot.html",
            "yacybot (webportal-global; amd64 Linux 5.4.0-122-generic; java 1.8.0_242; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; aarch64 Linux 5.15.0-1013-oracle; java 17; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 4.19.0-20-amd64; java 1.8.0_345; Europe/en) http://yacy.net/bot.html",
            "yacybot (intranet-local; amd64 Linux 5.14.21-150400.24.11-default; java 1.8.0_332; Europe/de) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.10.0-15-amd64; java 11.0.15; Europe/ro) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.15.38; java 17.0.2; US/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.13.0-52-generic; java 11.0.15; Europe/es) http://yacy.net/bot.html",
            "yacybot (webportal-global; amd64 Linux 5.13.0-52-generic; java 11.0.15; Europe/es) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.10.0-9-amd64; java 11.0.14; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.18.5-gentoo; java 17.0.3; Europe/de) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.17.9-gnu-hardened1-1-hardened; java 18.0.1.1; Europe/en) http://yacy.net/bot.html",
            "yacybot (freeworld/global; amd64 Linux 5.10.0-13-amd64; java 11.0.15; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Windows 10 10.0; java 1.8.0_331; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.17.7-gnu-hardened1-1-hardened; java 1.8.0_332; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.10.0-12-amd64; java 1.8.0_212; GMT/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.17.7-gentoo; java 17.0.3; Europe/de) http://yacy.net/bot.html",
            "yacybot (-global; amd64 Linux 4.19.0-20-amd64; java 11.0.15; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 4.15.0-176-generic; java 1.8.0_242; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 4.4.301; java 1.8.0_322; US/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.17.4-arch1-1; java 18.0.1; US/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.4.0-109-generic; java 11.0.15; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.16.12-artix1-1; java 17.0.3; America/en) http://yacy.net/bot.html",
            "yacybot (-global; amd64 Linux 5.13.0-21-generic; java 1.8.0_242; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Windows 10 10.0; java 1.8.0_271; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.10.28-Unraid; java 1.8.0_242; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.15.34-gentoo; java 17.0.2; Poland/pl) http://yacy.net/bot.html",
            "yacybot (-global; amd64 FreeBSD 9.2-RELEASE-p10; java 1.7.0_65; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 FreeBSD 13.0-RELEASE-p8; java 1.8.0_322; Europe/en) http://yacy.net/bot.html",
            "yacybot (-global; amd64 Linux 5.17.0; java 11.0.14.1; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.15.29; java 1.8.0_242; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.15.12-gnu-hardened1-1-hardened; java 17.0.3; Europe/en) http://yacy.net/bot.html",
            "yacybot (-global; amd64 Linux 5.17.0; java 11.0.14; Europe/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Windows 10 10.0; java 17.0.2; America/en) http://yacy.net/bot.html",
            "yacybot (-global; amd64 Linux 5.15.12-gnu-1; java 17.0.3; UTC/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 4.19.0-19-amd64; java 11.0.14; America/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Linux 5.4.0-99-generic; java 11.0.13; Etc/en) http://yacy.net/bot.html",
            "yacybot (/global; amd64 Windows 11 10.0; java 17.0.2; Europe/en) http://yacy.net/bot.html",

        ]
        temp_user_agent = random.choice(temp).replace("\n", "")
        return temp_user_agent

    def get_prox_driver(self):
        """--------run code-----"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            # chrome_options.add_argument(f'user-agent={str(self.get_user_agent())}')
            """---chromedrive----"""
            # driver_path = r'G:\Ashish\All_project\New folder\advarisk\jamabandi\chromedriver.exe'
            # driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            """----withut path-----"""
            driver = webdriver.Chrome(options=chrome_options)
            return driver

        except Exception as e:
            print('Error in get_prox_driver function')

if __name__ == "__main__":
    class_obj = WithUserJamabandi()
    class_obj.Initiate()
