//+------------------------------------------------------------------+
//|                                                            Check |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "build_request.mqh"
#include "calc_profit.mqh"

string checker_comment;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool check_input_lot_size(string symbol, double lot_size)
  {
   if(
      lot_size >= SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN)
      && lot_size <= SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX)
   )
     {
      return(true);
     }
   return(false);
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool check_input_devation_trade(uint take_profit, uint stop_loss, int devation_trade)
  {
   if(
      take_profit * 0.01 > devation_trade
      || stop_loss * 0.01 > devation_trade
   )
     {
      return(false);
     }
   return(true);
  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool check_input_section_time(MqlDateTime& start_time, MqlDateTime& end_time, MqlDateTime& broker_time)
  {
   long start = StructToTime(start_time);
   long end = StructToTime(end_time);
   long broker=  StructToTime(broker_time);

   if(start == end)
     {
      return(false);
     }

   if(broker >= end)
     {
      return(false);
     }

   return(true);
  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool check_filling_mode(
   MqlTradeRequest& request,
   MqlTradeCheckResult& result,
   double lot_size,
   type_order_trade order_type,
   uint take_profit,
   uint stop_loss,
   int deviation_trade,
   ENUM_ORDER_TYPE_FILLING& filling_mode_to_set,
   double price_ask,
   double price_bid
)
  {
   ENUM_ORDER_TYPE_FILLING list_order_type_filling[] = {ORDER_FILLING_FOK, ORDER_FILLING_IOC, ORDER_FILLING_RETURN, ORDER_FILLING_BOC};

   for(int i=0; i<ArraySize(list_order_type_filling); i++)
     {

      build_request(
         request,
         _Symbol,
         round_volume(
            lot_size,
            SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP)
         ),
         order_type,
         take_profit,
         stop_loss,
         deviation_trade,
         list_order_type_filling[i],
         price_ask,
         price_bid
      );

      if(fix_filling_mode(request, result, filling_mode_to_set))
        {
         return(true);
        }
      else
         if(result.retcode != TRADE_RETCODE_INVALID_FILL)
           {
            Alert(StringFormat("OrderCheck failed, return code %d: %s", result.retcode, result.comment));
           }

     }

   return(false);
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool fix_filling_mode(MqlTradeRequest& request, MqlTradeCheckResult& result, ENUM_ORDER_TYPE_FILLING& filling_mode_to_set)
  {
   if(!OrderCheck(request, result))
     {
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
bool check_position(
   MqlTradeRequest& request,
   MqlTradeCheckResult& result,
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
      _Symbol,
      round_volume(
         lot_size,
         SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP)
      ),
      order_type,
      take_profit,
      stop_loss,
      deviation_trade,
      correct_filling_mode,
      price_ask,
      price_bid
   );

   if(!OrderCheck(request, result))
     {
      return(false);
     }
   else
     {
      checker_comment = StringFormat(
                           "Trading Simulation %s Lot:%.2f, TP Line:%s, SL Line:%s, Dev:%d. Retcode: %d, %s",
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
