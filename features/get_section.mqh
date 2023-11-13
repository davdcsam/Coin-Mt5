#include "enum.mqh"
#include "timer.mqh"
#include "send_order.mqh"
#include "close_position.mqh"

input group "Get Section"

input turn get_section_show_string = ON; // Show String

input turn close_position_out_section = OFF; // Close Positions Out Section

input type_mode_section mode_section = ADJUST;

input group "Start Section"

input int start_hour = 15; // Hour

input int start_min = 1; // Min

input int start_sec = 1; //Seg

input group "End Section"

input int end_hour = 16; // Hour

input int end_min = 0; // Min

input int end_sec = 0; //Seg

string get_section_string;

turn get_section_state = OFF;

turn get_section_day_current = OFF;

turn get_section_first_time_flag = OFF;

void get_section_ontick()
    {       
        if(
            date_time.hour > start_hour ||
            (date_time.hour == start_hour && date_time.min > start_min) ||
            (date_time.hour == start_hour && date_time.min == start_min && date_time.sec >= start_sec)
        ) 
        {
            if(
                date_time.hour < end_hour ||
                (date_time.hour == end_hour && date_time.min < end_min) ||
                (date_time.hour == end_hour && date_time.min == end_min && date_time.sec <= end_sec)
            )
            {
                get_section_state = ON;
            }
            else 
            {
                get_section_state = OFF;
            }
        }
        else 
        {
            get_section_state = OFF;
        }


        if(last_operation_day == date_time.day)
            {
                get_section_day_current = ON;
            } else 
                {
                    get_section_day_current = OFF;
                    
                    get_section_first_time_flag = ON;
                }
        
        if(close_position_out_section == ON && get_section_state == OFF)
            {
                close_position_magic_symbol();
            }
        
        if(get_section_show_string == ON)
            {
                get_section_string =
                        "\n" +
                        "      State " + EnumToString(get_section_state) + " At " + 
                        IntegerToString(start_hour) + ":" + IntegerToString(start_min) + ":" + IntegerToString(start_sec) + " to " + 
                        IntegerToString(end_hour) + ":" + IntegerToString(end_min) + ":" + IntegerToString(end_sec) + 
                        "\n" +
                        "      Close Positions Out Section " + EnumToString(close_position_out_section) + 
                        "\n";
           
            }
    }