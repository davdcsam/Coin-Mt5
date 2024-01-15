//+------------------------------------------------------------------+
//|                                                             NH-1 |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, DavdCsam"
#property link      "https://github.com/davdcsam"

#include "modules//transaction//transaction_handler.mqh"
#include "modules//transaction//checker.mqh"
#include "modules//section_time//section_time_handler.mqh"
#include "modules//no_position//no_position_handler.mqh"

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {
   Alert("");
   Alert("Welcome to Coin for Mql5");

   update_transaction_handler();

   update_section_time_handler();

   update_no_position_handler();

   if(!check_input_lot_size(_Symbol, input_lot_size))
     {
      Alert("Input Lot Size is incorrect.");
      Alert(" - The correct format comprises as minimum lot %s, maximum %s and steps in %s.",
            DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN), 2),
            DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX), 2),
            DoubleToString(SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP), 2)
           );
      return(INIT_PARAMETERS_INCORRECT);
     }

   if(!check_input_devation_trade(input_take_profit, input_stop_loss, input_deviation_trade))
     {
      Alert("Input Devation Trade is incorrect.");
      Alert(" - The deviation may not be sufficient. If there is too much volatility the order could not be placed.");
     }

   if(
      !check_filling_mode(
         trade_request,
         trade_check_result,
         input_lot_size,
         input_order_type,
         input_take_profit,
         input_stop_loss,
         input_deviation_trade,
         correct_filling_type,
         symbol_price_ask,
         symbol_price_bid
      )
   )
     {
      return(INIT_PARAMETERS_INCORRECT);
     }
   else
     {
      PrintFormat("Filling mode in %s is %s", _Symbol, EnumToString(correct_filling_type));
     }

   show_comment();

   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason) {Comment("");}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick()
  {
   update_transaction_handler();

   update_section_time_handler();

   update_no_position_handler();

   operation();

   show_comment();
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void show_comment()
  {
   Comment(transaction_handler_comment, section_time_comment, no_position_comment);
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void operation()
  {
   bool flag_verify_section_time = verify_section_time();

   bool flag_verify_no_position = verify_no_position(_Symbol, 0);

   if(flag_verify_section_time && flag_verify_no_position)
     {
      Print("Trade");
      ExpertRemove();
     }
  }
//+------------------------------------------------------------------+
