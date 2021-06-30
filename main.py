import os
from utils.common_utils import create_testcase

if __name__ == '__main__':
    if not os.path.exists("./testcase"):
        os.mkdir("./testcase")
    with open('./testcase/__init__.py' ,'w') as f:
        print("")
    f.close()
    create_testcase()
    result = os.popen("pytest -v -s --alluredir=report/xml ./testcase")
    print(result.read())
    report = os.popen("allure generate report/xml -o report/html --clean")
    os.system("allure open ./report")
