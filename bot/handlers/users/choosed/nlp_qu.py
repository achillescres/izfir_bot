from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import text

from bot.keyboards.default import main_kb, nlp_qu_kb
from bot.nlp import hook_answer
from bot.states import MainFSM, NlpFSM

from loader import dp


@dp.message_handler(text=main_kb.Texts.nlp_qus.value, state=MainFSM.choosed)
async def nlp_qu_activate(message: types.Message, state: FSMContext):
    await message.answer(
        'Напишите свой вопрос, попытайтесь максимально упростить его, оставив при этом смысл',
        reply_markup=main_kb.return_ikb
    )

    await state.set_state(NlpFSM.writing)


@dp.message_handler(state=NlpFSM.writing)
async def nlp_qu_apply(message: types.Message, state: FSMContext):
    await message.reply(
        'Вы уверены в корректности вопроса?',
        reply_markup=nlp_qu_kb.kb
    )

    await state.set_state(NlpFSM.apply)


@dp.message_handler(text=nlp_qu_kb.Texts.apply.value, state=NlpFSM.apply)
async def nlp_qu_apllied(message: types.Message, state: FSMContext):
    waiting = await message.answer('Обрабатываю ваш вопрос...')
    ans = hook_answer(message.text)
    if ans == 'err':
        ans = 'По каким-то причинам я не смог обработать ваш вопрос, извините'

    await waiting.delete()
    await message.reply(
        text(ans),
        reply_markup=main_kb.kb
    )
    await state.set_state(MainFSM.choosed)


@dp.message_handler(text=nlp_qu_kb.Texts.cancel.value, state=NlpFSM.apply)
async def nlp_qu_cancel(message: types.Message, state: FSMContext):
    await message.answer(
        'Напишите свой вопрос, попытайтесь максимально упростить его, оставив при этом смысл',
        reply_markup=main_kb.return_ikb
    )

    await state.set_state(NlpFSM.writing)
