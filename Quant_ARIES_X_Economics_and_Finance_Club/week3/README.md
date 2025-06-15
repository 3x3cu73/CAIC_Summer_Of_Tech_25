# 📈 Stock Market Prediction: Advanced Modeling, Feature Engineering, and Portfolio Optimization

Welcome to Week 3 of our time-series forecasting journey! This week focuses on bridging machine learning with real-world financial applications. You'll explore advanced modeling techniques, richer feature engineering, risk-aware trading strategies, and portfolio optimization.

---

## 🚀 Objectives

- Apply SARIMAX with seasonality and exogenous variables
- Create ensemble models from previous forecasts
- Explore the Temporal Fusion Transformer (TFT)
- Improve interpretability through feature importance analysis
- Evaluate models using MAE and directional accuracy
- Backtest a trading strategy with risk management
- Optimize a two-stock portfolio using Mean-Variance Optimization (MVO)

---

## 📂 Dataset

- Continue using the *AMZN stock dataset* from Week 2.
- Introduce at least *one exogenous variable* (e.g., S&P 500 index or trading volume).

---

## 🛠 Assignment Tasks

### 1. Advanced Feature Engineering
- Decompose time-series to extract *seasonal components* (e.g., weekly/monthly).
- Apply *log transformations* to stabilize variance.
- Engineer *polynomial features* (e.g., SMA², RSI × Volume).
- Include *exogenous variables* for multivariate modeling.

### 2. Modeling

#### a. SARIMAX
- Incorporate seasonality + exogenous inputs to predict AMZN closing prices.

#### b. Ensemble Model
- Average or weight predictions from Week 2 models (Linear Regression, ARIMA, Random Forest) using their MAE scores.

#### c. Temporal Fusion Transformer (Optional)
- Explore the TFT through provided readings.
- Discuss its potential applications in time-series forecasting.

### 3. Model Interpretability
- Visualize feature importance from the *Random Forest* model.
- Analyze the SARIMAX model components and impact of exogenous variables.

### 4. Evaluation
- Use *Mean Absolute Error (MAE)* and *directional accuracy* to compare:
  - SARIMAX
  - Ensemble Model
  - Week 2 Models

---

## 📉 Backtesting & Risk Management

- Use the Week 2 strategy:  
  *Buy* if predicted price > current price, *Sell* otherwise.
  
- Add:
  - 📉 *Stop-loss* (e.g., exit if price drops 5% from entry)
  - 📊 *Sharpe Ratio* for risk-adjusted return evaluation

---

## 💼 Portfolio Optimization

- Include *AAPL* stock alongside *AMZN*.
- Use historical returns to:
  - Calculate the *expected returns* and *covariance matrix*
  - Perform *Mean-Variance Optimization* (MVO)
  - Maximize the *Sharpe Ratio* to find optimal asset weights

---

## 📚 Resources

### 📘 SARIMAX
- [Statsmodels SARIMAX Example](https://www.statsmodels.org/stable/examples/notebooks/generated/statespace_sarimax_stata.html)  
- [Machine Learning Mastery - SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/)

### 🧠 Ensemble Methods
- [Ensemble Techniques - Machine Learning Mastery](https://machinelearningmastery.com/ensemble-machine-learning-with-python-7-day-mini-course/)  
- [Guide to Ensemble Models – Analytics Vidhya](https://www.analyticsvidhya.com/blog/2018/06/comprehensive-guide-for-ensemble-models/)

### 🏗 Feature Engineering
- [6 Feature Engineering Techniques for Time Series](https://www.analyticsvidhya.com/blog/2019/12/6-powerful-feature-engineering-techniques-time-series/)  
- [Decomposing Time Series](https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/)

### 🔮 Temporal Fusion Transformer (TFT)
- [TFT Research Paper](https://arxiv.org/abs/1912.09363)  
- [TFT Primer – Towards Data Science](https://towardsdatascience.com/temporal-fusion-transformer-a-primer-on-deep-forecasting-in-python-4eb37f3f3594/)

### 📊 Portfolio Optimization
- [Modern Portfolio Theory – Investopedia](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)  
- [Portfolio Optimization in Python – Analytics Vidhya](https://www.analyticsvidhya.com/blog/2021/04/portfolio-optimization-using-mpt-in-python/)

### ⚠ Risk Management
- [Sharpe Ratio – Investopedia](https://www.investopedia.com/terms/s/sharperatio.asp)  
- [Stop-Loss Orders – Investopedia](https://www.investopedia.com/articles/stocks/09/use-stop-loss.asp)

---

Happy Forecasting 📈
