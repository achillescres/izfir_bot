from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text

from bot.keyboards.default.menu import menu_kb
from bot.keyboards.default.questions import questions_menu_kb, nlp_kb
from bot.nlp import hook_answer
from bot.states import MenuFSM, NlpFSM

from loader import dp


@dp.message_handler(text=questions_menu_kb.Texts.nlp.value, state=MenuFSM.main)
async def nlp_qu_activate(message: types.Message, state: FSMContext):
    await message.answer(
        'Напишите свой вопрос, попытайтесь максимально упростить его, оставив при этом смысл',
        reply_markup=menu_kb.return_kb
    )

    await state.set_state(NlpFSM.writing)


@dp.message_handler(state=NlpFSM.writing)
async def nlp_qu_apply(message: types.Message, state: FSMContext):
    await message.reply(
        'Вы уверены в корректности вопроса?',
        reply_markup=nlp_kb.kb
    )

    await state.update_data(question=message)
    await state.set_state(NlpFSM.apply)


@dp.message_handler(text=nlp_kb.Texts.apply.value, state=NlpFSM.apply)
async def nlp_qu_apllied(message: types.Message, state: FSMContext):
    waiting = await message.answer('Обрабатываю ваш вопрос...')
    ans = hook_answer(message.text)
    if ans == 'err':
        ans = 'По каким-то причинам я не смог обработать ваш вопрос, извините'

    await waiting.delete()
    await (await state.get_data())['question'].reply(
        text(ans),
        reply_markup=menu_kb.kb
    )
    await state.update_data(question=None)
    await state.set_state(MenuFSM.main)


@dp.message_handler(text=nlp_kb.Texts.cancel.value, state=NlpFSM.apply)
async def nlp_qu_cancel(message: types.Message, state: FSMContext):
    await message.answer(
        'Напишите свой вопрос, попытайтесь максимально упростить его, оставив при этом смысл',
        reply_markup=menu_kb.return_kb
    )

    await state.set_state(NlpFSM.writing)
