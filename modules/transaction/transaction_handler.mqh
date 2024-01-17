//+------------------------------------------------------------------+
//|                                              Transaction Handler |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "..\\enum.mqh"

MqlTradeRequest trade_request;

MqlTradeCheckResult trade_check_result;

MqlTradeResult trade_result;

input group "Trade"

input type_order_trade input_order_type = BUY;//Select Order

input float input_lot_size = 1;//Lot Size

input uint input_take_profit = 20000;//Take Profit

input uint input_stop_loss = 20000;//Stop Loss

input uint input_deviation_trade  = 1000; //Deviation in Point

input turn input_show_transaction_handler_comment = ON;//Show Comment

double symbol_price_close;

double symbol_price_ask;

double symbol_price_bid;

double symbol_tick_size;

ENUM_ORDER_TYPE_FILLING correct_filling_type;

string transaction_handler_comment;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void update_transaction_handler()
  {
   symbol_price_ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

   symbol_price_bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);

   symbol_tick_size = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);

   symbol_price_ask = round(symbol_price_ask / symbol_tick_size) * symbol_tick_size;

   symbol_price_bid = round(symbol_price_bid / symbol_tick_size) * symbol_tick_size;

   if(input_show_transaction_handler_comment == ON)
     {
      transaction_handler_comment = StringFormat(
                                       "\n Type %s\n Lot Size %s\n Stop Loss %d\n Take Profit %d\n Devation %d\n Correct Filling %s\n",
                                       EnumToString(input_order_type),
                                       trade_request.volume,
                                       input_stop_loss,
                                       input_take_profit,
                                       input_deviation_trade,
                                       EnumToString(correct_filling_type)
                                    );
     }
   else
     {
      transaction_handler_comment = "";
     }
  }
//+------------------------------------------------------------------+
