//+------------------------------------------------------------------+
//|                                              Transaction Handler |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "inputs.mqh"

double price_close;

double price_ask;

double price_bid;

double tick_size;

string send_order_string;
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void update_send_order_data()
  {
   price_ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   price_bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

   tick_size = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);

   price_ask = round(price_ask / tick_size) * tick_size;

   price_bid = round(price_bid / tick_size) * tick_size;

   if(send_order_show_string == ON)
     {
      send_order_string = StringFormat("\n      Type %s\n      Lot Size %s\n      Stop Loss %d\n      Take Profit %d\n", EnumToString(select_type), DoubleToString(lot_size, _Digits), stop_loss, take_profit);
     }
  }
//+------------------------------------------------------------------+
