//+------------------------------------------------------------------+
//|                                              Transaction Handler |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#include "..\\enum.mqh"

MqlDateTime start_datetime;

MqlDateTime end_datetime;

MqlDateTime broker_datetime;

input group "Section Time"

input uchar input_start_time_hour = 15; // Start Hour

input uchar input_start_time_min = 0; // Start Min

input uchar input_start_time_seg = 6; // Start Seg

input uchar input_end_time_hour = 17; // End Hour

input uchar input_end_time_min = 0; // End Min

input uchar input_end_time_seg = 0; // End Seg

input turn input_show_section_time_handler_comment = ON; // Show Comment

string start_time_str;

string end_time_str;

string broker_time_str;

string section_time_comment;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void update_section_time_handler()
  {
   TimeToStruct(TimeCurrent(), broker_datetime);

   start_datetime.year = broker_datetime.year;
   start_datetime.mon = broker_datetime.mon;
   start_datetime.day = broker_datetime.day;
   start_datetime.hour = input_start_time_hour;
   start_datetime.min = input_start_time_min;
   start_datetime.sec = input_start_time_seg;

   end_datetime.year = broker_datetime.year;
   end_datetime.mon = broker_datetime.mon;
   end_datetime.day = broker_datetime.day;
   end_datetime.hour = input_end_time_hour;
   end_datetime.min = input_end_time_min;
   end_datetime.sec = input_end_time_seg;

   if(StructToTime(start_datetime) > StructToTime(end_datetime))
     {
      MqlDateTime temp = start_datetime;
      start_datetime = end_datetime;
      end_datetime = temp;
     }


   start_time_str= StringFormat("%02d:%02d:%02d", start_datetime.hour, start_datetime.min, start_datetime.sec);

   end_time_str = StringFormat("%02d:%02d:%02d", end_datetime.hour, end_datetime.min, end_datetime.sec);

   broker_time_str = StringFormat("%02d:%02d:%02d", broker_datetime.hour, broker_datetime.min, broker_datetime.sec);

   if(input_show_section_time_handler_comment == ON)
     {
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
   return(StructToTime(start_datetime) <= StructToTime(broker_datetime) && StructToTime(broker_datetime) <= StructToTime(end_datetime));
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool verify_no_pass_section_time()
  {
   return(StructToTime(broker_datetime) < StructToTime(end_datetime));
  }
//+------------------------------------------------------------------+
