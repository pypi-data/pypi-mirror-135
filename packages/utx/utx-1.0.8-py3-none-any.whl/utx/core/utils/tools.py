#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  8/31/2021 9:42 PM
@Desc    :  Tools line.
"""
import base64
import platform
import subprocess
import re

import requests
import urllib3
from tqdm import tqdm
from airtest.utils.logger import get_logger
from airtest.core.api import *
from airtest.core.android.adb import ADB
import os
import configparser

LOGGING = get_logger(__name__)


def allure_report(report_path, report_html):
    """
    Generate allure Report
    :param report_path:
    :param report_html:
    :return:
    """
    # 执行命令 allure generate
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    try:
        subprocess.call(allure_cmd, shell=True)
    except Exception:
        LOGGING.error("The generation of allure report failed. Please check the relevant configuration of the test "
                      "environment")
        raise


def plat():
    """
    Check the current script running platform
    :return:'Linux', 'Windows' or 'Darwin'.
    """
    return platform.system()


def check_port(port):
    """
    Detect whether the port is occupied and clean up
    :param port:System port
    :return:None
    """
    if plat() != 'Windows':
        os.system("lsof -i:%s| grep LISTEN| awk '{print $2}'|xargs kill -9" % port)
    else:
        port_cmd = 'netstat -ano | findstr {}'.format(port)
        r = os.popen(port_cmd)
        if len(r.readlines()) == 0:
            return
        else:
            pid_list = []
            for line in r.readlines():
                line = line.strip()
                pid = re.findall(r'[1-9]\d*', line)
                pid_list.append(pid[-1])
            pid_set = list(set(pid_list))[0]
            pid_cmd = 'taskkill -PID {} -F'.format(pid_set)
            os.system(pid_cmd)


def display():
    """
    Gets the length and width of the current device
    :return:
    """
    width, height = device().get_current_resolution()
    return width, height


def device_udid(state, types: str):
    """
    Perform `adb devices` command and return the list of adb devices
    Perform `utx list` command and return the list of iphone devices
    :param types: mobile platform
    :param state: optional parameter to filter devices in specific state
    :return: list od android devices or ios devices
    """
    device_list = []
    if types.lower() == 'android':
        patten = re.compile(r'^[\w\d.:-]+\t[\w]+$')
        output = ADB().cmd("devices", device=False)
        for line in output.splitlines():
            line = line.strip()
            if not line or not patten.match(line):
                continue
            serialno, cstate = line.split('\t')
            if state and cstate != state:
                continue
            device_list.append(serialno)
    elif types.lower() == 'ios':
        # 获取接入的手机的udid列表
        sub = subprocess.Popen('utx list', shell=True, close_fds=True, stdout=subprocess.PIPE)
        sub.wait()
        udid = sub.stdout.read().decode().splitlines()
        for u in udid:
            device_list.append(u.strip().split(' ')[0])
    return device_list


def ios_device_info():
    """
    Gets device_info of the current device

    :return:
    """
    res = subprocess.run('{} info'.format(decryption(b'dGlkZXZpY2U=')), shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    lines = res.stdout.decode("utf-8", "ignore")
    device_info = [info for info in lines.split('\n') if info]
    _device = {}
    if len(device_info) < 2:
        LOGGING.error(f'Read device info line error. {lines}')
    for info in device_info:
        info_kv = info.split(':')
        if info_kv[0] == 'ProductVersion':
            _device['ProductVersion'] = info_kv[1].strip()
        if info_kv[0] == 'MarketName':
            _device['MarketName'] = info_kv[1].strip()
        if info_kv[0] == 'SerialNumber':
            _device['SerialNumber'] = info_kv[1].strip()
    return _device


def get_report(airtest_report_path):
    """
    Get the latest test report path
    :return: report name and path
    """
    file_lists = os.listdir(airtest_report_path)
    file_lists.sort(key=lambda fn: os.path.getmtime(airtest_report_path + "/" + fn)
    if not os.path.isdir(airtest_report_path + "/" + fn) else 0)
    report = os.path.join(airtest_report_path, file_lists[-1])
    print(file_lists[-1])
    return report


def encryption(value):
    """
    encryption
    https://cdn.jsdelivr.net/gh/openutx/static/
    :param value:
    :return:
    """
    bytes_url = value.encode("utf-8")
    str_url = base64.b64encode(bytes_url)
    return str_url


def decryption(value):
    """
    decryption
    https://cdn.jsdelivr.net/gh/openutx/static/
    :param value:
    :return:
    """
    str_url = base64.b64decode(value).decode("utf-8")
    return str_url


def str_to_bool(value):
    """
    str convert bool
    :param value:
    :return:
    """
    return True if value.lower() == 'true' else False


def selector(status, flag, cases_list):
    """

    :param status:
    :param flag:
    :param cases_list:
    :return:
    """
    cases = []
    if int(status) == 0:
        for suite in cases_list:
            if flag in suite:
                if suite.endswith(".air"):
                    cases.append(suite)
    else:
        for suite in cases_list:
            if suite.endswith(".air"):
                cases.append(suite)

    return cases


def download(file_url, types):
    """

    :param types:
    :param file_url:
    :return:
    """
    if 'http' not in file_url:
        return
    download_url = 'http' + file_url.split('http')[-1]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = requests.get(download_url, stream=True, verify=False)
    total = int(r.headers.get('content-length', 0))
    filename = "{}utx_download_{}.{}".format(file_url.split('http')[0], int(round(time.time() * 1000)), types)

    with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    return filename


class ReadConfig:
    """
    configuration file
    """

    def __init__(self, ini_path):
        self.ini_path = ini_path
        if not os.path.exists(ini_path):
            raise FileNotFoundError("Profile %s does not exist！" % ini_path)
        self.config = configparser.RawConfigParser()  # When there are% symbols, use raw to read
        self.config.read(ini_path, encoding='utf-8')

    def _get(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """

        :param section:
        :param option:
        :param value:
        :return:
        """
        self.config.set(section, option, value)
        with open(self.ini_path, 'w') as f:
            self.config.write(f)

    def getvalue(self, env, name):
        return self._get(env, name)

    def update_value(self, env, name, value):
        return self._set(env, name, value)
