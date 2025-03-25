from typing import Optional
from aiogram.filters.callback_data import CallbackData


class BalanceManageCallback(CallbackData, prefix="balance"):
    action: Optional[str] = None  # choose_way, choose_sum, check_withd, choose_other, bet_other, check_topup,
    # confirm_withd, check_bet, change_bet, create_bet, create_request, enter_requisites, choose_bet, get_statistics
    role: Optional[str] = None  # user, admin
    operation: Optional[str] = None  # topup, withd, bet, rem, add, set
    game: Optional[str] = None  # bowl, cube, slot, duel, russ, king
    way: Optional[str] = None  # qiwi, bank
    sum: Optional[int] = None
    from_where: Optional[str] = None  # main
    id_msg: Optional[str] = None
    id_oper: Optional[str] = None
    requisites: Optional[str] = None


class AdminManageCallback(CallbackData, prefix="admin"):
    user_id: Optional[str] = None
    user_nickname: Optional[str] = None
    action: Optional[str] = None  # open_main, check_oper, confirm_oper, choose_type, select_oper, change_balance,
    # user_info, oper_info, user_balance, choose_user, check_ban, ban_user, change_way, change_requisites,
    # new_requisites, user_checker, choose_admin, admin_info, admin_list, add_admin
    sum: Optional[int] = None
    key: Optional[str] = None
    from_where: Optional[str] = None
    id_oper: Optional[int] = None
    operation: Optional[str] = None
    old_way: Optional[str] = None
    new_way: Optional[str] = None
    new_requisites: Optional[str] = None
