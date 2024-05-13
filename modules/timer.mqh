//+------------------------------------------------------------------+
//|                                                             NH-1 |
//|                                         Copyright 2024, DavdCsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, DavdCsam"
#property link      "https://github.com/davdcsam"

#include "enum.mqh"

MqlDateTime date_time;

//Discomment the next variables if you need to how the time when this file was called
//datetime start_time = TimeCurrent();

//datetime local_start_time = TimeLocal();

//Define the variable for get time in timer_ontick()
datetime current_time;

int remain_time;

int period;

int m1_to_seconds = 60;

int current_period;

string timer_string;

//timer_ontick() necessarily need to be in ontick event handler
void timer_ontick()
  {
//Obtain the current period in the graph
   period = _Period;

   current_period = period * m1_to_seconds;

//Update the value of current_time
   current_time = TimeCurrent();

//iTime obtain the opening date of the current candlestick
//Subtracting the current_time from the opening time of a candlestick gives a negative number representing how much time has elapsed since the candlestick opened
//To make the number positive, current_period is added to it, which represents the time needed to create the next candle.
//(int) is used to convert the output of curren_time, iTime and current_period to an integer.
   remain_time = (int)(iTime(_Symbol, PERIOD_CURRENT, 0) - current_time + current_period);

//The next struct is use to get the current time and date with for indepents integer variables

   TimeToStruct(current_time, date_time);

//This string is use to bring timer data in Comment in main file
   timer_string =
      "\n" +
      "      TIME " + IntegerToString(date_time.year) + "." + IntegerToString(date_time.mon) + "." + IntegerToString(date_time.day) + " " + IntegerToString(date_time.hour) + ":" + IntegerToString(date_time.min) + ":" + IntegerToString(date_time.sec) + " to UTS " + IntegerToString(current_time) +
      "\n";
  }
//+------------------------------------------------------------------+
