# FUNDAMENTALS OF DEEP LEARNING NETWORKS Homework2 - LLM APIs
本次作業要建立兩大功能模組，其一是**ChatBot聊天機器人模組**，其二是將建立好的ChatBot掛載到**Django架構的APIs**上在本地端執行操作。

* ##  LLM 模型
  這邊製作語言模型的方法，是事先建立一個聊天資料集intent.json，將各種意義的語句集合各賦予一個`tag`作為label，`pattern`則是作為各種語句集合的input，在這邊我們會將語句先進行**tokenize** 並且經過**steamming**、**lemmatization** ，最後做**bag of words** 讓電腦可以針對不同詞語去做意義分類，使它了解各種字詞的意思。接著將這些語詞集合包裝成training data。
  #### ANN model
    這邊我們用最基本的**Artificial Neural Network**去訓練資料集，
