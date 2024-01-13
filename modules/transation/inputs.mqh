//+------------------------------------------------------------------+
//|                                                           Inputs |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "..\\enum.mqh"

input group "Trade"

input type_order_trade select_type = BUY;//Select Type

input double lot_size = 1;//Lot Size

input uint stop_loss = 20000;//Stop Loss

input uint take_profit = 20000;//Take Profit

input uint deviation_trade = 1000; //Deviation in Point

input turn send_order_show_string = ON;//Show String
//+------------------------------------------------------------------+
