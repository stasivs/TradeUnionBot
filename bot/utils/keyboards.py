from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from utils import check_role

BUTTON_GET_INFO = KeyboardButton("Поиск по базе данных")
BUTTON_PROF_ID = KeyboardButton("Проф карта")
BUTTON_STUD_NUMBER = KeyboardButton("Студенческий билет")
BUTTON_SURNAME = KeyboardButton("Фамилия студента")
BUTTON_NAME = KeyboardButton("Имя студента")
BUTTON_SECOND_NAME = KeyboardButton("Отчество студента")
BUTTON_FIO = KeyboardButton("ФИО студента")
BUTTON_REASON = KeyboardButton("Причина мат помощи")
BUTTON_ROLE = KeyboardButton("Роль пользователя")
BUTTON_TG_ID = KeyboardButton("Телеграм ID")
BUTTON_COMMENT = KeyboardButton("Комментарий")
BUTTON_FINANCING_FORM = KeyboardButton("Форма финансирования")
BUTTON_IKG = KeyboardButton("ИКГ")
BUTTON_YES = KeyboardButton("Да")
BUTTON_NO = KeyboardButton("Нет")
BUTTON_USER = KeyboardButton("User")
BUTTON_ADMIN = KeyboardButton("Admin")
BUTTON_SUPERADMIN = KeyboardButton("SuperAdmin")
BUTTON_BUDGET = KeyboardButton("бюджет")
BUTTON_CONTRACT = KeyboardButton("контракт")

BUTTON_GET_PROFCOME_SCHEDULE = KeyboardButton("Узнать расписание приёма документов")
BUTTON_GET_PROF_ID = KeyboardButton("Узнать номер своей профкарты")
BUTTON_GET_MAT_HELP_DOCS = KeyboardButton("Материальная помощь - перечень документов")
BUTTON_GET_MAT_SUPPORT_DOCS = KeyboardButton(
    "Материальная поддержка - перечень документов"
)
BUTTON_FAQ = KeyboardButton("Часто задаваемые вопросы")
BUTTON_REGISTRATION = KeyboardButton("Регистрация")

BUTTON_IPGS = KeyboardButton("ИПГС")
BUTTON_IAG = KeyboardButton("ИАГ")
BUTTON_IGES = KeyboardButton("ИГЭС")
BUTTON_IIESM = KeyboardButton("ИИЭСМ")
BUTTON_IEUKSN = KeyboardButton("ИЭУКСН")
BUTTON_ICTMS = KeyboardButton("ИЦТМС")
BUTTON_MF = KeyboardButton("МФ")

BUTTON_TO_MAIN_MENU = KeyboardButton("В главное меню")
BUTTON_CANCEL = KeyboardButton("Отмена")

BUTTON_DORMITORY_STUDENT = KeyboardButton("Проживание в общежитии")
BUTTON_NOTFULL_FAMILY = KeyboardButton("Неполная семья")
BUTTON_PENSIONER_PARENTS = KeyboardButton("Родители пенсионеры/инвалиды")
BUTTON_DISPANCER_RECORD = KeyboardButton("Диспансерный учёт")
BUTTON_INVALID_STUDENT = KeyboardButton("Инвалидность")
BUTTON_CHERNOBYL_STUDENT = KeyboardButton("Студенты - чернобыльцы")
BUTTON_MILITARY_INJURED = KeyboardButton("Инвалиды вследствие военной травмы")
BUTTON_HAVING_CHILDREN_STUDENT = KeyboardButton("Студенты, имеющие детей")
BUTTON_ORPHAN_STUDENT = KeyboardButton("Студент - сирота")
BUTTON_LARGE_FAMILY = KeyboardButton("Многодетная семья")
BUTTON_MILITARY_STUDENT = KeyboardButton("Студенты - участники боевых действий")
BUTTON_MARRIED_STUDENT = KeyboardButton("Заключение брака")
BUTTON_PREGNANT_STUDENT = KeyboardButton("Беременность")
BUTTON_NEEDY_FAMILY = KeyboardButton("Малоимущая семья")
BUTTON_HEAVY_DISEASE = KeyboardButton("Тяжёлое заболевание")
BUTTON_RELATIVE_LOST = KeyboardButton("Потеря близкого родственника")
BUTTON_EMERGENCY_SITUATION = KeyboardButton("Чрезвычайная ситуация")
BUTTON_PARENTS_LOST = KeyboardButton("Потеря родителей")

BUTTON_WHAT_IS_MATHELP = KeyboardButton("Что такое материальная помощь?")
BUTTON_WHAT_IS_MATSUPPORT = KeyboardButton("Что такое материальная поддержка?")
BUTTON_WHAT_IS_SOCSTIP = KeyboardButton("Что такое социальная стипендия?")
BUTTON_HOW_GET_SOCSTIP = KeyboardButton("Как получить социальную стипендию?")
BUTTON_HOW_PAY_PROFVZNOS = KeyboardButton("Где и как оплатить профвзнос?")
BUTTON_HOW_TO_APPLY_FOR_MATHELP = KeyboardButton("Как подать на материальную помощь?")
BUTTON_HOW_TO_APPLY_FOR_MATSUPPORT = KeyboardButton(
    "Как подать на материальную поддержку?"
)
BUTTON_PROFCOME_TIME = KeyboardButton("Часы работы профкома")
BUTTON_NOT_FOUND_ANSWER = KeyboardButton("Не нашёл ответ на интересующий вопрос")

INLINE_BUTTON_INN = InlineKeyboardButton(
    text="Узнать свой ИНН", url="https://service.nalog.ru/inn.do"
)
INLINE_BUTTON_MAT_HELP_BLANK = InlineKeyboardButton(
    text="Бланк заявления", callback_data="get_mat_help_blank"
)
INLINE_BUTTON_MAT_SUPPORT_BLANK = InlineKeyboardButton(
    text="Бланк заявления", callback_data="get_mat_support_blank"
)
INLINE_BUTTON_GET_PROFCOME_SCHEDULE = InlineKeyboardButton(
    text="Расписание приёма документов", callback_data="get_profcome_schedule"
)

INLINE_BUTTON_VK_GROUP = InlineKeyboardButton(
    text="Наша группа ВК", url="https://vk.com/pk_mgsu"
)

ADMIN_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
CHANGE_POLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INFO_POLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
APPROVAL_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
ROLE_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
FINANCING_FORM_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

STUDENT_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)
INSTITUTE_NAME_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

CANCEL_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

REGISTRATION_KEYBOARD = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)

MAT_HELP_REASONS_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

MAT_SUPPORT_REASONS_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

QUESTIONS_KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True)

MATHELP_DOCS_INLINE_KEYBOARD = InlineKeyboardMarkup()

MATSUPPORT_DOCS_INLINE_KEYBOARD = InlineKeyboardMarkup()

VK_GROUP_INLINE_KEYBOARD = InlineKeyboardMarkup()

ADMIN_KEYBOARD.add(BUTTON_GET_INFO)

CHANGE_POLE_KEYBOARD.add(BUTTON_PROF_ID).add(BUTTON_STUD_NUMBER).add(BUTTON_ROLE).add(BUTTON_TG_ID) \
    .add(BUTTON_COMMENT).add(BUTTON_SURNAME).add(BUTTON_NAME).add(BUTTON_SECOND_NAME).add(BUTTON_IKG) \
    .add(BUTTON_FINANCING_FORM).add(BUTTON_TO_MAIN_MENU)

INFO_POLE_KEYBOARD.add(BUTTON_SURNAME).add(BUTTON_FIO).add(BUTTON_PROF_ID).add(BUTTON_STUD_NUMBER) \
    .add(BUTTON_TO_MAIN_MENU)

ROLE_KEYBOARD.add(BUTTON_USER).add(BUTTON_ADMIN).add(BUTTON_SUPERADMIN).add(BUTTON_CANCEL)

FINANCING_FORM_KEYBOARD.add(BUTTON_BUDGET).add(BUTTON_CONTRACT).add(BUTTON_CANCEL)

APPROVAL_KEYBOARD.add(BUTTON_YES).insert(BUTTON_NO)

STUDENT_KEYBOARD.add(BUTTON_GET_MAT_HELP_DOCS).add(BUTTON_GET_MAT_SUPPORT_DOCS) \
    .add(BUTTON_GET_PROF_ID).add(BUTTON_GET_PROFCOME_SCHEDULE).add(BUTTON_FAQ)

INSTITUTE_NAME_KEYBOARD.add(BUTTON_IPGS).insert(BUTTON_IAG).add(BUTTON_IGES).insert(BUTTON_IIESM) \
    .add(BUTTON_IEUKSN).insert(BUTTON_ICTMS).add(BUTTON_MF).insert(BUTTON_TO_MAIN_MENU)

MAT_HELP_REASONS_KEYBOARD.add(BUTTON_DORMITORY_STUDENT).insert(BUTTON_PENSIONER_PARENTS).add(BUTTON_DISPANCER_RECORD) \
    .insert(BUTTON_INVALID_STUDENT).add(BUTTON_CHERNOBYL_STUDENT).insert(BUTTON_HAVING_CHILDREN_STUDENT) \
    .add(BUTTON_ORPHAN_STUDENT).insert(BUTTON_LARGE_FAMILY).add(BUTTON_MILITARY_STUDENT) \
    .insert(BUTTON_PREGNANT_STUDENT).add(BUTTON_MARRIED_STUDENT).insert(BUTTON_HEAVY_DISEASE) \
    .add(BUTTON_MILITARY_INJURED).insert(BUTTON_EMERGENCY_SITUATION).add(BUTTON_NEEDY_FAMILY) \
    .insert(BUTTON_NOTFULL_FAMILY).add(BUTTON_RELATIVE_LOST).insert(BUTTON_PARENTS_LOST).add(BUTTON_TO_MAIN_MENU)

MAT_SUPPORT_REASONS_KEYBOARD.add(BUTTON_NOTFULL_FAMILY).insert(BUTTON_PENSIONER_PARENTS).add(BUTTON_DISPANCER_RECORD) \
    .insert(BUTTON_INVALID_STUDENT).add(BUTTON_CHERNOBYL_STUDENT).insert(BUTTON_HAVING_CHILDREN_STUDENT) \
    .add(BUTTON_ORPHAN_STUDENT).insert(BUTTON_LARGE_FAMILY).add(BUTTON_MILITARY_STUDENT).insert(BUTTON_TO_MAIN_MENU)

QUESTIONS_KEYBOARD.add(BUTTON_WHAT_IS_MATHELP).add(BUTTON_HOW_TO_APPLY_FOR_MATHELP) \
    .add(BUTTON_WHAT_IS_MATSUPPORT).add(BUTTON_HOW_TO_APPLY_FOR_MATSUPPORT).add(BUTTON_WHAT_IS_SOCSTIP) \
    .add(BUTTON_HOW_GET_SOCSTIP).add(BUTTON_HOW_PAY_PROFVZNOS).add(BUTTON_PROFCOME_TIME).add(BUTTON_NOT_FOUND_ANSWER) \
    .add(BUTTON_TO_MAIN_MENU)

CANCEL_KEYBOARD.add(BUTTON_CANCEL)

REGISTRATION_KEYBOARD.add(BUTTON_REGISTRATION)

MATHELP_DOCS_INLINE_KEYBOARD.add(INLINE_BUTTON_INN).add(INLINE_BUTTON_MAT_HELP_BLANK) \
    .add(INLINE_BUTTON_GET_PROFCOME_SCHEDULE)

MATSUPPORT_DOCS_INLINE_KEYBOARD.add(INLINE_BUTTON_INN).add(INLINE_BUTTON_MAT_SUPPORT_BLANK)

VK_GROUP_INLINE_KEYBOARD.add(INLINE_BUTTON_VK_GROUP)


async def keyboard_choice(user_id: int) -> ReplyKeyboardMarkup:
    if await check_role.check_student_role(user_id) == "SuperAdmin":
        return ADMIN_KEYBOARD

    elif await check_role.check_student_role(user_id) == "Admin":
        return ADMIN_KEYBOARD

    elif await check_role.check_student_role(user_id) == "User":
        return STUDENT_KEYBOARD

    else:
        return REGISTRATION_KEYBOARD


async def inline_keyboard_choice(
        user_id: int, student_bd_id: int, telegram_id: str | None
) -> InlineKeyboardMarkup:
    redact_keyboard = InlineKeyboardMarkup()

    if await check_role.check_student_role(user_id) == "SuperAdmin":
        if telegram_id:
            button_redact = InlineKeyboardButton(
                text="Редактировать",
                callback_data=f"redact {student_bd_id} {telegram_id}",
            )
        else:
            button_redact = InlineKeyboardButton(
                text="Редактировать", callback_data=f"redact {student_bd_id}"
            )

        redact_keyboard.add(button_redact)

    else:
        redact_keyboard.add()

    return redact_keyboard
