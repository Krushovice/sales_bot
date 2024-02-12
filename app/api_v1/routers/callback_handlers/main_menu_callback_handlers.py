from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.api_v1.core.crud import AsyncOrm

from app.api_v1.markups import MenuActions, MenuCbData
from app.api_v1.markups import build_account_kb


router = Router(name=__name__)


@router.callback_query(MenuCbData.filter(F.action == MenuActions.account))
async def handle_account_button(call: CallbackQuery):
    await call.answer()
    user = await AsyncOrm.get_user(
        tg_id=call.from_user.id,
    )
    print(call.data)
    await call.message.edit_text(
        text=(
            f"<b>Личный кабинет</b>\n\n"
            f"🆔 {user.tg_id} \n"
            f"💰 Баланс: {user.balance}руб\n\n"
            f"<i>Для оплаты и продления VPN используется баланс.\n</i>"
            f"<i>Для его пополнения используйте клавиши ниже</i>"
        ),
        reply_markup=build_account_kb(),
    )
