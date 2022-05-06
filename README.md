# Cryptocurrencies Investment Helper

This project is a MVP tool to allow's someone interested in Cryptocurrencies, to know more about them as well as an Investment Helper tool.

![Image](https://wortev.capital/wp-content/uploads/2021/07/principales-paises-que-mas-invierten-en-criptomonedas.jpg)

---

## **Description**
The app contains 2 types of user, the admin one and the final user one.

- The **administrator** role  will be in charge of updating the information for the user, as well as carry out the 'Long-Term' Stock Prediction once a week.
- The **final user** role will be able to chose, if he/she wants to get a Cryptocurrency general Analysis, a Prediction for short and long-term, and/or Daily information for Investment proposals.


## **Getting Started**
### :baby: **Status**
This is the final project of Ironhack Data Analytics Bootcamp. The main goal is to build a complete pipeline app.

### :computer: **Skills**
During the project, next skills have been worked:
 - **Python**: All scripts have been developed in Python, from data extraction to data visualization
 - **SQL**: A databse have been created to store the cryptos daily main values. Then they are read by the main app.
 - **Web Scrapping**: To get daily cryptos values, daily news, etc.
 - **Data Cleanning**: To clean and prepare all data before preparing them for the user
 - **Statistic**: To understand the main cryptocurrencies in the market, the prices evolution, the market volatility, etc.
 - **Supervised Machine Learning**: To carrry out the Long-Term Stock Price Prediction
 - **Unsupervised Machine Learning**: To carrry out the Short-Term Stock Price Prediction
 - **Sentiment-Analysis**: To identify the positive, negative and neutral daily news
 - **Mail Functionality**: To send an email in case of Buy/Sell market signals
 - **Visualization**: To show in an easy-way the main KPIs and prices evolution, predictions and news to the user

### :page_facing_up: **Data Avilability**
 - Daily and historical market values are obtained from [yahoo finance](https://finance.yahoo.com/).
 - Daily news are obtained from [Crypto News API](https://cryptonews-api.com/)

### :books: **Libraries**

- This repository is tested on **Python 3.7+**.
- Create a virtual environment with the version of Python you're going to use and activate it.
- Check requirements.txt file to install the tested versions

- Install [pandas](https://pandas.pydata.org/docs/user_guide/index.html) library. Copy and paste next command in your master branch:
    ```
    pip install pandas
    ```
- Install [numpy](https://numpy.org/) library. Copy and paste next command in your master branch:
    ```
    pip install numpy
    ```
- Install [streamlit](https://streamlit.io/) library. Copy and paste next command in your master branch:
    ```
    pip install streamlit
    ```
- Install [yfinance](https://pypi.org/project/yfinance/) library. Copy and paste next command in your master branch:
    ```
    pip install yfinance
    ```
- Install [plotly](https://plotly.com/python/getting-started/) library. Copy and paste next command in your master branch:
    ```
    pip install plotly==5.7.0
    ```
- Install [matplotlib](https://matplotlib.org/stable/index.html) library. Copy and paste next command in your master branch:
    ```
    pip install matplotlib
    ```
- Install [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) library. Copy and paste next command in your master branch:
    ```
    pip install beautifulsoup4
    ```
- Install [requests](https://docs.python-requests.org/en/latest/) library. Copy and paste next command in your master branch:
    ```
    python -m pip install requests
    ```
- Install [pystan](https://pystan.readthedocs.io/en/latest/) library. Copy and paste next command in your master branch:
    ```
    python -m pip install pystan
    ```
- Install [prophet](https://facebook.github.io/prophet/) library. Copy and paste next command in your master branch:
    ```
    pip install prophet
    ```
- Install [dateutil](https://pypi.org/project/python-dateutil/1.4/) library. Copy and paste next command in your master branch:
    ```
    pip install python-dateutil==2.8.2
    ```
- Install [keras](https://keras.io/) library. Copy and paste next command in your master branch:
    ```
    pip install tensorflow==1.8
    pip install keras
    ```
- Install [joblib](https://pypi.org/project/joblib/) library. Copy and paste next command in your master branch:
    ```
    pip install joblib
    ```

- Install [dotenv](https://pypi.org/project/python-dotenv/) library. Copy and paste next command in your master branch:
    ```
    pip install python-dotenv
    ```
- Install [sqlite3](https://docs.python.org/es/3/library/sqlite3.html) library. Copy and paste next command in your master branch:
    ```
    pip install pretty-html-table
    ```

- Be sure next Python modules are installed: [sys](https://docs.python.org/3/library/sys.html) , [os](https://docs.python.org/3/library/os.html), [datetime](https://docs.python.org/3/library/datetime.html), [sqlite](https://docs.python.org/es/3/library/sqlite3.html).


<p align="center"><img src="https://c.tenor.com/pPKOYQpTO8AAAAAd/monkey-developer.gif"></p>

&nbsp;

---

# :lock: **ADMIN Script**


The admin role will be in charge of execute the main_admin.py script, which will carry out next functions:
- Updates the historical stock prices database 
- Calculates the Long-Term predictions
- Reports errors in case they exist.

# :point_right: **USER Script**
The user app is divided in 3 sections, in order to help the user to understand, predict and help in the Cryptocurrencies trade.

## :chart_with_upwards_trend: **Cryptocurrencies Analysis**
The main function of this first part of the main app (script) is understand the top 15 cryptocurrencies in the market.
Selecting which crypto do the user want to visualize, as well as the data period he/she wish to consult, the user will be able to see:
- Evolution of stock prices in that period (Close, Open, Low, High or Market Volume)
- Candlestick chart with the market values in that period.
- Daily Stock Prices Change(%).
- Main KPIs with the highest and lowest values in that period.


https://user-images.githubusercontent.com/83816010/167087677-1b10a75b-26c8-4410-844d-e7fe0ad23737.mov


https://user-images.githubusercontent.com/83816010/167087792-d71b8d6a-b8cb-45ad-bf53-8b2cf2ee5708.mov








&nbsp;

---

### :file_folder: **Folder structure**
```
└── crypto_investment_helper
    ├── __trash__
    │ 
    ├── .git
    │ 
    ├── .gitignore
    │     
    ├── LICENSE
    │     
    ├── README.md
    │ 
    ├── main_user.py
    │ 
    ├── main_admin.py
    │ 
    ├── EDAs
    │ 
    ├── notebooks_not_updated
    │
    ├── scripts
    │   ├── crypto_tracker.py
    │   ├── crypto_predictor.py
    │   └── buy_sell_helper.py
    │
    └── data
        ├── models
        ├── predictions
        ├── scalers_neural_network
        ├── crypto_descriptions.csv
        └── historical_prices.db
```

> Do not forget to include `__trash__` and `.env` in `.gitignore` 

&nbsp;
### :shit: **ToDo**
:black_square_button: Add some other Cryptocurrencies.
:black_square_button: Add news sentiment analysis to price predictions.
:black_square_button: Add more email functionalities and alerts.
:black_square_button: Automatize buy and sell actions.

---
