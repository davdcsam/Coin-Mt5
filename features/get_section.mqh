#include "enum.mqh"
#include "timer.mqh"
#include "send_order.mqh"

input group "Get Section"

input int get_section_start_hour = 15; // Start

input int get_section_start_minute = 0; // Start

input int get_section_end_hour = 16; // End

string get_section_string;

turn get_section_state = OFF;

turn get_section_day_current = OFF;

turn get_section_first_time_flag = OFF;

void get_section_ontick()
    {       
        if(((Hours == get_section_start_hour && Minutes >= get_section_start_minute) || Hours > get_section_start_hour) && (Hours < get_section_end_hour))
            {
                get_section_state = ON;
            }
            
        if((Hours < get_section_start_hour && Minutes < get_section_start_minute) || (Hours > get_section_end_hour))
            {
                get_section_state = OFF;
            }            
            
        if(last_operation_day == Day)
            {
                get_section_day_current = ON;
            } else 
                {
                    get_section_day_current = OFF;
                    
                    get_section_first_time_flag = ON;
                }
                
        get_section_string =
                "\n" +
                "      State " + EnumToString(get_section_state) + " At " + IntegerToString(get_section_start_hour) + " to " + IntegerToString(get_section_end_hour) +
                "\n";
    }