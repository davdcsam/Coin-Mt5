#include "enum.mqh"
#include "timer.mqh"
#include "send_order.mqh"
#include "close_position.mqh"

input group "Section Time"

input turn section_time_show_string = ON; // Show String

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

string section_time_string;

turn section_time_state = OFF;

turn section_time_day_current = OFF;

turn section_time_first_time_flag = OFF;

void set_section_time()
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
                section_time_state = ON;
            }
            else 
            {
                section_time_state = OFF;
            }
        }
        else 
        {
            section_time_state = OFF;
        }    
    }

void section_flag_swicther_day()
    {
        if(last_operation_day == date_time.day)
            {
                section_time_day_current = ON;
            } else
                {
                    section_time_day_current = OFF;
                    section_time_first_time_flag = ON;
                }
    }

void section_close_out()
    {
        if(close_position_out_section == ON && section_time_state == OFF)
            {
                close_position_magic_symbol();
            }
    }

void section_show_string()
    {
        if(section_time_show_string == ON)
            {
                section_time_string =
                        "\n" +
                        "      State " + EnumToString(section_time_state) + " At " + 
                        IntegerToString(start_hour) + ":" + IntegerToString(start_min) + ":" + IntegerToString(start_sec) + " to " + 
                        IntegerToString(end_hour) + ":" + IntegerToString(end_min) + ":" + IntegerToString(end_sec) + 
                        "\n" +
                        "      Close Positions Out Section " + EnumToString(close_position_out_section) + 
                        "\n";
            }
    }

void section_time_ontick()
    {
        set_section_time();

        section_flag_swicther_day();
   
        section_close_out();

        section_show_string();
    }