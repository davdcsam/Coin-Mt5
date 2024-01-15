//+------------------------------------------------------------------+
//|                                              Transaction Handler |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "..\\enum.mqh"

MqlDateTime start_time;

MqlDateTime end_time;

MqlDateTime broker_time;

input group "Section Time"

input uchar input_start_time_hour = 15; // Start Hour

input uchar input_start_time_min = 0; // Start Min

input uchar input_start_time_seg = 6; // Start Seg

input uchar input_end_time_hour = 17; // End Hour

input uchar input_end_time_min = 0; // End Min

input uchar input_end_time_seg = 0; // End Seg

input turn input_show_section_time_handler_comment = ON; // Show Comment

string section_time_comment;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void update_section_time_hanlder()
  {
   datetime current_time = TimeCurrent();

   TimeToStruct(current_time, broker_time);

   start_time.year = broker_time.year;
   start_time.mon = broker_time.mon;
   start_time.day = broker_time.day;
   start_time.hour = input_start_time_hour;
   start_time.min = input_start_time_min;
   start_time.sec = input_start_time_seg;

   end_time.year = broker_time.year;
   end_time.mon = broker_time.mon;
   end_time.day = broker_time.day;
   end_time.hour = input_end_time_hour;
   end_time.min = input_end_time_min;
   end_time.sec = input_end_time_seg;
   
   if(StructToTime(start_time) > StructToTime(end_time))
     {
      MqlDateTime temp = start_time;
      start_time = end_time;
      end_time = temp;
     }

   if(input_show_section_time_handler_comment == ON)
     {
      string start_time_str= StringFormat("%02d:%02d:%02d", start_time.hour, start_time.min, start_time.sec);

      string end_time_str = StringFormat("%02d:%02d:%02d", end_time.hour, end_time.min, end_time.sec);

      section_time_comment = StringFormat("\n Section Time from %s to %s\n", start_time_str, end_time_str);

     }
   else
     {
      section_time_comment = "";
     }
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool verify_section_time()
  {
   return(StructToTime(start_time) <= StructToTime(broker_time) && StructToTime(broker_time) <= StructToTime(end_time));
  }
//+------------------------------------------------------------------+
