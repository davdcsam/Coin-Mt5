//+------------------------------------------------------------------+
//|                                                            Check |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "build_request.mqh"

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void checker(
   MqlTradeRequest& request,
   MqlTradeCheckResult& result,
   float& lot_size,
   type_order_trade& order_type,
   uint& take_profit,
   uint& stop_loss,
   int& deviation_trade,
   ENUM_ORDER_TYPE_FILLING& filling_mode_to_set,
   double& price_ask,
   double& price_bid
)
  {
   int list_order_type_filling[] = {ORDER_FILLING_FOK, ORDER_FILLING_IOC, ORDER_FILLING_RETURN, ORDER_FILLING_BOC};

   for(int i=0; i<ArraySize(list_order_type_filling); i++)
     {
      build_request(request, lot_size, order_type, take_profit, stop_loss, deviation_trade, list_order_type_filling[i], price_ask, price_bid);

      if(check_position(request, result, filling_mode_to_set))
        {
         PrintFormat("Filling mode in %s is %s", _Symbol, EnumToString(filling_mode_to_set));
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
