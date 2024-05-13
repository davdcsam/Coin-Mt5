#include "enum.mqh"

MqlDateTime time;

//Discomment the next variables if you need to how the time when this file was called
//datetime start_time = TimeCurrent();

//datetime local_start_time = TimeLocal();

datetime current_time;

int remain_time;

int Day;

int Hours; 

int Minutes; 

int Seconds;

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
        TimeToStruct(current_time, time);
        
        Day = time.day;
       
        Hours = time.hour;
       
        Minutes = time.min;
       
        Seconds = time.sec;
        
        //This string is use to bring timer data in Comment in main file
        timer_string =                
               "\n" +
               "      TIME " + IntegerToString(time.year) + "." + IntegerToString(time.mon) + "." + IntegerToString(time.day) + " " + IntegerToString(Hours) + ":" + IntegerToString(Minutes) + ":" + IntegerToString(Seconds) + " to UTS " + IntegerToString(current_time) +
               "\n"
               "      Remain Time               " + IntegerToString(remain_time) +
               "\n";        
}