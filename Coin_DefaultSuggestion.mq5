//+------------------------------------------------------------------+
//|                                       Coin_DefaultSuggestion.mq5 |
//|                                         Copyright 2024, davdcsam |
//|                                      https://github.com/davdcsam |
//+------------------------------------------------------------------+
#property copyright "Copyright 2024, davdcsam"
#property link      "https://github.com/davdcsam"

// Include necessary modules for handling different aspects of the trading bot
#include <AutomatedTradingMQL5/transaction/Transaction.mqh>
#include <AutomatedTradingMQL5/section_time/SectionTime.mqh>
#include <AutomatedTradingMQL5/filter_nod/FilterNOD.mqh>
#include <AutomatedTradingMQL5/remove/Remove.mqh>
#include <AutomatedTradingMQL5/profit_protection/ProfitProtection.mqh>
#include <AutomatedTradingMQL5/detect/DetectPositions.mqh>

// Group of inputs related to trade
input group "Trade"

// Input to allow sending extra orders
input bool input_allow_extra_orders = false; // Allow extra orders

// Input for the position type
input ENUM_ORDER_PENDING_TYPE input_order_type = ORDER_PENDING_TYPE_BUY; // Position Type

// Input for the lot size
input double input_lot_size = 1; // Lot Size

// Input for the take profit
input uint input_take_profit = 10000; // Take Profit

// Input for the stop loss
input uint input_stop_loss = 2500; // Stop Loss

// Input for the deviation trade
input uint input_deviation_trade  = 100; // Deviation

// Input for the magic number
input ulong input_magic_number = 420; // Magic Number

Transaction transaction(_Symbol, MathAbs(input_lot_size), input_take_profit, input_stop_loss, input_deviation_trade, input_magic_number);

// Function to update the comment for the transaction
string              TransactionCommentInput()
  {
   return StringFormat(
             " Send Extra Orders: %s\n Type: %s\n",
             input_allow_extra_orders ? "Allowed" : "Prohibited",
             input_order_type == ORDER_PENDING_TYPE_BUY ? "Buy" : "Sell"
          );
  }

// -- -- //

// Group of inputs related to section time
input group "Section Time"

input bool input_remove_positions_out_section_time = false; // Remove Positions Out Section Time

// Inputs for the start and end times
input uchar input_start_time_hour = 15; // Start Hour

input uchar input_start_time_min = 0; // Start Min

input uchar input_start_time_seg = 6; // Start Seg

input uchar input_end_time_hour = 17; // End Hour

input uchar input_end_time_min = 0; // End Min

input uchar input_end_time_seg = 0; // End Seg

// Create a new SectionTime object
SectionTime section_time(input_start_time_hour, input_start_time_min, input_start_time_seg, input_end_time_hour, input_end_time_min, input_end_time_seg);

RemoveByOrderType remove();

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string RemoveCommentInput()
  {
   return StringFormat(
             " Remove Positions Out: %s\n",
             input_remove_positions_out_section_time ? "Allowed" : "Prohibited"
          );
  }

// -- -- //

input group "Filter By Day Week"

input bool input_filter_by_day_week = false; // Filter By Day Week

input bool input_filter_by_day_week_sunday = true; // Sunday

input bool input_filter_by_day_week_monday = true; // Monday

input bool input_filter_by_day_week_tuesday = true; // Tuesday

input bool input_filter_by_day_week_wednesday = true; // Wednesday

input bool input_filter_by_day_week_thursday = true; // Thursday

input bool input_filter_by_day_week_friday = true; // Friday

input bool input_filter_by_day_week_saturday = false; // Saturday

FilterByDayWeek filterByDayWeek;

FilterByDayWeek::Frame frame;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string FilterByDayWeekCommentInput(void)
  {
   return StringFormat(
             "\n FilterByDayWeek to Operative:%s%s%s%s%s%s%s\n",
             input_filter_by_day_week_sunday ? " Sun" : "",
             input_filter_by_day_week_monday ? " Mon" : "",
             input_filter_by_day_week_tuesday ? " Tue" : "",
             input_filter_by_day_week_wednesday ? " Wed" : "",
             input_filter_by_day_week_thursday ? " Thu" : "",
             input_filter_by_day_week_friday ? " Fri" : "",
             input_filter_by_day_week_saturday ? " Sat" : ""
          );
  }

// -- -- //

input group "Filter By CSV File"

input bool input_filter_by_csv_file = false; // Active

input string input_filter_by_csv_file_name = "days.csv"; // Name

FilterByCSVFile filterByCSVFile;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
string FilterByCSVFileCommentInput(void)
  {
   return StringFormat(
             "\n Filter By CSV File getting from %s\n",
             input_filter_by_csv_file_name
          );
  }

// -- -- //

// Group of inputs for the profit protection
input group "Profit Protection";

// Boolean to check if break even is active
input bool input_active_profit_protection = true; // Active

input ENUM_PROFIT_PROTECTION_TYPE input_profit_protection_type = BREAK_EVEN; // Type

// Activation percent for the break even
input uchar input_profit_protection_activation_percent = 30; // Activation Percent

// Deviation percent from the open price for the break even
input uchar input_profit_protection_deviation_percent= 10; // Deviation Percent

// Instance of the BreakEven class
BreakEven break_even(input_profit_protection_activation_percent, input_profit_protection_deviation_percent);


// Instance of the TrailingStop class
TrailingStop trailing_stop(input_profit_protection_activation_percent, input_profit_protection_deviation_percent);

// Function to update the comment for the profit protection handler
string ProfitProtectionCommentInput()
  {
   string result;

   switch(input_profit_protection_type)
     {
      case BREAK_EVEN:
         result = StringFormat(
                     "\n BreakEven: %s\n Activation Percent: %d\n Deviation Percent From Open Price: %d \n",
                     input_active_profit_protection ? "Allowed" : "Prohibited",
                     input_profit_protection_activation_percent,
                     input_profit_protection_deviation_percent
                  );
         break;
      case TRAILING_STOP:
         result = StringFormat(
                     "\n TrailingStop: %s\n Activation Percent: %d\n Deviation Percent From Current Price: %d \n",
                     input_active_profit_protection ? "Allowed" : "Prohibited",
                     input_profit_protection_activation_percent,
                     input_profit_protection_deviation_percent
                  );
         break;
     }

   return result;
  }


// Global variables
MqlDateTime last_operation;
DetectPositions detect_positions;

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
int OnInit(void)
  {
// Check if the bot has full access to trade
   ENUM_SYMBOL_TRADE_MODE symbol_trade_mode = ENUM_SYMBOL_TRADE_MODE(SymbolInfoInteger(_Symbol, SYMBOL_TRADE_MODE));
   if(symbol_trade_mode != SYMBOL_TRADE_MODE_FULL)
     {
      Alert(
         StringFormat(
            "BreakLevel need a Full Access Trade. %s has %s. Go to Symbols/your-symbol/Trade.",
            _Symbol,
            EnumToString(symbol_trade_mode)
         )
      );
      return(INIT_FAILED);
     }

// Welcome message
   Alert("Welcome to Coin Default Suggestion");

// Check Section Time Input
   ENUM_CHECK_SECTION_TIME result_section_time_arg = section_time.CheckArg();
   if(result_section_time_arg != CHECK_ARG_SECTION_TIME_PASSED)
     {
      Alert(section_time.EnumCheckSectionTimeToString(result_section_time_arg));
      return(INIT_PARAMETERS_INCORRECT);
     }
   else
      Print(section_time.EnumCheckSectionTimeToString(result_section_time_arg));

// Check Transaction Inputs
   ENUM_CHECK_TRANSACTION result_transaction_check_arg = transaction.CheckArg();
   if(
      result_transaction_check_arg != CHECK_ARG_TRANSACTION_PASSED
      && result_transaction_check_arg != ERR_DEVIATION_INSUFFICIENT
   )
     {
      Alert(transaction.EnumCheckTransactionToString(result_transaction_check_arg));
      return(INIT_PARAMETERS_INCORRECT);
     }
   else
     {
      if(result_transaction_check_arg == ERR_DEVIATION_INSUFFICIENT)
         Alert(transaction.EnumCheckTransactionToString(ERR_DEVIATION_INSUFFICIENT));

      Print(transaction.EnumCheckTransactionToString(CHECK_ARG_TRANSACTION_PASSED));
     }

// Fix Filling Mode
   ENUM_FIX_FILLING_MODE result_fix_filling_mode = transaction.FixFillingMode();
   if(result_fix_filling_mode != FILLING_MODE_FOUND)
     {
      Alert(transaction.EnumFixFillingModeToString(result_fix_filling_mode));
      return(INIT_FAILED);
     }
   else
      Print(transaction.EnumFixFillingModeToString(result_fix_filling_mode));

   ShowComment();

// Initialize Operation Day by Day Week
   if(input_filter_by_day_week)
     {
      frame.sunday = input_filter_by_day_week_sunday;
      frame.monday = input_filter_by_day_week_monday;
      frame.tuesday = input_filter_by_day_week_tuesday;
      frame.wednesday = input_filter_by_day_week_wednesday;
      frame.thursday = input_filter_by_day_week_thursday;
      frame.friday = input_filter_by_day_week_friday;
      frame.saturday = input_filter_by_day_week_saturday;

      filterByDayWeek.UpdateAtr(frame);
     }

//  Initialize Operation Day by Week
   if(input_filter_by_csv_file)
     {
      if(!filterByCSVFile.UpdateAtr(input_filter_by_csv_file_name))
         return(INIT_PARAMETERS_INCORRECT);

      if(!filterByCSVFile.Read())
         return(INIT_FAILED);
     }

// Initialize Extra Component
   remove.UpdateAtr(input_magic_number, _Symbol);

   break_even.UpdateRequiredAtr(input_magic_number, _Symbol);

   trailing_stop.UpdateRequiredAtr(input_magic_number, _Symbol);

   detect_positions.UpdateAtr(_Symbol, input_magic_number);

   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
// Restart the comment
   Comment("");
  }

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void OnTick(void)
  {
// Verify if the profit protection measures (break even and trailing stop) are active
   VerifyProfitProtection();

// Update the section time
   section_time.Update();

// Verify if the current time is within the section time
   VerifySectionTime();

// Show the comment on the chart
   ShowComment();
  }

// This function verifies if the profit protection measures (break even and trailing stop) are active. If they are, it verifies them.
void VerifyProfitProtection()
  {
   if(!input_active_profit_protection)
     { return; }

   switch(input_profit_protection_type)
     {
      case BREAK_EVEN:
         break_even.Verify();
         break;
      case TRAILING_STOP:
         trailing_stop.Verify();
         break;
     }
  }


// This function verifies if the current time is within the section time. If it's not, it removes positions and pending orders if necessary. If it is, it verifies extra orders.
void VerifySectionTime()
  {

// If the current time is not within the section time
   if(!section_time.VerifyInsideSection())
     {
      if(input_remove_positions_out_section_time)
         remove.RemovePositions();
     }
   else
     {
      // If the current day is different from the last operation day, verify extra orders
      if(last_operation.day != section_time.broker_datetime.day)
         VerifyExtraOrders();
     }
  }

// This function verifies if extra orders are allowed. If they are, it sends orders. If they're not, it updates orders and positions and sends orders if necessary.
void VerifyExtraOrders()
  {

// If extra orders are allowed, send orders
   if(input_allow_extra_orders)
      SendOrders();
   else
     {
      // If there are no orders and positions, send orders
      if(!detect_positions.UpdatePositions())
         SendOrders();
     }
  }

// This function sends orders based on the type of near lines. It gets the near lines, updates the comment lines, and sends orders accordingly.
void SendOrders()
  {
   TimeCurrent(last_operation);

   if(input_filter_by_csv_file)
     {
      bool isOperativeDay = filterByCSVFile.IsOperativeDay();

      PrintFormat(
         "Today %s is %s operative day",
         TimeToString(TimeCurrent()),
         isOperativeDay ? "a" : "NOT a"
      );
      if(!isOperativeDay)
         return;
     }

   if(input_filter_by_day_week)
     {
      bool isOperativeDay = filterByDayWeek.IsOperativeDay();

      PrintFormat(
         "Today %s is %s operative day",
         EnumToString(ENUM_DAY_OF_WEEK(last_operation.day_of_week)),
         isOperativeDay ? "a" : "NOT a"

      );
      if(!isOperativeDay)
         return;
     }

   Print(
      (input_order_type == ORDER_PENDING_TYPE_BUY) ?
      transaction.EnumOrderTransactionToString(transaction.SendPosition(ENUM_POSITION_TYPE(ORDER_PENDING_TYPE_BUY))) :
      transaction.EnumOrderTransactionToString(transaction.SendPosition(ENUM_POSITION_TYPE(ORDER_PENDING_TYPE_SELL)))
   );
  }


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
// This function updates the comments for transaction, lines, section time, removal, and profit protection, and then shows them on the chart.
void ShowComment()
  {
   if(MQLInfoInteger(MQL_TESTER) && !MQLInfoInteger(MQL_VISUAL_MODE))
     {
      return;
     }

// Show the comments on the chart
   Comment(
      transaction.CommentToShow(),
      TransactionCommentInput(),
      section_time.CommentToShow(),
      input_remove_positions_out_section_time ? RemoveCommentInput() : "",
      input_filter_by_day_week ? FilterByDayWeekCommentInput() : "",
      input_filter_by_csv_file ? FilterByCSVFileCommentInput() : "",
      input_active_profit_protection ? ProfitProtectionCommentInput() : ""
   );
  }
//+------------------------------------------------------------------+
