#include <Trade/Trade.mqh>
CTrade trade;

#include "enum.mqh"
#include "timer.mqh"

MqlTradeRequest request_trade = {};
        
MqlTradeResult result_trade = {};

input group "Trade"

input type_order_trade select_type = BUY;//Select Type

input double lot_size = 4;//Lot Size

input double stop_loss = 105;//Stop Loss

input double take_profit = 105;//Take Profit

input uint magic_number = 666;//Magic Number

input ulong deviation_trade = 10; //Deviation in Point

input turn send_order_show_string = ON;//Show String

int count_operation;

int last_operation_day;

double price_close;

double price_ask;

double price_bid;

double tick_size;

string comment_trade;

string send_order_string;

void sell_function()
    {
        Print( "Sending SELL order in ", _Symbol, " with ", magic_number ); 
   
        request_trade.action                   = TRADE_ACTION_DEAL;
   
        request_trade.symbol                   = _Symbol;
   
        request_trade.volume                   = lot_size;
   
        request_trade.type                     = ORDER_TYPE_SELL;
   
        request_trade.price                    = price_bid;
   
        request_trade.sl                       = request_trade.price + stop_loss;
      
        request_trade.tp                       = request_trade.price - take_profit;
   
        request_trade.deviation                = deviation_trade;
   
        request_trade.magic                    = magic_number;
   
        request_trade.comment                  = comment_trade;
        
        request_trade.type_filling              = ORDER_FILLING_IOC;        
   
        if( !OrderSend( request_trade, result_trade ) )
            {
                Alert( "Error sending order, code: ", GetLastError() );
            } else 
                {
                    Print(request_trade.symbol, " ", result_trade.retcode, " ", " | Lot ", request_trade.volume, " Price ", DoubleToString(result_trade.price, _Digits));
                    
                    count_operation++;
                    
                    last_operation_day = date_time.day;
                }
    }
  
void buy_function()
    {        
        Print("Sending BUY order in ", _Symbol, " with ", magic_number);
   
        request_trade.action                   = TRADE_ACTION_DEAL;
   
        request_trade.symbol                   = _Symbol;
   
        request_trade.volume                   = lot_size;
   
        request_trade.type                     = ORDER_TYPE_BUY;
   
        request_trade.price                    = price_ask;
   
        request_trade.sl                       = request_trade.price - stop_loss;
        
        request_trade.tp                       = request_trade.price + take_profit;

        request_trade.deviation                = deviation_trade;
   
        request_trade.magic                    = magic_number;
   
        request_trade.comment                  = comment_trade;
        
        request_trade.type_filling             = ORDER_FILLING_IOC;
   
        if(!OrderSend(request_trade, result_trade))
            {
                Alert("Error en el envio de la orden", GetLastError());
            } else
                {
                    Print(request_trade.symbol, " ", result_trade.retcode, " ", " | Lot ", request_trade.volume, " Price ", DoubleToString(result_trade.price, _Digits));
                                   
                    count_operation++;
                    
                    last_operation_day = date_time.day;
                }
    }

void send_order_ontick()
    {
        price_ask                              = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   
        price_bid                              = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   
        tick_size                              = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   
        price_ask                              = round( price_ask / tick_size ) * tick_size;
   
        price_bid                              = round( price_bid / tick_size ) * tick_size;
        
        price_close                            = iClose(_Symbol, PERIOD_CURRENT, 0);
    
        if(send_order_show_string == ON)
            {
                send_order_string =
                    "\n" +
                    "      Lot Size                      "  + DoubleToString(lot_size, _Digits) +
                    "\n"
                    "      Stop Loss                   "    + DoubleToString(stop_loss, 0) +
                    "\n"
                    "      Take Profit                  "   + DoubleToString(take_profit, 0) +
                    "\n";           
          }
    }