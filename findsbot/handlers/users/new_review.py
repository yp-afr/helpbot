from aiogram import types
from aiogram.dispatcher import FSMContext

from findsbot.filters import TextButton
from findsbot.keyboards.default.Cancel import cancel
from findsbot.keyboards.default.main_menus import main_menu
from findsbot.keyboards.inline import CreatingReview
from findsbot.loader import dp, bot
from findsbot.states.NewReview import NewReview
from findsbot.utils.dp_api.commands import get_name, add_new_review


@dp.message_handler(TextButton("button_create_review"))
async def create_new_review(message: types.Message, state: FSMContext):
    markup = await cancel()
    msgs = []
    msg = await message.answer(text=await get_name("new_review_text"), reply_markup=markup)
    msgs.append(msg.message_id)
    msg = await message.answer(text=await get_name("choose_answer_review_text"), reply_markup=CreatingReview.markup)
    msgs.append(msg.message_id)
    await NewReview.AskQuestion.set()
    await state.update_data(msgs=msgs)


@dp.message_handler(TextButton("button_cancel_text"), state=NewReview)
async def cancel_creating_review(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    msgs = data.get("msgs")
    if msgs:
        for msg in msgs:
            try:
                await bot.delete_message(chat_id=types.User.get_current().id, message_id=msg)
            except Exception:
                pass
    markup = await main_menu()
    await message.answer(text=await get_name("menu_text"), reply_markup=markup)


@dp.message_handler(state=NewReview.EnterCaption, content_types=types.ContentType.TEXT)
async def enter_caption_review(message: types.Message, state: FSMContext):
    caption = message.text
    await add_new_review(caption)
    markup = await main_menu()
    await message.answer(text=await get_name("thks_for_review_text"), reply_markup=markup)
    await state.reset_state()


@dp.callback_query_handler(state=NewReview.AskQuestion, text_contains="no_review")
async def choose_category(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msgs = data.get("msgs")
    msg = await call.message.answer(text=await get_name("negative_review_text"))
    msgs.append(msg.message_id)
    await call.message.delete()
    await NewReview.EnterCaption.set()
    await state.update_data(msgs=msgs)


@dp.callback_query_handler(state=NewReview.AskQuestion, text_contains="yes_review")
async def choose_category(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msgs = data.get("msgs")
    msg = await call.message.answer(text=await get_name("positive_review_text"))
    msgs.append(msg.message_id)
    await call.message.delete()
    await NewReview.EnterCaption.set()
    await state.update_data(msgs=msgs)
