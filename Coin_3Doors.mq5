//+------------------------------------------------------------------+
//|                                                       3doors.mq5 |
//|                                         Copyright 2023, davdcsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, davdcsam"
#property link      "https://github.com/davdcsam"

#include "features\\timer.mqh"
#include "features\\get_section.mqh"
#include "features\\send_order.mqh"
#include "features\\close_position.mqh"

ENUM_ORDER_TYPE switch_order_type = select_type;

void select_order()
{
    switch(switch_order_type)
        {
            case ORDER_TYPE_BUY:
                switch_order_type = ORDER_TYPE_SELL;
                sell_function();
                break;
            
            case ORDER_TYPE_SELL:
                switch_order_type = ORDER_TYPE_BUY;
                buy_function();
                break;
    
            default:
                Alert("No valid type position, only allowed ORDER_TYPE_SELL and ORDER_TYPE_BUY");
                break;
        }
    }

void operation_module()
    {
        if(get_section_state == ON && get_section_first_time_flag == ON && get_section_day_current == OFF)
            {
                select_order();
            }
        if(get_section_state == OFF)
            {
                close_position_magic_symbol();
            }
    }

int OnInit()
    {
        return(INIT_SUCCEEDED);
    }

void OnDeinit(const int reason) {Comment("");}

void OnTick()
    {
    
        timer_ontick();
    
        get_section_ontick();
        
        send_order_ontick();
        
        operation_module();
        
        Comment(     
               timer_string,
               get_section_string,
               send_order_string
        );                     
    }