//+------------------------------------------------------------------+
//|                                                             NH-1 |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, DavdCsam"
#property link      "https://github.com/davdcsam"

#include "enum.mqh"
#include "timer.mqh"

MqlTradeRequest trade_request;

MqlTradeResult trade_result;

MqlTradeCheckResult check_result;

input group "Trade"

input type_order_trade select_type = BUY;//Select Type

input double lot_size = 1;//Lot Size

input uint stop_loss = 20000;//Stop Loss

input uint take_profit = 20000;//Take Profit

input uint deviation_trade = 1000; //Deviation in Point

input turn send_order_show_string = ON;//Show String

double price_close;

double price_ask;

double price_bid;

double tick_size;

string send_order_string;

ENUM_ORDER_TYPE_FILLING correct_type_filling;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void checker()
  {
   int list_order_type_filling[] = {ORDER_FILLING_FOK, ORDER_FILLING_IOC, ORDER_FILLING_RETURN, ORDER_FILLING_BOC};

   for(int i=0; i<ArraySize(list_order_type_filling); i++)
     {
      build_request(list_order_type_filling[i]);

      if(check_position(trade_request, check_result, correct_type_filling))
        {
         PrintFormat("Filling mode in %s is %s", _Symbol, EnumToString(correct_type_filling));
         break;
        }
     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool check_position(MqlTradeRequest& request, MqlTradeCheckResult& result, ENUM_ORDER_TYPE_FILLING& filling_mode_to_set)
  {
   Print(DoubleToString(request.price), DoubleToString(request.sl), DoubleToString(request.tp));

   if(!OrderCheck(request, result))
     {
      PrintFormat("OrderCheck failed, return code %d: %s", result.retcode, result.comment);
      return(false);
     }

   switch(result.retcode)
     {
      case TRADE_RETCODE_DONE:
         filling_mode_to_set = request.type_filling;
         return(true);
         break;
      case 0:
         filling_mode_to_set = request.type_filling;
         return(true);
         break;
      default:
         return(false);
         break;
     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void build_request(int type_filling)
  {
   trade_request.action = TRADE_ACTION_DEAL;
   trade_request.symbol = _Symbol;
   trade_request.volume = lot_size;
   trade_request.deviation = deviation_trade;
   trade_request.magic = 0;
   trade_request.type_filling = (ENUM_ORDER_TYPE_FILLING)type_filling;

   if(select_type == BUY)
     {
      trade_request.type = ORDER_TYPE_BUY;
      trade_request.price = price_ask;
      trade_request.tp = NormalizeDouble(trade_request.price + take_profit * _Point, _Digits);
      trade_request.sl = NormalizeDouble(trade_request.price - stop_loss * _Point, _Digits);
     }
   else
      if(select_type == SELL)
        {
         trade_request.type = ORDER_TYPE_SELL;
         trade_request.price = price_bid;
         trade_request.tp = NormalizeDouble(trade_request.price - take_profit * _Point, _Digits);
         trade_request.sl = NormalizeDouble(trade_request.price + stop_loss * _Point, _Digits);
        }
  }

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
//|                                                                  |
//+------------------------------------------------------------------+
/*
void send()
  {
   build_request();

   if(!OrderSend(trade_request, trade_result))
     {
      Alert(EnumToString(select_type), " order was not placed. ", IntegerToString(trade_result.retcode), " ", trade_result.comment);
     }
   else
     {
      Alert(EnumToString(select_type), " order was placed. ", trade_request.symbol, trade_request.order, trade_request.volume, trade_request.tp, trade_request.sl);
     }
  }
*/
//+------------------------------------------------------------------+
