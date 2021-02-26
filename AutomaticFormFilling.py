#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2021/2/24 21:46
#@Author: 李明特
#@File  : AutomaticFormFilling.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 获取需要填报的学生信息
def getStu():
    with open('stuMessage.txt','r',encoding='utf-8') as f:
        lines = f.readlines()[5:]
        return lines

# 获取输入标签
def inputElement(driver):
    # 点击sheng、shi、qu的标签会跳出地区选择框，获取地区选择的输入框以输入地址
    inputElement = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/input')
    return inputElement

# 获取完成标签
def complete(driver):
    completeElement = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/div')
    return completeElement

# 获取选中标签
def select(driver):
    selectElement = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div[3]')
    return selectElement

# 定位，点击选择地区并输入关键字
def location(element,driver,key):
    element.click()
    time.sleep(1.5)
    # 调用获取input输入框的函数，并传入省份关键字
    inputElement(driver).send_keys(key)
    time.sleep(2)
    completeDiv = complete(driver)
    completeDiv.click()
    time.sleep(0.5)

# 模拟浏览器操作
def autoFunction(stuInfo):
    stu_list = list()
    for stu in stuInfo:
        stu.replace('\n','')
        stu_list.append(stu.split())
    for stu in stu_list:
        # 提取学号，拼接请求地址
        stuid = stu[1]
        url = 'http://dw10.fdzcxy.edu.cn/datawarn/ReportServer?formlet=app/yibao.frm&op=h5&xh=' + stuid +'#/form'
        print(url)
        print("正在填报 {} 的表格".format(stu[0]))
        driver = webdriver.Chrome()
        driver.get(url=url)
        try:
            shengElement = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="SHENG"]/div[2]/div[2]'))
            )
            shiElement = driver.find_element_by_xpath('//*[@id="SHI"]/div[2]/div[2]')
            quElement = driver.find_element_by_xpath('//*[@id="QU"]/div[2]/div[2]')

            # 分别定位省、市、区
            location(shengElement,driver,stu[2])
            location(shiElement,driver,stu[3])
            location(quElement,driver,stu[4])

            # 获取承诺填报的内容全部真实的确认按钮
            confirmElement = driver.find_element_by_xpath('//*[@id="CHECK"]/div[2]/div[2]/input')
            driver.execute_script("arguments[0].scrollIntoView();", confirmElement)
            # 点击承诺按钮并提交
            confirmElement.click()
            time.sleep(0.5)
            # 获取提交按钮
            submitElement = driver.find_element_by_xpath('//*[@id="SUBMIT"]/div[2]')
            submitElement.click()
            time.sleep(1)
        finally:
            driver.quit()
    print("填报完毕")
if __name__ == '__main__':
    stus = getStu()
    autoFunction(stus)