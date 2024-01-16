//+------------------------------------------------------------------+
//|                                                       Send Order |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+

#include "build_request.mqh"
#include "calc_profit.mqh"

string send_order_comment;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool send_order(
   MqlTradeRequest& request,
   MqlTradeResult& result,
   string symbol,
   double lot_size,
   type_order_trade order_type,
   uint take_profit,
   uint stop_loss,
   int deviation_trade,
   ENUM_ORDER_TYPE_FILLING& correct_filling_mode,
   double price_ask,
   double price_bid
)
  {
   build_request(
      request,
      symbol,
      round_volume(
         lot_size,
         SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP)
      ),
      order_type,
      take_profit,
      stop_loss,
      deviation_trade,
      correct_filling_mode,
      price_ask,
      price_bid
   );

   if(!OrderSend(request, result))
     {
      send_order_comment = "";
      
      calc_profit_comment = "";
     
      return(false);
     }
   else
     {
      send_order_comment = StringFormat(
                           "Trade Result %s Lot:%.2f, TP Line:%s, SL Line:%s, Dev:%d. Retcode: %d, %s",
                           EnumToString(request.type),
                           request.volume,
                           DoubleToString(request.sl, _Digits),
                           DoubleToString(request.tp, _Digits),
                           request.deviation,
                           result.retcode,
                           result.comment
                        );

      calculated_profits(request.volume, request.type, request.symbol, request.sl, request.tp);

      return(true);
     }

   return(false);
  }
//+------------------------------------------------------------------+
