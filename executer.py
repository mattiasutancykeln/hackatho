import hackathon_linc as lh
import pandas as pd
import time
from threading import Thread

class Executor():

    def __init__(self):
        # Connect
        api_key = "cad17e97-11c1-414a-b38d-11cd1ca657f1"
        lh.init(api_key)

        # Set portfolio state
        self.portfolio = {ticker:0 for ticker in lh.get_all_tickers()}
        rec_port = lh.get_portfolio()
        for ticker in rec_port:
            self.portfolio[ticker] = rec_port[ticker]
        self.target_pos = self.portfolio
    
    def get_cprices(self):
        return pd.DataFrame(lh.get_current_price()['data'])

    def get_portfolio(self):
        return self.portfolio
    
    def get_balance(self):
        return lh.get_balance()

    def set_target_pos(self,pos):
        self.target_pos = pos

    def execute_to_position(self):
        pos = dict(self.target_pos)
        for ticker in pos:
            delta = pos[ticker] - self.portfolio[ticker]
            if delta > 0:
                ord_result = lh.buy(ticker, delta,None, 1)
            elif delta < 0:
                ord_result = lh.sell(ticker, -delta)
            else:
                continue
            print(ord_result)
            if ord_result == {'message': 'The rate limit has been reached'}:
                print("slow API")
            elif ord_result["order_status"] == "pending":
                print(ticker + " got pending")
            elif ord_result["order_status"] == "completed":
                self.portfolio[ticker] = pos[ticker]
                continue
            else:
                raise("Shit hit the Fan, with the order sport!!")
            

    def execute_to_position_threaded(self):
        thread = Thread(target=self.execute_to_position)
        thread.start()