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
   update_transaction_handler();

   update_section_time_handler();
   
   update_no_position_handler();

   checker(trade_request, trade_check_result, input_lot_size, input_order_type, input_take_profit, input_stop_loss, input_deviation_trade, correct_filling_type, symbol_price_ask, symbol_price_bid);

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
