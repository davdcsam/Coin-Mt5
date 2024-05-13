//+------------------------------------------------------------------+
//|                                                     Coin-Mt5.mq5 |
//|                                         Copyright 2024, davdcsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, davdcsam"
#property link      "https://github.com/davdcsam"

#include "modules//transaction//transaction_handler.mqh"
#include "modules//transaction//checker.mqh"
#include "modules//transaction//send_order.mqh"
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

   if(!verify_no_pass_section_time())
     {
      Alert(
         StringFormat(
            "The broker's current time %s is after the set period %s to %s.",
            broker_time_str,
            start_time_str,
            end_time_str
         )
      );
      return(INIT_PARAMETERS_INCORRECT);
     }


   if(!check_input_lot_size(_Symbol, input_lot_size))
     {
      Alert("Input Lot Size is incorrect.");
      Alert(
         StringFormat(
            " - The correct format comprises as minimum lot %s, maximum %s and steps in %s.",
            DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN), 2),
            DoubleToString(SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX), 2),
            DoubleToString(SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP), 2)
         )
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

   if(!check_position(trade_request, trade_check_result, input_lot_size, input_order_type, input_take_profit, input_stop_loss, input_deviation_trade, correct_filling_type, symbol_price_ask, symbol_price_bid))
     {
      return(INIT_PARAMETERS_INCORRECT);
     }
   else
     {
      Alert(checker_comment);
      Alert(calc_profit_comment);
     }
   show_comment();

   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason) {Comment("\n", send_order_comment, "\n", calc_profit_comment);}

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
   Comment(transaction_handler_comment, section_time_comment, no_position_comment, "\n", calc_profit_comment,"\n");
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
      send_order(trade_request, trade_result, _Symbol, input_lot_size, input_order_type, input_take_profit, input_stop_loss, input_deviation_trade, correct_filling_type, symbol_price_ask, symbol_price_bid);

      Alert(send_order_comment);

      Alert(calc_profit_comment);

      ExpertRemove();
     }
  }
//+------------------------------------------------------------------+
