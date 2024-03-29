//+------------------------------------------------------------------+
//|                                              No Position Handler |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+

#include "..\\enum.mqh"
#include <Arrays\ArrayLong.mqh>
CArrayLong tickets;

input group "No Position"

input turn input_allow_no_position = ON; // Allow No Position

input turn input_show_no_position_hanlder_comment = ON; // Show Comment

string no_position_comment;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void update_no_position_handler()
  {
   if(input_show_no_position_hanlder_comment == ON)
     {
      no_position_comment = StringFormat("\n No Position is turned %s\n", EnumToString(input_allow_no_position));
     }
     else
       {
        no_position_comment = "";
       }

  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool verify_no_position(string symbol, int magic)
  {
   if(input_allow_no_position == OFF)
     {
      return(true);
     }

   get_positions(symbol, magic);

   if(tickets.Total() == 0)
     {
      return(true);
     }
   else
     {
      return(false);
     }

  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void get_positions(string symbol, int magic)
  {
   tickets.Clear();

   for(int i = PositionsTotal()-1; i >= 0; i--)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket > 0)
        {
         if(PositionGetString(POSITION_SYMBOL) == symbol && PositionGetInteger(POSITION_MAGIC) == magic)
           {
            tickets.Add(ticket);
           }
        }
     }
  }
//+------------------------------------------------------------------+
