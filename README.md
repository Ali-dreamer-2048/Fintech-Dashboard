# Fintech Dashboard

一個互動式 Fintech 儀表板，專為 CityU Year 1 金融科技課程（JS1221）設計。  
包含兩個強大功能：
- 多檔股票篩選器：計算年化報酬、波動率與 Sharpe Ratio，並排序顯示
- 即時外匯匯率查詢器：支援 USD/HKD、CNY/HKD、EUR/HKD、JPY/HKD 等常見匯率對，並顯示歷史走勢圖

使用 Streamlit 打造，簡單、直觀、適合展示在 GitHub 作為 portfolio。

## 功能亮點
- 股票篩選：輸入多個股票代碼（例如 0700.HK, AAPL, TSLA），自動計算年化報酬、波動率、Sharpe Ratio
- 外匯查詢：選擇匯率對 + 天數，即時顯示最新匯率與互動走勢圖（Plotly）
- 錯誤處理：網路或代碼無效時顯示友好提示
- 響應式設計：適合電腦與平板瀏覽

## 安裝與執行步驟

1. 進入專案資料夾  
   ```bash
   cd "/Users/ali/PycharmProjects/DEV/fintech-dashboard"

安裝所有依賴套件Bashpip install -r requirements.txt
啟動應用程式Bashstreamlit run app.py瀏覽器會自動打開：http://localhost:8501
（如果沒自動開啟，手動輸入上面網址即可）