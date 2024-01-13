//+------------------------------------------------------------------+
//|                                                             NH-1 |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, DavdCsam"
#property link      "https://github.com/davdcsam"

#include "modules//transaction//transaction_handler.mqh"
#include "modules//transaction//checker.mqh"

bool flag = true;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit()
  {
   update_transaction_handler();

   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+


void OnDeinit(const int reason) {Comment("");}

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick()
  {
   update_transaction_handler();
   /*
      if(flag == true)
        {
         send();
         flag = false;
        }
   */
   Comment(
      transaction_handler_comment
   );
  }
//+------------------------------------------------------------------+
