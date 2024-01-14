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

input uchar input_start_time_hour;

input uchar input_start_time_min;

input uchar input_start_time_seg;

input uchar input_end_time_hour;

input uchar input_end_time_min;

input uchar input_end_time_seg;

input turn input_show_section_time_handler_comment = ON;

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
   
   string start_time_str= StringFormat("%d.%02d.%02d %02d:%02d:%02d", start_time.year, start_time.mon, start_time.day, start_time.hour, start_time.min, start_time.sec);
   
   string end_time_str = StringFormat("%d.%02d.%02d %02d:%02d:%02d", start_time.year, start_time.mon, start_time.day, start_time.hour, start_time.min, start_time.sec);
   
   PrintFormat("Section Time from %s to %s", start_time_str, end_time_str);

  }
//+------------------------------------------------------------------+
