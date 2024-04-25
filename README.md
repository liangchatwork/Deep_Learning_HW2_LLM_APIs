# FUNDAMENTALS OF DEEP LEARNING NETWORKS Homework2 - LLM APIs
本次作業要建立兩大功能模組，其一是**ChatBot聊天機器人模組**，其二是將建立好的ChatBot掛載到**Django架構的APIs**上在本地端執行操作。

* ##  LLM 模型
  這邊製作語言模型的方法，是事先建立一個聊天資料集intent.json，將各種意義的語句集合各賦予一個`tag`作為label，`pattern`則是作為各種語句集合的input，在這邊我們會將語句先進行**tokenize** 並且經過**steamming**、**lemmatization** ，最後做**bag of words** 讓電腦可以針對不同詞語去做意義分類，使它了解各種字詞的意思。接著將這些語詞集合包裝成training data。
  ### ANN model
  這邊我們用最基本的**Artificial Neural Network**去訓練資料集，ANN的程式碼架構如下 :
  
  ```python
  class ANN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out
  ```

  訓練完之後我將模型儲存成一個`new_data.path`的檔案供後續API進行呼叫。

  

* ##  文字回應 API 伺服器
  這邊使用的是Django架構，要使用Django架購必須經過以下步驟 :

  ### 一、安裝Django
  ```bash
  pip install django
  pip install djangorestframework
  ```
  ### 二、創建新專案Project
  ```bash
  django-admin startproject <project_name>
  ```
  ### 三、創建API資料夾
  ```bash
  cd <project_name>
  django-admin startapp <api_name>
  ```
  ### 四、調整URL
  這邊我們要調整外部project的`<project_name>/url.py`也要調整內部的`<api_name>/url.py`。

  首先外部的`<project_name>/url.py`程式碼如下，由於我的<api_name>=LLM :
  ```python
  from django.contrib import admin
  from django.urls import path, include 
  
  urlpatterns = [
      path('LLM/', include('LLM.urls')),
      path('admin/', admin.site.urls),
  ]
  ```

  接著內部的`<api_name>/url.py`程式碼如下，裡面的`chatbot`是我們要呼叫的API功能，這個部分是寫在`view.py`裡面 :
  ```python
  from django.contrib import admin
  from django.urls import path
  from . import views
  
  urlpatterns = [
      path('', views.chatbot, name='chatbot'),
  ]
  ```
  '''

  ### 五、調整settings
  這個部份是要調整project的setting部分，讓我們可以使用後面建立的API，方法是調整`<project_name>/settings.py`程式碼裡面`INSTALLED_APPS`的部分 :
  ```python
  # Application definition

  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'rest_framework',
      'corsheaders',
      'LLM'  # Add the API name 
  ]
  ```
  
  ### 六、自定義views
  這邊就是整個API的核心，這邊你自定義的函式名稱要對應到前面Step.4 URL設定部分裡面的`urlpatterns`，設定好之後你可以在裡面寫下聊天機器人  的功能，程式碼如下 :
  ```python
  from django.http import JsonResponse
  from django.views.decorators.csrf import csrf_exempt
  import json
  import random
  import torch
  import LLM.models
  import LLM.utils

  @csrf_exempt
  def chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            if message:
                
                # 在這裡可以對訊息進行處理，然後給予回覆
                chatbot = Chatbot()
                response_message = chatbot.chat(message)
                print(response_message)

                # response_message = "Chatbot > " + message
                return JsonResponse({'status': True, 'data': response_message})
            else:
                return JsonResponse({'status': False, 'message': '參數錯誤：請提供訊息'})
        except Exception as e:
            return JsonResponse({'status': False, 'failed': str(e)})
    else:
        return JsonResponse({'status': False, 'message': '只支援 POST 請求'})
  ```
  完整程式碼請見Repository。

  ### 七、啟用API
  最後要讓API啟用就必須開port給API，這邊的指令我們必須回到外層`<project_name>`的資料夾。
  ```
  python manage.py runserver
  ```
  上面指令啟動後如此一來，預設port number為`8000`，若要自行指定port可以用下面指令 :
  ```
  python manage.py runserver 0.0.0.0:<port_number>
  ```
  所以我自己再開發是搭被screen指令做使用，讓API在背景執行，我則是使用自製的test.py檔來測試聊天機器人。
  以上就是開發的一些小撇步，接著下面是打包成docker之後的使用說明，請將Repository載下來之後依照下面步驟使用 :

* ##  使用說明
  ### Step.1 啟動Docker
  ```
  ./start.sh
  ```
  ### Step.2 用screen建立背景
  ```
  screen -S API
  ```
  ### Step.3 至screen內部執行API
  ```
  python3 manage.py runserver 0.0.0.0:8080
  ```
  接著請用Ctrl+A+D跳出screen再接著到Step.4。
  ### Step.4 使用機器人
  ```
  python3 test.py
  ```
  ### Step.5 輸入訊息並接收回覆，輸入`exit`則結束操作
  ```
  You > Hi
  {'status': True, 'data': 'Good to see you again!'}
  You > Hello
  {'status': True, 'data': 'Hello!'}
  You > Goodbye!
  {'status': True, 'data': 'Sad to see you go :('}
  You > exit
  ```
  本作業只限本地端操作，請見諒。
