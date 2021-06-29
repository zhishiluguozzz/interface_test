# interface_test
* 环境前置：
  >pip3 install requests  
  >pip3 install pytest  
  >pip3 install pytest-allure  
  >环境需配置allure

* config目录：
  >config.json中baseurl填写为待测根url
  
* testdata目录：
  >创建xxx.json文件，具体格式可参考test.json
  
  > * 1、json文件中以step+数字形式预置前置动作  
  ```
  "step1": {  
    "apiname": "login",  //前置接口名
    "method": "post",    //前置接口方法
    "headers": {         //前置接口header
      "Accept": "application/json",  
      "Content-Type": "application/json"  
    },  
    "testdata": {        //前置接口所需参数
      "name": "",  
      "password": ""  
    },  
    "return_data": ["token","testdata2"]  //待传递参数名
    }
  ```
  
  > * 2、json文件中以case预置测试用例
  ```
   "case": {
    "apiname": "test",  //待测接口名
    "method": "get",    //待测接口方法
    "headers": {        //待测接口header
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-user-token": "$~token"  //变量名需与接口返回key一致，并以$~起始
    },
    "testdata": [       //支持同时键入多组测试数据
      {"currentPage": 1, "pageSize": 10},
      {"currentPage": 1.3, "pageSize": 10},
      {"currentPage": 1, "pageSize": 10.5},
      {"currentPage": null, "pageSize": 10},
      {"currentPage": 1, "pageSize": null},
      {"currentPage": "zzz", "pageSize": 10},
      {"currentPage": 1, "pageSize": "zzz"}
    ],
    "expect_code": [    //预期返回码与测试数据结果应一一对应
      "200",
      "400",
      "400",
      "400",
      "400",
      "400",
      "400"
    ]
  }
  }
  ```
  
* 测试执行
  >配置文件、接口信息及测试数据写入完成后，在根目录下执行python3 main.py即可
  
  >测试结束后自动弹出allure报告页面，点击html可查看细节
  > 
* 过程文件生成
  >过程文件包含：report目录，testcase目录
  >>report目录：allure测试报告相关文件
  > 
  >>testcase目录：内容为动态生成的pytest测试用例