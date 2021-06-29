# -*- coding: utf-8 -*-
import requests
import json
import os


def config_read():
    with open('./config/config.json', 'r') as f:
        load_config = json.load(f)
        baseurl = load_config["baseurl"]
    f.close()
    return baseurl


burl= config_read()


"""
GetToken方法需要根据当前项目适配
如果无法适配，可尝试手动预置token
"""


# def get_token():
#     api = "login"
#     para = {"name": username, "password": password}
#     res = requests.post(url=burl+api, json=para)
#     return res.json()["token"]


def r_get(api, param, header):
    res = requests.get(url=burl+api, params=param, headers=header)
    return res.status_code, res.json()


def r_post(api, param, header):
    res = requests.post(url=burl+api, json=param, headers=header)
    return res.status_code, res.json()


def testfile_read(file_dir):
    file_list = os.listdir(file_dir)
    return file_list


def dynamic_make_testcase(api, data, method, expect, headers):
    f_name = "test_" + str(api).replace('/', '_') + ".py"
    testcasenum = len(data)
    with open('./testcase/'+f_name, 'w') as f:
        print("import pytest", file=f)
        print("import json", file=f)
        print("from utils.common_utils import r_get,r_post", file=f)
        for i in range(0, testcasenum):
            print("def test_" + str(api).replace('/', '_') + "_" + str(i+1) + "():", file=f)
            print("  api = \"" + api + "\"", file=f)
            print("  params = " + str(data[i]), file=f)
            print("  headers = " + str(headers), file=f)
            print("  code = r_" + str(method) + "(api, params, headers)[0]", file=f)
            print("  print(\"param is: \" + str(params))", file=f)
            print("  assert code ==" + str(expect[i]) + ", \"Test Failed, please check, status code is %s , param is %s\" % (str(code),str(params))", file=f)
            print("\n", file=f)


def find_replace(ph,rd):
    if isinstance(ph,dict):
        for i in ph.keys():
            for j in rd:
                if ph[i] == ("$~"+j):
                    ph[i] = rd[j]
        return ph
    elif isinstance(ph,list):
        le = len(ph)
        for i in range(0,le):
            for j in ph[i]:
                for k in rd:
                    if ph[i][j] == ("$~"+k):
                        ph[i][j] = rd[k]
        return ph


def create_testcase():
    lis = testfile_read('./testdata')
    for i in lis:
        with open("./testdata/"+i, 'r') as f:
            load_data = json.load(f)
            le = len(load_data)
            for i in range(1, le):
                if "step" + str(i) in load_data:
                    apiname = load_data["step" + str(i)]["apiname"]
                    method = load_data["step" + str(i)]["method"]
                    headers = load_data["step" + str(i)]["headers"]
                    testdata = load_data["step" + str(i)]["testdata"]
                    #replace_data = load_data["step" + str(i)]["return_data"]
                    if method == "get":
                        return_d = r_get(apiname, testdata, headers)
                    elif method == "post":
                        return_d = r_post(apiname, testdata, headers)
            apiname = load_data["case"]["apiname"]
            headers = load_data["case"]["headers"]
            headers = find_replace(headers, return_d[1])
            testdata = load_data["case"]["testdata"]
            testdata = find_replace(testdata, return_d[1])
            method = load_data["case"]["method"]
            expect_result = load_data["case"]["expect_code"]
        f.close()
        dynamic_make_testcase(apiname, testdata, method ,expect_result, headers)


