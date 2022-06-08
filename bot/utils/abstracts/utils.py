from aiogram import types


def get_message_from_obj(obj: types.Message | types.CallbackQuery):
    return obj.message if isinstance(obj, types.CallbackQuery) else obj