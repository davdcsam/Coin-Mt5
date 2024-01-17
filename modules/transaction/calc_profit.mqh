//+------------------------------------------------------------------+
//|                                                      Calc Profit |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+

string calc_profit_comment;

double calculated_profit;

double calculated_loss;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void calculated_profits(double lot_size, ENUM_ORDER_TYPE order_type, string symbol, double stop_loss, double take_profit)
  {
   double open_price= (order_type == ORDER_TYPE_BUY) ? SymbolInfoDouble(symbol, SYMBOL_ASK) : SymbolInfoDouble(symbol, SYMBOL_BID);

   bool calculated_profit_return = OrderCalcProfit(order_type, symbol, lot_size, open_price, take_profit, calculated_profit);

   bool calculated_loss_return = OrderCalcProfit(order_type, symbol, lot_size, open_price, stop_loss, calculated_loss);

   if(calculated_profit_return && calculated_loss_return)
     {
      calc_profit_comment = StringFormat(
                               "Estimated benefits. Profit %s %.2f. Loss %s %.2f",
                               SymbolInfoString(_Symbol, SYMBOL_CURRENCY_PROFIT),
                               calculated_profit,
                               SymbolInfoString(_Symbol, SYMBOL_CURRENCY_PROFIT),
                               calculated_loss
                            );

     }
   else
     {
      Print("No posible calc profits");
      calc_profit_comment = "";
     }
  }
//+------------------------------------------------------------------+
