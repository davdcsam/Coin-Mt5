//|                                                    Build Request |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "..\\enum.mqh"

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void build_request(
   MqlTradeRequest& request,
   float& lot_size,
   type_order_trade& order_type,
   uint& take_profit,
   uint& stop_loss,
   int& deviation_trade,
   int& type_filling,
   double& price_ask,
   double& price_bid
)
  {
   request.action = TRADE_ACTION_DEAL;
   request.symbol = _Symbol;
   request.volume = lot_size;
   request.deviation = deviation_trade;
   request.magic = 0;
   request.type_filling = (ENUM_ORDER_TYPE_FILLING)type_filling;

   if(order_type == BUY)
     {
      request.type = ORDER_TYPE_BUY;
      request.price = price_ask;
      request.tp = NormalizeDouble(request.price + take_profit * _Point, _Digits);
      request.sl = NormalizeDouble(request.price - stop_loss * _Point, _Digits);
     }
   else
      if(order_type == SELL)
        {
         request.type = ORDER_TYPE_SELL;
         request.price = price_bid;
         request.tp = NormalizeDouble(request.price - take_profit * _Point, _Digits);
         request.sl = NormalizeDouble(request.price + stop_loss * _Point, _Digits);
        }
  }
//+------------------------------------------------------------------+
