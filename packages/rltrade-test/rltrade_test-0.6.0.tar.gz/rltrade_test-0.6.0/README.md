# rl-trade

### Python 3.7.11 or greater is required
    conda create -n env_name python=3.7
    conda activate env_name

### installation.
    pip install rltrade-test

### Login into your Interactive Borker app (live or paper)
    1. For training the model run train.py from examples folder.
    2. For trading use trade.py from examples folder.
 
#### Import
```python
from rltrade import config
from rltrade.data import IBKRDownloader
from rltrade.backtests import get_metrics
from rltrade.models import SmartPortfolioAgent
```
#### Parameters
```python
demo = True #for live trading set demo to False
train_period = ('2012-01-01','2020-08-01') #for training the model
test_period = ('2020-08-02','2021-12-29') #for backtesting

ticker_list = ['pall', 'rio', 'spy', 'tlt', 'jbss', 'aapl'] # ticker list as per ibkr
sec_types = ['STK'] * len(ticker_list) #sec type as per ibkr
exchanges = ['SMART'] * len(ticker_list) #exchange as per ibkr

tech_indicators = config.STOCK_INDICATORS_LIST #these are indicators from stockstats library
additional_indicators = config.ADDITIONAL_STOCK_INDICATORS #these are indicators created by rltrade

env_kwargs = {
    "initial_amount": 50_828, #this is total amount spend
    "ticker_col_name":"tic",
    "filter_threshold":0.25, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
    "target_metrics":['asset','sortino','calamar','skew','kurtosis'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "tech_indicator_list":tech_indicators + additional_indicators, 
    "reward_scaling": 1}
    
PPO_PARAMS = {'ent_coef':0.005,
            'learning_rate':0.01,
            'batch_size':252}
```
#### Download Data and set up agent

```python
df = IBKRDownloader(start_date = train_period[0], #first date
                    end_date = test_period[1], #last date
                    ticker_list = ticker_list,
                    sec_types=sec_types,
                    exchanges=exchanges,
                    demo=demo,
                    ).fetch_data() #require subscription

agent = SmartPortfolioAgent("ppo",
                    df=df,
                    ticker_list=ticker_list,
                    sec_types=sec_types,
                    exchanges=exchanges,
                    ticker_col_name="tic",
                    tech_indicators=tech_indicators,
                    additional_indicators=additional_indicators,
                    train_period=train_period,
                    test_period=test_period,
                    env_kwargs=env_kwargs,
                    model_kwargs=PPO_PARAMS,
                    tb_log_name='ppo',
                    demo=demo,
                    epochs=9)
```
#### Training model and trading

```python
# agent.train_model()
agent.train_model_filter() #training model on trading period
agent.save_model(path) #save the model for trading

df_daily_return,df_actions = agent.make_prediction() #testing model on testing period
get_metrics(path)
```

