#include "send_order.mqh"

void close_all_position()
    {
        int total_position = PositionsTotal();
    
        while(total_position != 0)
            {
                 ulong ticket = PositionGetTicket(PositionsTotal()-1);
           
                 trade.PositionClose(ticket, -1);
           
                 total_position--;
            }
    }
    
void close_position_magic_symbol()
    {
        for(int i = PositionsTotal() -1; i >= 0; i--)
            {
                ulong position_ticket = PositionGetTicket(i);
            
                if(PositionSelectByTicket(position_ticket))
                    {
                        if(PositionGetString(POSITION_SYMBOL) == _Symbol && PositionGetInteger(POSITION_MAGIC) == magic_number)
                            {
                                trade.PositionClose(position_ticket);
                            }
                    }
            }
    }