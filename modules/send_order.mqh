//+------------------------------------------------------------------+
//|                                                             NH-1 |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, DavdCsam"
#property link      "https://github.com/davdcsam"

#include <Trade/Trade.mqh>
CTrade trade;

#include "enum.mqh"
#include "timer.mqh"

MqlTradeRequest request_trade = {};

MqlTradeResult result_trade = {};

input group "Trade"

input type_order_trade select_type = BUY;//Select Type

input double lot_size = 1;//Lot Size

input double stop_loss = 10;//Stop Loss

input double take_profit = 10;//Take Profit

input uint magic_number = 666;//Magic Number

input ulong deviation_trade = 10; //Deviation in Point

input turn send_order_show_string = ON;//Show String

double price_close;

double price_ask;

double price_bid;

double tick_size;

string send_order_string;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void build_request_trade()
  {
   request_trade.action = TRADE_ACTION_DEAL;
   request_trade.symbol = _Symbol;
   request_trade.volume = lot_size;
   request_trade.deviation = deviation_trade;
   request_trade.magic = magic_number;
   request_trade.type_filling = (ENUM_ORDER_TYPE_FILLING)SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);

   if(select_type == BUY)
     {
      request_trade.type = ORDER_TYPE_BUY;
      request_trade.price = price_ask;
      request_trade.tp = request_trade.price + take_profit;
      request_trade.sl = request_trade.price - stop_loss;
     }
   else
      if(select_type == SELL)
        {
         request_trade.type = ORDER_TYPE_SELL;
         request_trade.price = price_bid;
         request_trade.tp = request_trade.price - take_profit;
         request_trade.sl = request_trade.price + stop_loss;
        }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void send()
  {
   build_request_trade();

   if(!OrderSend(request_trade, result_trade))
     {
      Alert(EnumToString(select_type), " order was not placed. ", IntegerToString(result_trade.retcode), " ", result_trade.comment);
     }
   else
     {
      Alert(EnumToString(select_type), " order was placed. ", request_trade.symbol, request_trade.order, request_trade.volume, request_trade.tp, request_trade.sl);
     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void send_order_ontick()
  {
   price_ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   price_bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

   tick_size = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);

   price_ask = round(price_ask / tick_size) * tick_size;

   price_bid = round(price_bid / tick_size) * tick_size;

   if(send_order_show_string == ON)
     {
      send_order_string =
         "\n" +
         "      Type                         "  + EnumToString(select_type) +
         "\n" +
         "      Lot Size                      "  + DoubleToString(lot_size, _Digits) +
         "\n"
         "      Stop Loss                   "    + DoubleToString(stop_loss, 0) +
         "\n"
         "      Take Profit                  "   + DoubleToString(take_profit, 0) +
         "\n";
     }
  }
//+------------------------------------------------------------------+
