//+------------------------------------------------------------------+
//|                                                      Calc Profit |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+

double calculated_profit;
double calculated_loss;


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void calculated_profits(double lot_size, ENUM_ORDER_TYPE order_type, string symbol, double stop_loss, double take_profit)
  {
   double open_price= (order_type == ORDER_TYPE_BUY) ? SymbolInfoDouble(symbol, SYMBOL_ASK) : SymbolInfoDouble(symbol, SYMBOL_BID);

   if(!OrderCalcProfit(order_type, symbol, lot_size, open_price, take_profit, calculated_profit))
     {
      Print("No posible calc profit");
     }
   if(!OrderCalcProfit(order_type, symbol, lot_size, open_price, stop_loss, calculated_loss))
     {
      Print("No posible calc loss");
     }
  }
//+------------------------------------------------------------------+
