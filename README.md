# SMA_2026S

## 讀書會觀摩網頁
https://text-analytics-and-retrieval.github.io/SMA_2025S/

## 每週資料夾內容
我們會根據課程內容提供對應的 Python 程式碼給同學們做實作練習，每一週的內容會以分開的資料夾上傳，資料夾包含執行當週程式碼所需的全部資源。   
以第三週為例，說明資料夾中可能會包含哪些內容：

- ```week3```   

    - ```dict 資料夾```：資料清理或分析會使用到的字典   

    - ```pic 資料夾```：Jupyter Notebook 中的範例圖片   
    
    - ```raw_data 資料夾```：尚未清理或欲分析的資料集   

    - ```week3_nlp_en.ipynb```：包含主要程式碼的 Jupyter Notebook 檔（英文文本）   

    - ```week3_nlp_zh.ipynb```：包含主要程式碼的 Jupyter Notebook 檔（中文文本）
    

## 初始環境設置
```requirements.txt``` 檔案中列出了大部分本堂課會使用到的套件以及建議安裝的版本，在第一次建置 Python 執行環境時，同學們可以透過以下方法安裝套件。   

### 本地端運行
1. 創建新的虛擬環境（以 conda 為例），並切換至該環境，我們建議使用 python 3.11.0 版本

    ```bash
    conda create --name 環境名稱 python=3.11.0
    conda activate 環境名稱

2. 在欲安裝套件的環境中打開 Terminal，確定當前所在資料夾中包含 requirements.txt，可以透過以下指令切換資料夾   

    ```bash
    cd 目標資料夾路徑

3. 接著在 Terminal 輸入以下指令，安裝 requirements.txt 中的所有套件   

    ```bash
    pip install -r requirements.txt

4. 安裝完後可以使用以下指令列出當前環境中所有套件與版本，確定套件是否成功安裝與版本是否正確

    ```bash
    pip list

### 在 Google Colab 運行
1. 在 Jupyter Notebook 中確保當前位置為包含 requirements.txt 的資料夾，在儲存格中執行以下 Python 程式碼

    ```python
    import os
    path = "目標資料夾路徑"
    os.chdir(path)
    print(os.getcwd())

2. 接著在儲存格中執行以下指令，安裝 requirements.txt 中的所有套件。請注意，因為是在儲存格中執行，指令的最前面要記得加上驚嘆號！ 

    ```bash
    !pip install -r requirements.txt

3. 安裝完後可以在儲存格中執行以下指令列出當前環境中所有套件與版本，確定套件是否成功安裝與版本是否正確

    ```bash
    !pip list



