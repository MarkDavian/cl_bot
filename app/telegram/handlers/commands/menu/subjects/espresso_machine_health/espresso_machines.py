import uuid
import asyncio
from bson import ObjectId
from datetime import datetime

from typing import Dict, Any, Optional

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from app.telegram.handlers.states import EmployeesSG
from app.core.types.espresso_machine import EspressoMachine 
from app.core.db.espresso_machines import EspressoMachinesDB
from app.core.funcs.correct_date import date_incorrect

from app.telegram.handlers.commands.menu.common import MenuCallbackData
from .common import EspressoCallbackData


class AsyncCallbackStore:
    """
    Асинхронное безопасное хранилище для временных данных callback.
    Поддерживает операции get, set, update, delete и delete_all.
    Потокобезопасно с использованием асинхронной блокировки.
    """
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()  # Асинхронная блокировка
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Получает данные по ключу.
        
        Args:
            key: Ключ для поиска данных
            
        Returns:
            Словарь с данными или None, если ключ не найден
        """
        async with self._lock:
            return self._store.get(key, None)
    
    async def set(self, key: str, value: Dict[str, Any]) -> str:
        """
        Устанавливает данные для ключа.
        
        Args:
            key: Ключ для сохранения данных
            value: Данные для сохранения
            
        Returns:
            Используемый ключ (полезно при генерации случайных ключей)
        """
        async with self._lock:
            self._store[key] = value
            return key
    
    async def update(self, key: str, value: Dict[str, Any]) -> bool:
        """
        Обновляет существующие данные для ключа.
        
        Args:
            key: Ключ для обновления данных
            value: Новые данные или данные для обновления
            
        Returns:
            True если обновление успешно, False если ключ не найден
        """
        async with self._lock:
            if key in self._store:
                self._store[key].update(value)
                return True
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Удаляет данные по ключу.
        
        Args:
            key: Ключ для удаления
            
        Returns:
            True если удаление успешно, False если ключ не найден
        """
        async with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False
    
    async def delete_all(self) -> int:
        """
        Удаляет все данные из хранилища.
        
        Returns:
            Количество удаленных элементов
        """
        async with self._lock:
            count = len(self._store)
            self._store.clear()
            return count
    
    async def __len__(self) -> int:
        """Возвращает количество хранимых элементов"""
        async with self._lock:
            return len(self._store)
    
    async def contains(self, key: str) -> bool:
        """Проверяет наличие ключа в хранилище"""
        async with self._lock:
            return key in self._store

    @classmethod
    def _get_random_key(cls, size: int = 8) -> str:
        """Генерирует случайный ключ для хранилища"""
        return str(uuid.uuid4())[:size]    


# Создаем глобальный экземпляр хранилища
CALLBACK_STORE = AsyncCallbackStore()


async def show_machines(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.Menu.state)
    
    with EspressoMachinesDB() as db:
        machines = db.get_all_machines()
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    # Добавляем кнопку для добавления новой машины
    keyboard.add(types.InlineKeyboardButton(
        "Добавить кофемашину",
        callback_data=EspressoCallbackData(
            action="add_machine"
        ).pack()
    ))
    
    # Добавляем кнопки для каждой машины
    for machine in machines:
        key = CALLBACK_STORE._get_random_key()
        await CALLBACK_STORE.set(key, {"machine_id": machine.id})
        keyboard.add(types.InlineKeyboardButton(
            f"{machine.location}",
            callback_data=EspressoCallbackData(
                action="view_machine",
                key=key
            ).pack()
        ))
    
    # Добавляем кнопку "Назад"
    keyboard.add(types.InlineKeyboardButton(
        "⬅️ Назад",
        callback_data=MenuCallbackData(action="espresso_health").hash()
    ))
    
    await callback.message.edit_text(
        "☕️ Управление кофемашинами\n\n"
        f"Всего машин: {len(machines)}",
        reply_markup=keyboard
    )

async def view_machine(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.Details.state)
    
    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key
    
    data = await CALLBACK_STORE.get(key)
    if not data:
        await callback.message.edit_text("Кофемашина не найдена")
        return
    
    machine_id = data["machine_id"]
    
    with EspressoMachinesDB() as db:
        machine = db.get_machine(machine_id)
    
    if not machine:
        await callback.message.edit_text("Кофемашина не найдена")
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    # Добавляем кнопки для действий с машиной
    keyboard.row(types.InlineKeyboardButton(
        "Добавить обслуживание",
        callback_data=EspressoCallbackData(
            action="add_service",
            key=key
        ).pack()),
        types.InlineKeyboardButton(
        "История обслуживания",
        callback_data=EspressoCallbackData(
            action="history_service",
            key=key
        ).pack()
    ))
    
    keyboard.add(types.InlineKeyboardButton(
        "Обновить замену резинок",
        callback_data=EspressoCallbackData(
            action="update_gasket",
            key=key
        ).pack()
    ))
    
    keyboard.add(types.InlineKeyboardButton(
        "Удалить кофемашину",
        callback_data=EspressoCallbackData(
            action="delete_machine",
            key=key
        ).pack()
    ))
    
    keyboard.add(types.InlineKeyboardButton(
        "Назад к списку",
        callback_data=EspressoCallbackData(
            action="back_to_list",
            key=key
        ).pack()
    ))
    
    # Формируем текст с информацией о машине
    text = (
        f"☕️ Кофемашина {machine.model}\n"
        f"📍 Местоположение: {machine.location}\n\n"
        f"📅 Последняя замена резинок: {machine.last_gasket_replacement}\n"
        f"📅 Следующая замена резинок: {machine.next_gasket_replacement}\n\n"
        "📋 История обслуживания:\n"
    )
    
    # Сортируем даты обслуживания в хронологическом порядке
    sorted_service_dates = sorted(machine.service_dates, 
                                 key=lambda x: datetime.strptime(x.date, '%d.%m.%Y'))
    if len(sorted_service_dates) > 3:
        old_dates = sorted_service_dates[:-3]
        # Оставляем только последние 3 даты
        sorted_service_dates = sorted_service_dates[-3:]
        text += f"И еще {len(old_dates)} записей...\n"

    for service in sorted_service_dates:
        text += f"- {service.date}: {service.description}\n"
    
    await callback.message.edit_text(text, reply_markup=keyboard)


async def add_machine_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.Add.Location)

    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "⬅️ Отмена",
        callback_data=EspressoCallbackData(
            action="cancel_add",
            key=key
        ).pack()
    ))
    
    await callback.message.edit_text(
        "Введите местоположение кофемашины (фили, пресня, пруд, соко):",
        reply_markup=keyboard
    )


async def add_machine_location(message: types.Message, state: FSMContext):
    location = message.text.lower()
    if location not in ["фили", "пресня", "пруд", "соко"]:
        await message.reply(
            "❌ Неверное местоположение. Используйте: фили, пресня, пруд или соко"
        )
        return
    
    await state.update_data(location=location)
    
    await message.reply(
        "Введите модель кофемашины:"
    )
    await state.set_state(EmployeesSG.Espresso.Add.Model)


async def add_machine_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    
    data = await state.get_data()
    
    # Создаем новую кофемашину
    new_machine = EspressoMachine(
        id=str(ObjectId()),
        location=data["location"],
        model=data["model"],
        service_dates=[],
        last_gasket_replacement="",
        next_gasket_replacement=""
    )
    
    # Добавляем машину в базу
    with EspressoMachinesDB() as db:
        db.add(new_machine)
    
    # Возвращаемся к списку машин
    await state.set_state(EmployeesSG.Espresso.Menu.state)
    
    with EspressoMachinesDB() as db:
        machines = db.get_all_machines()
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Добавить кофемашину",
        callback_data=EspressoCallbackData(
            action="add_machine"
        ).pack()
    ))
    
    # Добавляем кнопки для каждой машины
    for machine in machines:
        key = CALLBACK_STORE._get_random_key()
        await CALLBACK_STORE.set(key, {"machine_id": machine.id})
        keyboard.add(types.InlineKeyboardButton(
            f"{machine.location}",
            callback_data=EspressoCallbackData(
                action="view_machine",
                key=key
            ).pack()
        ))
    
    keyboard.add(types.InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="back"
    ))
    
    await message.reply(
        f"✅ Кофемашина успешно добавлена!\n\n"
        f"☕️ Управление кофемашинами\n\n"
        f"Всего машин: {len(machines)}",
        reply_markup=keyboard
    )


async def add_service_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.Add.ServiceDate)
    
    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key

    data = await CALLBACK_STORE.get(key)
    machine_id = data["machine_id"]
    
    await state.update_data(machine_id=machine_id, key=key)
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "⬅️ Отмена",
        callback_data=EspressoCallbackData(
            action="cancel_add",
            key=key
        ).pack()
    ))
    
    await callback.message.edit_text(
        "Введите дату обслуживания в формате ДД.ММ.ГГГГ:",
        reply_markup=keyboard
    )


async def add_service_date(message: types.Message, state: FSMContext):
    if date_incorrect(message.text):
        await message.reply(
            "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ\n"
            "Например: 01.01.2024"
        )
        return
    
    await state.update_data(service_date=message.text)
    
    await message.reply(
        "Введите описание обслуживания:"
    )
    await state.set_state(EmployeesSG.Espresso.Add.ServiceDescription)


async def add_service_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    key = data['key']

    with EspressoMachinesDB() as db:
        machine = db.get_machine(data["machine_id"])
    
    if not machine:
        await message.reply("Кофемашина не найдена")
        return
    
    # Добавляем новое обслуживание
    machine.add_service_date(
        date=data["service_date"], 
        description=message.text,
        authorized=message.from_user.id
    )
    with EspressoMachinesDB() as db:
        db.update_machine(machine)
    
    # Возвращаемся к просмотру машины
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "⬅️ Назад к кофемашине",
        callback_data=EspressoCallbackData(
            action="view_machine",
            key=key
        ).pack()
    ))
    await message.reply(
        "✅ Обслуживание добавлено",
        reply_markup=keyboard
    )


async def update_gasket_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.Update.GasketDate)
    
    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key
    data = await CALLBACK_STORE.get(key)
    machine_id = data["machine_id"]

    await state.update_data(machine_id=machine_id, key=key)
    
    cancel_keyboard = types.InlineKeyboardMarkup(row_width=1)
    cancel_keyboard.add(types.InlineKeyboardButton(
        "⬅️ Отмена",
        callback_data=EspressoCallbackData(
            action="cancel_update",
            key=key
        ).pack()
    ))
    now_date = datetime.now().strftime("%d.%m.%Y")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(now_date))

    await callback.message.edit_text(
        "Обновим дату замены резинок",
        reply_markup=cancel_keyboard
    )

    await callback.message.reply(
        "Введите дату замены резинок в формате ДД.ММ.ГГГГ:",
        reply_markup=keyboard
    )

async def update_gasket_date(message: types.Message, state: FSMContext):
    if date_incorrect(message.text):
        await message.reply(
            "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ\n"
            "Например: 01.01.2024"
        )
        return
    
    data = await state.get_data()
    with EspressoMachinesDB() as db:
        machine = db.get_machine(data["machine_id"])
    
    if not machine:
        await message.reply("Кофемашина не найдена", reply_markup=types.ReplyKeyboardRemove())
        return
    
    # Обновляем дату замены резинок
    machine.update_gasket_replacement(message.text)
    with EspressoMachinesDB() as db:
        db.update_machine(machine)
    
    # Возвращаемся к просмотру машины
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "⬅ Вернуться",
        callback_data=EspressoCallbackData(
            action="view_machine",
            key=data["key"]
        ).pack()
    ))
    await message.reply(
        "✅ Дата замены резинок обновлена",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await message.reply(
        f"⬅️ Вернуться к кофемашине ({machine.location})?",
        reply_markup=keyboard
    )

async def delete_machine_confirm(callback: types.CallbackQuery, state: FSMContext):
    callback_data = EspressoCallbackData.unpack(callback.data)
    data = await CALLBACK_STORE.get(callback_data.key)
    machine_id = data["machine_id"]
    key = callback_data.key

    with EspressoMachinesDB() as db:
        machine = db.get_machine(machine_id)
    
    if not machine:
        await callback.message.edit_text("Кофемашина не найдена")
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "Да, удалить",
        callback_data=EspressoCallbackData(
            action="confirm_delete",
            key=key
        ).pack()
    ))
    keyboard.add(types.InlineKeyboardButton(
        "⬅️ Отмена",
        callback_data=EspressoCallbackData(
            action="view_machine",
            key=key
        ).pack()
    ))
    
    await callback.message.edit_text(
        f"Вы уверены, что хотите удалить кофемашину {machine.model} в {machine.location}?",
        reply_markup=keyboard
    )


async def delete_machine_execute(callback: types.CallbackQuery, state: FSMContext):
    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key
    data = await CALLBACK_STORE.get(key)
    machine_id = data["machine_id"]

    with EspressoMachinesDB() as db:
        db.delete_machine(machine_id)

    await CALLBACK_STORE.delete(key)
    
    await callback.message.edit_text("✅ Кофемашина удалена")
    # Возвращаемся к списку машин
    await show_machines(callback, state)


async def cancel_add(callback: types.CallbackQuery, state: FSMContext):
    await show_machines(callback, state)


async def cancel_update(callback: types.CallbackQuery, state: FSMContext):
    await view_machine(callback, state)


async def view_service_history(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.ServiceHistory.state)
    
    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key
    data = await CALLBACK_STORE.get(key)
    
    if not data:
        await callback.message.edit_text("Данные не найдены")
        return
        
    machine_id = data["machine_id"]
    
    # Get page from callback_data, default to 1
    page = int(getattr(callback_data, 'page', 1))
    
    with EspressoMachinesDB() as db:
        machine = db.get_machine(machine_id)
    
    if not machine or not machine.service_dates:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(
            "⬅️ Назад",
            callback_data=EspressoCallbackData(
                action="view_machine",
                key=key
            ).pack()
        ))
        
        await callback.message.edit_text(
            "☕️ История обслуживания\n\n"
            "Нет записей об обслуживании для данной кофемашины.",
            reply_markup=keyboard
        )
        return
    
    # Sort service dates by date (newest first)
    sorted_service_dates = sorted(
        machine.service_dates, 
        key=lambda x: datetime.strptime(x.date, '%d.%m.%Y'),
        reverse=True
    )
    
    # Calculate pagination
    items_per_page = 5
    total_pages = (len(sorted_service_dates) + items_per_page - 1) // items_per_page
    
    # Adjust page if out of bounds
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # Get current page items
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_page_items = sorted_service_dates[start_idx:end_idx]
    
    # Create keyboard with service date buttons
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    for service in current_page_items:
        # Создаем уникальный ключ для каждого сервиса
        service_key = CALLBACK_STORE._get_random_key()
        # Сохраняем информацию о машине и сервисе
        await CALLBACK_STORE.set(service_key, {
            "machine_id": machine_id,
            "service_id": service._id
        })
        
        keyboard.add(types.InlineKeyboardButton(
            f"📅 {service.date}",
            callback_data=EspressoCallbackData(
                action="view_service_details",
                key=service_key,
                page=page
            ).pack()
        ))
    
    # Add pagination controls
    navigation_buttons = []
    
    if page > 1:
        # Для пагинации сохраняем тот же ключ машины, но меняем страницу
        navigation_buttons.append(types.InlineKeyboardButton(
            "◀️ Назад",
            callback_data=EspressoCallbackData(
                action="history_service",
                key=key,
                page=page-1
            ).pack()
        ))
    
    if page < total_pages:
        navigation_buttons.append(types.InlineKeyboardButton(
            "Вперед ▶️",
            callback_data=EspressoCallbackData(
                action="history_service",
                key=key,
                page=page+1
            ).pack()
        ))
    
    if navigation_buttons:
        keyboard.row(*navigation_buttons)
    
    # Add back button
    keyboard.add(types.InlineKeyboardButton(
        "↩️ Вернуться к кофемашине",
        callback_data=EspressoCallbackData(
            action="view_machine",
            key=key
        ).pack()
    ))
    
    await callback.message.edit_text(
        f"☕️ История обслуживания {machine.model} ({machine.location})\n\n"
        f"Страница {page} из {total_pages}",
        reply_markup=keyboard
    )


async def view_service_details(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EmployeesSG.Espresso.ServiceDetails.state)
    
    callback_data = EspressoCallbackData.unpack(callback.data)
    key = callback_data.key
    data = await CALLBACK_STORE.get(key)
    
    if not data:
        await callback.message.edit_text("Данные не найдены")
        return
    
    machine_id = data["machine_id"]
    service_id = data["service_id"]
    
    # Создаем новый ключ для кнопки "Назад" с информацией только о машине
    back_key = CALLBACK_STORE._get_random_key()
    await CALLBACK_STORE.set(back_key, {"machine_id": machine_id})
    
    with EspressoMachinesDB() as db:
        machine = db.get_machine(machine_id)
    
    if not machine:
        await callback.message.edit_text("Кофемашина не найдена")
        return
    
    # Find the service by ID
    service = next((s for s in machine.service_dates if s._id == service_id), None)
    
    if not service:
        await callback.message.edit_text("Запись об обслуживании не найдена")
        return
    
    # Create keyboard with back button
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "↩️ Назад к списку",
        callback_data=EspressoCallbackData(
            action="history_service",
            key=back_key,
            page=callback_data.page
        ).pack()
    ))
    
    # Format service details
    text = (
        f"📝 Детали обслуживания кофемашины {machine.model}\n\n"
        f"📍 Местоположение: {machine.location}\n"
        f"📅 Дата: {service.date}\n"
        f"🔍 Описание: {service.description}\n"
    )
    
    if service.authorized:
        text += f"👤 Авторизовал: {service.authorized}\n"
        text += f"👤 Нажми, чтобы найти: /whois{service.authorized}\n"

    text += f"🆔 Идентификатор: {service._id}"
    
    await callback.message.edit_text(text, reply_markup=keyboard)


def reg_espresso_handlers(dp: Dispatcher):
    # Регистрируем обработчики для просмотра списка машин
    dp.register_callback_query_handler(
        show_machines,
        lambda c: (c.data.startswith(EspressoCallbackData.prefix) and 
                  EspressoCallbackData.unpack(c.data).action == "show_machines") or 
                 (c.data.startswith(EspressoCallbackData.prefix) and 
                  EspressoCallbackData.unpack(c.data).action == "back_to_list"),
        state='*'
    )
    
    # Регистрируем обработчик для просмотра деталей машины
    dp.register_callback_query_handler(
        view_machine,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "view_machine",
        state='*'
    )
    
    # Регистрируем обработчики для добавления машины
    dp.register_callback_query_handler(
        add_machine_start,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "add_machine",
        state=EmployeesSG.Espresso.Menu.state
    )
    
    dp.register_message_handler(
        add_machine_location,
        state=EmployeesSG.Espresso.Add.Location.state
    )
    
    dp.register_message_handler(
        add_machine_model,
        state=EmployeesSG.Espresso.Add.Model.state
    )
    
    # Регистрируем обработчики для добавления обслуживания
    dp.register_callback_query_handler(
        add_service_start,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "add_service",
        state='*'
    )
    
    dp.register_message_handler(
        add_service_date,
        state=EmployeesSG.Espresso.Add.ServiceDate.state
    )
    
    dp.register_message_handler(
        add_service_description,
        state=EmployeesSG.Espresso.Add.ServiceDescription.state
    )
    
    # Регистрируем обработчики для обновления замены резинок
    dp.register_callback_query_handler(
        update_gasket_start,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "update_gasket",
        state='*'
    )
    
    dp.register_message_handler(
        update_gasket_date,
        state=EmployeesSG.Espresso.Update.GasketDate.state
    )
    
    # Регистрируем обработчики для удаления машины
    dp.register_callback_query_handler(
        delete_machine_confirm,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "delete_machine",
        state='*'
    )
    
    dp.register_callback_query_handler(
        delete_machine_execute,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "confirm_delete",
        state='*'
    )
    
    # Регистрируем обработчики для отмены операций
    dp.register_callback_query_handler(
        cancel_add,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "cancel_add",
        state='*'
    )
    
    dp.register_callback_query_handler(
        cancel_update,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "cancel_update",
        state='*'
    ) 
    
    # Регистрируем обработчики для просмотра истории обслуживания
    dp.register_callback_query_handler(
        view_service_history,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "history_service",
        state='*'
    )
    
    dp.register_callback_query_handler(
        view_service_details,
        lambda c: c.data.startswith(EspressoCallbackData.prefix) and 
                 EspressoCallbackData.unpack(c.data).action == "view_service_details",
        state='*'
    )