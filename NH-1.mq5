//+------------------------------------------------------------------+
//|                                                             NH-1 |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, DavdCsam"
#property link      "https://github.com/davdcsam"

#include "modules//send_order.mqh"

bool flag = true;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {
   update_send_order_data();
   checker();

   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+


void OnDeinit(const int reason) {Comment("");}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick()
  {
   update_send_order_data();
   /*
      if(flag == true)
        {
         send();
         flag = false;
        }
   */
   Comment(
      send_order_string
   );
  }
//+------------------------------------------------------------------+
