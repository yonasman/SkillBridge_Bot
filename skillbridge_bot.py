import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext,CallbackQueryHandler
from datetime import datetime
from dotenv import load_dotenv
import os
from google_sheets_handler import add_student_to_course

#load the .env file
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# # Define states
CHOOSING_TYPE, BOOTCAMP_SELECTION,SHOLARSHIP_SELECTION,LANGUAGE_SELECTION, REGISTRATION_NAME, REGISTRATION_PHONE, REGISTRATION_EMAIL, REGISTRATION_PROFESSION, SCHOLARSHIP_REASON, \
REGISTRATION_ADDRESS, REGISTRATION_EDUCATION, REGISTRATION_INSTITUTION, REGISTRATION_SOURCE, REGISTRATION_MORE_INFO = range(14)

# Define bootcamp and scholarship options
bootcamp_options = [["DSA Bootcamp", "Python Mastery"], ["Full-Stack Development", "Mobile App Development"],
                    ["Data Science and ML","Cybersecurity"],["Cloud Computing","Devops"], ["Motion Graphics","3D Modeling"], ["Video Editing", "Graphics Design"],
                    ["UX/UI Design", "Digital Marketing"], ["Languages", "Others"]]

scholarship_options = [["DSA Scholarship", "Python Mastery Scholarship"], ["Full-Stack Scholarship", "Mobile App Scholarship"],
                       ["Data Science and ML Scholarship","Cybersecurity Scholarship"],["Cloud Computing Scholarship","Devops Scholarship"],[ "3D Modeling Scholarship", "Motion Graphics Scholarship"],
                       ["Video Editing Scholarship", "UX/UI Design Scholarship"], ["Digital Marketing Scholarship", "Languages Scholarship"], ["Others"]]

language_options = [["English","French"],["Arabic","Germany"],["Chinese","Others"]]

user_info = []

async def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["Bootcamp Registration", "Scholarship Registration"]]
    await update.message.reply_text(
        "Welcome to SkillBridge! Please choose an option to proceed:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_TYPE


def get_reset_cancel_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Reset", callback_data="reset"),
         InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def choose_registration_type(update: Update, context: CallbackContext) -> int:
    choice = update.message.text
    context.user_data["registration_type"] = choice
    
    if choice == "Bootcamp Registration":
        await update.message.reply_text("Select a bootcamp:",
            reply_markup=ReplyKeyboardMarkup(bootcamp_options, one_time_keyboard=True, resize_keyboard=True))
        return BOOTCAMP_SELECTION
    
    elif choice == "Scholarship Registration":
        await update.message.reply_text("Select a scholarship:",
            reply_markup=ReplyKeyboardMarkup(scholarship_options, one_time_keyboard=True, resize_keyboard=True))
        return SHOLARSHIP_SELECTION
    
    await update.message.reply_text("Invalid choice. Please try again.")
    return CHOOSING_TYPE

async def select_bootcamp(update: Update, context: CallbackContext) -> int:
    context.user_data["bootcamp"] = update.message.text

    if context.user_data.get("bootcamp") == "Languages":

        await update.message.reply_text("Select a Language:",
            reply_markup=ReplyKeyboardMarkup(language_options, one_time_keyboard=True, resize_keyboard=True))
        return LANGUAGE_SELECTION
    
    await update.message.reply_text("Enter your Full Name:\nሙሉ ስምዎን ያስገቡ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_NAME 

async def select_scholarship(update: Update, context: CallbackContext) -> int:
    context.user_data["scholarship"] = update.message.text

    context.user_data['is_scholarship_selected'] = True
    user_info.append(update.message.text)

    if context.user_data.get("bootcamp") == "Languages":
         
        await update.message.reply_text("Select a Language:",
            reply_markup=ReplyKeyboardMarkup(language_options, one_time_keyboard=True, resize_keyboard=True))
        
        return LANGUAGE_SELECTION
    
    await update.message.reply_text("Enter your Full Name:\nሙሉ ስምዎን ያስገቡ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_NAME

async def select_language(update: Update, context: CallbackContext) -> int:
    context.user_data["language"] = update.message.text

    await update.message.reply_text("Enter your Full Name:\nሙሉ ስምዎን ያስገቡ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_NAME   

async def enter_name(update: Update, context: CallbackContext) -> int:
    context.user_data["name"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Enter your Phone Number\nስልክ ኩትር፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_PHONE

async def enter_phone(update: Update, context: CallbackContext) -> int:
    context.user_data["phone"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Enter your Email:\nኢመል ያስገቡ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_EMAIL

async def enter_email(update: Update, context: CallbackContext) -> int:
    context.user_data['email'] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("What is your current profession? e.g student, developer...\n ስራዎ ምንድነው? ተማሪ፣ ደቨሎፐር...",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_PROFESSION

async def enter_profession(update: Update, context: CallbackContext) -> int:
    context.user_data["profession"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Enter your address:\nአድራሥሃዎ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_ADDRESS

async def enter_address(update: Update, context: CallbackContext) -> int:
    context.user_data["address"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("What is your Highest education level?\nከፍተኛ የትምርህችት ደረጃ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_EDUCATION

async def enter_education(update: Update, context: CallbackContext) -> int:
    context.user_data["education"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Which institution did you attend?\nየተማሩበት ትኳም፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_INSTITUTION

async def enter_scho_reason(update: Update, context: CallbackContext) -> int:
    context.user_data["scholarship_reason"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Which institution did you attend?\nየተማሩበት ትኳም፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_INSTITUTION

async def enter_institution(update: Update, context: CallbackContext) -> int:
    context.user_data["institution"] = update.message.text
    user_info.append(update.message.text)

    if context.user_data.get("is_scholarship_app"):
        return SCHOLARSHIP_REASON
    await update.message.reply_text("Where did you hear about us?\nስለኛ ከየት ሰሙ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_SOURCE
async def enter_source(update: Update, context: CallbackContext) -> int:
    context.user_data["source"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Any additional information?\nተችማሪ መረጃ፡",reply_markup=get_reset_cancel_keyboard())
    return REGISTRATION_MORE_INFO

async def enter_more_info(update: Update, context: CallbackContext) -> int:
    context.user_data["more_info"] = update.message.text
    user_info.append(update.message.text)
    await update.message.reply_text("Thanks!, Registration complete! ✅")
    return ConversationHandler.END

async def reset(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("Registration reset. Please start again:",
                                   reply_markup=ReplyKeyboardMarkup([["Bootcamp Registration", "Scholarship Registration"]], one_time_keyboard=True, resize_keyboard=True))
    return CHOOSING_TYPE


async def cancel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    print(query)
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("Registration cancelled. You can start again anytime by using /start.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_registration_type)],
            BOOTCAMP_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_bootcamp)],
            SHOLARSHIP_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_scholarship)],
            SCHOLARSHIP_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_scholarship)],
            LANGUAGE_SELECTION:[MessageHandler(filters.TEXT & ~filters.COMMAND, select_language)],
            REGISTRATION_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            REGISTRATION_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
            REGISTRATION_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_email)],
            REGISTRATION_PROFESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND,enter_profession)],
            REGISTRATION_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_address)],
            REGISTRATION_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_education)],
            REGISTRATION_INSTITUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_institution)],
            REGISTRATION_SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_source)],
            REGISTRATION_MORE_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_more_info)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(reset, pattern="^reset$"))
    app.add_handler(CallbackQueryHandler(cancel, pattern="^cancel$"))
    app.run_polling()

if __name__ == "__main__":
    main()
