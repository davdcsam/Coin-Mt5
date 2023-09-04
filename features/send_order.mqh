#include <Trade/Trade.mqh>
CTrade trade;

#include "enum.mqh"
#include "timer.mqh"

MqlTradeRequest request_trade = {};
        
MqlTradeResult result_trade = {};

input group "Trade"

input ENUM_ORDER_TYPE select_type = ORDER_TYPE_BUY;//Select Order

input double lot = 4;//Lot Size

input double stoplose = 105;//Stop Lose

input double takeprofit = 105;//Take Profit

input uint magic_number = 666;//Magic Number

input ulong deviation_trade = 10; //Deviation in Point

input turn send_order_show_string = OFF;//Show String

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
   
        request_trade.volume                   = lot;
   
        request_trade.type                     = ORDER_TYPE_SELL;
   
        request_trade.price                    = price_bid;
   
        request_trade.sl                       = request_trade.price + stoplose;
      
        request_trade.tp                       = request_trade.price - takeprofit;
   
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
                    
                    last_operation_day = Day;
                }
    }
  
void buy_function()
    {        
        Print("Sending BUY order in ", _Symbol, " with ", magic_number);
   
        request_trade.action                   = TRADE_ACTION_DEAL;
   
        request_trade.symbol                   = _Symbol;
   
        request_trade.volume                   = lot;
   
        request_trade.type                     = ORDER_TYPE_BUY;
   
        request_trade.price                    = price_ask;
   
        request_trade.sl                       = request_trade.price - stoplose;
        
        request_trade.tp                       = request_trade.price + takeprofit;

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
                    
                    last_operation_day = Day;
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
                    "      Lot Size                      "  + DoubleToString(lot, _Digits) +
                    "\n"
                    "      Stop Lose                   "    + DoubleToString(stoplose, 0) +
                    "\n"
                    "      Take Profit                  "   + DoubleToString(takeprofit, 0) +
                    "\n";           
          }
    }