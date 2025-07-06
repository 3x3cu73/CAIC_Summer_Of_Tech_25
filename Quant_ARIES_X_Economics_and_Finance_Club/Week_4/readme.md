# Financial Machine Learning - Week 4

This week shifts from pure point forecasting to classification and uncertainty modeling, using:

- **Support Vector Machines (SVM)** for directional prediction
- **Bayesian Regression** for confidence-aware price prediction

The goal is to combine classification + probabilistic reasoning to make smarter, risk-aware financial decisions on the stock **AMZN**.

---

## Resources

- **Support Vector Machines**
  - [scikit-learn SVM](https://scikit-learn.org/stable/modules/svm.html)
- **SVM in finance**
  - [SVM in investment strategies](https://wire.insiderfinance.io/support-vector-machines-in-investment-strategies-659c61767201)
- **Bayesian Machine Learning Introduction**
  - [Zilliz Glossary](https://zilliz.com/glossary/bayesian-machine-learning)
- **Bayesian Modelling (Ridge Regression)**
  - [sklearn Bayesian Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.BayesianRidge.html)

---

## Problem Statement

### A. Support Vector Machine (SVM)

**Label Creation**

- Create a binary label:
  - `1` if next day’s return > 0
  - `0` otherwise

**Feature Engineering**

- Use past 5–10 days of:
  - Daily returns
  - Moving averages
  - RSI
  - Bollinger Bands
  - Volume (if available)

**Modeling with SVM**

- Train an SVC (Support Vector Classifier) with RBF kernel
- Tune `C` and `gamma` using cross-validation

**Evaluation**

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- ROC-AUC

---

### B. Probabilistic Forecasting with Bayesian Regression

**Feature Engineering**

- Use the same feature set as above

**Modeling**

- Implement Bayesian Ridge Regression (scikit-learn)

**Forecast**

- Next-day closing price with credible intervals

**Evaluation**

- Mean Absolute Error (MAE)
- Interval coverage probability (how often the true value lies in the 95% credible interval)

---

### C. Trading Strategy (Hybrid Model)

**Entry Rule**

- Buy if:
  - SVM predicts *up*
  - Bayesian mean forecast > current price

**Exit Rule**

- Add stop-loss (e.g., 3%)
- Add take-profit levels

**Backtest**

- Use same logic from Week 2/3
- Report:
  - P&L
  - Sharpe Ratio
  - Drawdown

---

