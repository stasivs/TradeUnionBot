from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_run import bot
from utils import keyboards, request_funcs
from utils.lang_parser import get_phrase


class GetProfcomeScheduleFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о студенте."""
    waiting_institute_name = State()


async def get_profcome_schedule(message: types.Message) -> None:
    """Отлавливает команду о предоставлении расписания, запускает соответствующий диалог."""

    await bot.send_message(message.from_user.id, get_phrase('choose_institute_name'),
                           reply_markup=keyboards.INSTITUTE_NAME_KEYBOARD)
    await GetProfcomeScheduleFSM.waiting_institute_name.set()


async def obtain_institute_name(message: types.Message, state: FSMContext) -> None:
    """Отлавливает имя института и выдаёт соответствующее расписание."""

    response = await request_funcs.get_profcome_schedule(message.text)

    if response:
        await bot.send_photo(message.from_user.id, response['timetable'],
                             reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    else:
        await bot.send_message(message.from_user.id, get_phrase('schedule_not_available'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


async def get_prof_id(message: types.Message) -> None:
    """Отлавливает команду о предоставлении номера профкарты, используя id пользователя
    вызывает соответствующую функцию обращения к серверу."""

    stud_info = await request_funcs.get_student_info('Телеграм ID', message.from_user.id)

    if isinstance(stud_info, list):
        prof_id = stud_info[0]['profcard']
        await bot.send_message(message.from_user.id, get_phrase('profcard_output', prof_id),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    else:
        await bot.send_message(message.from_user.id, get_phrase('registration_require'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))


class GetDocsInfoFSM(StatesGroup):
    """Машина состояний - диалог предоставления ин-фы о причинах мат помощи."""
    waiting_reason_name = State()


async def get_docs_info(message: types.Message) -> None:
    """ Отлавливает команду о предоставлении документов, запускает соответствующий диалог. """

    await bot.send_message(message.from_user.id, get_phrase('choose_reason_name'),
                           reply_markup=keyboards.REASONS_KEYBOARD)
    await GetDocsInfoFSM.waiting_reason_name.set()


async def obtain_reason_name(message: types.Message, state: FSMContext) -> None:
    """ Отлавливает название причины, и выдаёт список соответствующих документов. """

    reasons_docs_dict = {
        'Проживание в общежитие': 'dormitory_student_docs',
        'Неполная семья': 'notfull_family_docs',
        'Родители пенсионеры/инвалиды': 'pensioner_parents_docs',
        'Диспансерный учёт': 'dispancer_record_docs',
        'Инвалидность': 'invalid_student_docs',
        'Студенты - чернобыльцы': 'chernobyl_student_docs',
        'Студенты, имеющие детей': 'having_children_student_docs',
        'Студент - сирота': 'orphan_student_docs',
        'Многодетная семья': 'large_family_docs',
        'Студенты - участники боевых действий': 'military_student_docs',
        'Инвалиды вследствие военной травмы': 'military_injured_docs',
        'Заключение брака': 'married_student_docs',
        'Беременность': 'pregnant_student_docs',
        'Малоимущая семья': 'needy_family_docs',
        'Тяжёлое заболевание': 'heavy_disease_docs',
        'Чрезвычайная ситуация': 'emergency_situation_docs'
    }

    try:
        phrase = reasons_docs_dict[message.text]

        await bot.send_message(message.from_user.id, get_phrase(phrase),
                               reply_markup=keyboards.MATHELP_DOCS_INLINE_KEYBOARD)

        await bot.send_message(message.from_user.id, get_phrase('good_luck'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    except KeyError:
        await bot.send_message(message.from_user.id, get_phrase('not_such_reason'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


async def send_blank(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """ Отлавливает нажатие инлайн кнопки и отправляет бланк заявления. """

    try:
        with open('/bot/sources/Blank_zayavlenia_na_MP.pdf', 'rb') as f:
            await bot.send_document(callback_query.from_user.id, document=f)

    except FileNotFoundError:
        await bot.send_message(callback_query.from_user.id, get_phrase('file_not_found'))


class FrAskQuestFSM(StatesGroup):
    """Машина состояний - диалог предоставления FAQ."""
    waiting_question_name = State()


async def fr_ask_quest(message: types.Message) -> None:
    """ Отлавливает команду о предоставлении FAQ, запускает соответствующий диалог. """

    await bot.send_message(message.from_user.id, get_phrase('choose_question_name'),
                           reply_markup=keyboards.QUESTIONS_KEYBOARD)
    await FrAskQuestFSM.waiting_question_name.set()


async def obtain_question_name(message: types.Message, state: FSMContext) -> None:
    """ Отлавливает название причины, и выдаёт список соответствующих документов. """

    reasons_docs_dict = {
        'Что такое материальная помощь?': 'what_is_mathelp_answer',
        'Что такое материальная поддержка?': 'what_is_matsupport_answer',
        'Что такое социальная стипендия?': 'what_is_socstip_answer',
        'Как получить социальную стипендию?': 'how_get_socstip_answer',
        'Где и как оплатить профвзнос?': 'how_pay_profvznos_answer',
        'Что такое ИКГ?': 'what_is_ikg_answer',
        'Если человек меняет паспорт, он может подавать на мат.помощь?': 'change_pass_question_answer',
        'Часы работы профкома.': 'profcome_time_answer'
    }

    try:
        phrase = reasons_docs_dict[message.text]

        await bot.send_message(message.from_user.id, get_phrase(phrase),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    except KeyError:
        await bot.send_message(message.from_user.id, get_phrase('not_such_question'),
                               reply_markup=await keyboards.keyboard_choice(message.from_user.id))

    await state.finish()


def register_student_handlers(dp: Dispatcher) -> None:
    """Регистрация студенческих хендлеров."""
    dp.register_callback_query_handler(send_blank, lambda x: x.data and x.data == 'get_blank',
                                       state='*')
    dp.register_message_handler(get_profcome_schedule, text=['Узнать расписание приёма документов'], state=None)
    dp.register_message_handler(obtain_institute_name, content_types=['text'],
                                state=GetProfcomeScheduleFSM.waiting_institute_name)
    dp.register_message_handler(get_prof_id, text=['Узнать номер своей профкарты'])
    dp.register_message_handler(get_docs_info, text=['Узнать список документов для получения материальной помощи'])
    dp.register_message_handler(obtain_reason_name, content_types=['text'], state=GetDocsInfoFSM.waiting_reason_name)
    dp.register_message_handler(fr_ask_quest, text=['Часто задаваемые вопросы'])
    dp.register_message_handler(obtain_question_name, content_types=['text'], state=FrAskQuestFSM.waiting_question_name)
