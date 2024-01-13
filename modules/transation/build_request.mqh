//|                                                    Build Request |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "..\\enum.mqh"

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void build_request(
   MqlTradeRequest& trade_request,
   float lot_size,
   type_order_trade order_type,
   uint take_profit,
   uint stop_loss,
   int deviation_trade,
   int type_filling,
   double price_ask,
   double price_bid
)
  {
   trade_request.action = TRADE_ACTION_DEAL;
   trade_request.symbol = _Symbol;
   trade_request.volume = lot_size;
   trade_request.deviation = deviation_trade;
   trade_request.magic = 0;
   trade_request.type_filling = (ENUM_ORDER_TYPE_FILLING)type_filling;

   if(order_type == BUY)
     {
      trade_request.type = ORDER_TYPE_BUY;
      trade_request.price = price_ask;
      trade_request.tp = NormalizeDouble(trade_request.price + take_profit * _Point, _Digits);
      trade_request.sl = NormalizeDouble(trade_request.price - stop_loss * _Point, _Digits);
     }
   else
      if(order_type == SELL)
        {
         trade_request.type = ORDER_TYPE_SELL;
         trade_request.price = price_bid;
         trade_request.tp = NormalizeDouble(trade_request.price - take_profit * _Point, _Digits);
         trade_request.sl = NormalizeDouble(trade_request.price + stop_loss * _Point, _Digits);
        }
  }
//+------------------------------------------------------------------+
