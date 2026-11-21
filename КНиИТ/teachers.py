"""Преподаватели КНиИТ. Одна запись нагрузки содержит академические часы hours."""
from copy import deepcopy


class TeacherProfile:
    # Пн–Сб, доступна сетка звонков. В классе преподавателя можно задать свой словарь.
    weekly_available = {day: tuple(range(1, 9)) for day in ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб")}
    date_overrides = {}  # Например, {"2027-02-08": (2, 3, 4)} или {"2027-02-08": ()}.
    courses = ()


class Абросимов_Михаил_Борисович(TeacherProfile):
    name = 'Абросимов Михаил Борисович'
    source = 'https://www.sgu.ru/schedule/teacher/1813'
    courses = (
        {'subject': 'НИР:Методы оптимизации графовых систем', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/192'], 'note': '', 'hours': None},
        {'subject': 'Сложность вычислений', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Сложность вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Теория графов', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Теория построения отказоустойчивых систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'Теория построения отказоустойчивых систем', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
    )


class Агафонова_Нина_Юрьевна(TeacherProfile):
    name = 'Агафонова Нина Юрьевна'
    source = 'https://www.sgu.ru/schedule/teacher/385'
    courses = (
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/351', 'do/381'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистики', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистики', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
    )


class Алексеева_Дина_Алексеевна(TeacherProfile):
    name = 'Алексеева Дина Алексеевна'
    source = 'https://www.sgu.ru/schedule/teacher/3101'
    courses = (
        {'subject': 'Введение в языкознание', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/121', 'do/131', 'do/132', 'do/141', 'do/151', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'Деловой иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
    )


class Алексеева_Мария_Олеговна(TeacherProfile):
    name = 'Алексеева Мария Олеговна'
    source = 'https://www.sgu.ru/schedule/teacher/4752'
    courses = (
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '2 под', 'hours': None},
    )


class Андреева_Ксения_Олеговна(TeacherProfile):
    name = 'Андреева   Ксения Олеговна'
    source = 'https://www.sgu.ru/schedule/teacher/5090'
    courses = (
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/221', 'do/241'], 'note': '', 'hours': None},
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '', 'hours': None},
    )


class Андрейченко_Дмитрий_Константинович(TeacherProfile):
    name = 'Андрейченко Дмитрий Константинович'
    source = 'https://www.sgu.ru/schedule/teacher/2523'
    courses = (
        {'subject': 'Автоматизированные системы научных исследований', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171', 'do/173', 'do/174'], 'note': '', 'hours': None},
        {'subject': 'Автоматизированные системы научных исследований', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'Автоматизированные системы научных исследований', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '1 под', 'hours': None},
        {'subject': 'Автоматизированные системы научных исследований', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '2 под', 'hours': None},
        {'subject': 'Автоматизированные системы научных исследований', 'kind': 'ПРАКТИКА', 'groups': ['do/174'], 'note': '', 'hours': None},
        {'subject': 'Математическое моделирование и высокопроизв вычисления', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '1 под', 'hours': None},
        {'subject': 'Математическое моделирование и высокопроизводительные вычисления', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/173'], 'note': '', 'hours': None},
        {'subject': 'Математическое моделирование и высокопроизводительные вычисления', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '2 под', 'hours': None},
        {'subject': 'Математическое моделирование, численные методы и комплексы программ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/291'], 'note': '226а', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/292'], 'note': '226а', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '', 'hours': None},
        {'subject': 'Системный анализ, управление и управление информации, статистика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/292'], 'note': '226а', 'hours': None},
        {'subject': 'Технология высокопроизводительной обработки больших данных', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/441'], 'note': '', 'hours': None},
        {'subject': 'Технология высокопроизводительной обработки больших данных', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Технология высокопроизводительной обработки больших данных', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
    )


class Андросов_Иван_Алексеевич(TeacherProfile):
    name = 'Андросов Иван Алексеевич'
    source = 'https://www.sgu.ru/schedule/teacher/4168'
    courses = (
        {'subject': 'Методы программирования', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Методы программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '2 под', 'hours': None},
    )


class Балакирева_Екатерина_Игоревна(TeacherProfile):
    name = 'Балакирева Екатерина Игоревна'
    source = 'https://www.sgu.ru/schedule/teacher/1054'
    courses = (
        {'subject': 'Педагогика высшей школы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/291', 'do/292'], 'note': '', 'hours': None},
    )


class Барков_Павел_Валерьевич(TeacherProfile):
    name = 'Барков Павел Валерьевич'
    source = 'https://www.sgu.ru/schedule/teacher/4554'
    courses = (
        {'subject': 'Физика', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '2 под', 'hours': None},
    )


class Батраева_Инна_Александровна(TeacherProfile):
    name = 'Батраева Инна Александровна'
    source = 'https://www.sgu.ru/schedule/teacher/132'
    courses = (
        {'subject': 'Базы данных', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/341', 'do/351'], 'note': '', 'hours': None},
        {'subject': 'Базы данных', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '1 под', 'hours': None},
        {'subject': 'Базы данных', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '1 под', 'hours': None},
        {'subject': 'Базы данных', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '1 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '2 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '3 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '3 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '2 под', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Проектирование высоконадеж и высокодоступ решений для БД', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/273'], 'note': '', 'hours': None},
        {'subject': 'Проектирование высоконадеж и высокодоступ решений для БД', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '1 под', 'hours': None},
        {'subject': 'Проектирование высоконадеж и высокодоступ решений для БД', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '2 под', 'hours': None},
        {'subject': 'Структура данных и алгоритмы', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Структура данных и алгоритмы', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/251'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '2 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '2 под', 'hours': None},
    )


class Богомолов_Алексей_Сергеевич(TeacherProfile):
    name = 'Богомолов Алексей Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/134'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/191'], 'note': '', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/292'], 'note': '', 'hours': None},
        {'subject': 'Стандартизация программного обеспечения', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Стандартизация программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Стандартизация программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
    )


class Бредихин_Дмитрий_Александрович(TeacherProfile):
    name = 'Бредихин  Дмитрий Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/3581'
    courses = (
        {'subject': 'Алгебра и геометрия', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'Алгебра и геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
    )


class Букушева_Алия_Владимировна(TeacherProfile):
    name = 'Букушева Алия Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/399'
    courses = (
        {'subject': 'Инструменты анализа данных', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '3 под', 'hours': None},
        {'subject': 'Методология разработки решений на основе искусственного интеллекта', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '1 под', 'hours': None},
        {'subject': 'Методология разработки решений на основе искусственного интеллекта', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '2 под', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '3 под', 'hours': None},
    )


class Булавина_Екатерина_Викторовна(TeacherProfile):
    name = 'Булавина Екатерина Викторовна'
    source = 'https://www.sgu.ru/schedule/teacher/138'
    courses = (
        {'subject': 'Введение в специальность', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121', 'do/141', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'Введение в специальность', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'Введение в специальность', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
        {'subject': 'Введение в специальность', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '2 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '4 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '2 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
    )


class Васильев_Александр_Алексеевич(TeacherProfile):
    name = 'Васильев Александр Алексеевич'
    source = 'https://www.sgu.ru/schedule/teacher/5396'
    courses = (
        {'subject': 'Программирование на языке С++', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '2 под', 'hours': None},
        {'subject': 'Технология хранения и архитектура больших данных', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '2 под', 'hours': None},
    )


class Вешнева_Ирина_Владимировна(TeacherProfile):
    name = 'Вешнева Ирина Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/2886'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/191'], 'note': '', 'hours': None},
        {'subject': 'Программирование распределенных сетей технических систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/174'], 'note': '', 'hours': None},
        {'subject': 'Программирование распределенных сетей технических систем', 'kind': 'ПРАКТИКА', 'groups': ['do/174'], 'note': '', 'hours': None},
        {'subject': 'Технологии построения микропроцессорной техники', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/174'], 'note': '', 'hours': None},
        {'subject': 'Технологии построения микропроцессорной техники', 'kind': 'ПРАКТИКА', 'groups': ['do/174'], 'note': '', 'hours': None},
    )


class Власов_Андрей_Александрович(TeacherProfile):
    name = 'Власов Андрей Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/4394'
    courses = (
        {'subject': 'Разработка WEB - приложений', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/441'], 'note': '', 'hours': None},
        {'subject': 'Разработка WEB - приложений', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Разработка WEB - приложений', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
    )


class Ганюшкина_Анна_Вячеславовна(TeacherProfile):
    name = 'Ганюшкина Анна Вячеславовна'
    source = 'https://www.sgu.ru/schedule/teacher/5100'
    courses = (
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '2 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '2 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '4 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '2 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '3 под', 'hours': None},
        {'subject': 'Технология хранения и архитектура больших данных', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '1 под', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '2 под', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '2 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '4 под', 'hours': None},
    )


class Гераськин_Алексей_Сергеевич(TeacherProfile):
    name = 'Гераськин Алексей Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/142'
    courses = (
        {'subject': 'Теория информации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Теория кодирования, сжатия и восстановления информации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Теория кодирования, сжатия и восстановления информации', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
    )


class Головченко_Милана_Андреевна(TeacherProfile):
    name = 'Головченко Милана Андреевна'
    source = 'https://www.sgu.ru/schedule/teacher/5150'
    courses = (
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '', 'hours': None},
    )


class Горбунова_Елена_Николаевна(TeacherProfile):
    name = 'Горбунова Елена Николаевна'
    source = 'https://www.sgu.ru/schedule/teacher/3381'
    courses = (
        {'subject': 'Основы теории изучаемого языка', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/221', 'do/231', 'do/241', 'do/251', 'do/281'], 'note': '', 'hours': None},
    )


class Гортинский_Алексей_Владимирович(TeacherProfile):
    name = 'Гортинский Алексей Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/143'
    courses = (
        {'subject': 'Защита в операционных системах', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Защита в операционных системах', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
        {'subject': 'Методы защиты информации и информационная безопасность', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/271', 'do/272', 'do/273'], 'note': '', 'hours': None},
        {'subject': 'Методы защиты информации и информационная безопасность', 'kind': 'ПРАКТИКА', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Методы защиты информации и информационная безопасность', 'kind': 'ПРАКТИКА', 'groups': ['do/272'], 'note': '', 'hours': None},
        {'subject': 'Методы защиты информации и информационная безопасность', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы защиты информации и информационная безопасность', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '2 под', 'hours': None},
        {'subject': 'Основы компьютерной экспертизы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Основы компьютерной экспертизы', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Программно-аппаратные средства обеспечения информационной безопасности', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '1 под', 'hours': None},
    )


class Грецова_Анастасия_Павловна(TeacherProfile):
    name = 'Грецова Анастасия Павловна'
    source = 'https://www.sgu.ru/schedule/teacher/2101'
    courses = (
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Теория графов', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '1 под', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/341', 'do/381'], 'note': '', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '1 под', 'hours': None},
    )


class Гущин_Андрей_Юрьевич(TeacherProfile):
    name = 'Гущин Андрей Юрьевич'
    source = 'https://www.sgu.ru/schedule/teacher/5398'
    courses = (
        {'subject': 'Операционные системы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Операционные системы', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '1 под', 'hours': None},
        {'subject': 'Операционные системы', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '2 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
    )


class Дмитриев_Павел_Олегович(TeacherProfile):
    name = 'Дмитриев Павел Олегович'
    source = 'https://www.sgu.ru/schedule/teacher/3536'
    courses = (
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '2 под', 'hours': None},
        {'subject': 'Проектирование компьютерных сетей', 'kind': 'ПРАКТИКА', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Проектирование компьютерных сетей', 'kind': 'ПРАКТИКА', 'groups': ['do/272'], 'note': '', 'hours': None},
        {'subject': 'Робототехника', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '2 под', 'hours': None},
        {'subject': 'Робототехника', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '3 под', 'hours': None},
        {'subject': 'Сети ЭВМ и системы телекоммуникаций', 'kind': 'ПРАКТИКА', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Сети ЭВМ и системы телекоммуникаций', 'kind': 'ПРАКТИКА', 'groups': ['do/272'], 'note': '', 'hours': None},
        {'subject': 'Сети и телекоммуникации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/321'], 'note': '', 'hours': None},
        {'subject': 'Сети и телекоммуникации', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '2 под', 'hours': None},
        {'subject': 'Сети и телекоммуникации', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '3 под', 'hours': None},
    )


class Дорохина_Анастасия_Сергеевна(TeacherProfile):
    name = 'Дорохина Анастасия Сергеевна'
    source = 'https://www.sgu.ru/schedule/teacher/5816'
    courses = (
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '4 под', 'hours': None},
    )


class Дорошин_Иван_Александрович(TeacherProfile):
    name = 'Дорошин Иван Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/1124'
    courses = (
        {'subject': 'Основы Российской государственности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121', 'do/141'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'Основы Российской государственности', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
    )


class Ежов_Д_М(TeacherProfile):
    name = 'Ежов Д. М.'
    source = None
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '2 под', 'hours': None},
    )


class Есин_Илья_Дмитриевич(TeacherProfile):
    name = 'Есин Илья Дмитриевич'
    source = 'https://www.sgu.ru/schedule/teacher/4611'
    courses = (
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '1 под', 'hours': None},
    )


class Жаркова_Анастасия_Владимировна(TeacherProfile):
    name = 'Жаркова Анастасия Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/3134'
    courses = (
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/421', 'do/441'], 'note': '', 'hours': None},
        {'subject': 'Информационная безопасность и защита информации', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы алгебраической геометрии в криптографии', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Методы алгебраической геометрии в криптографии', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы алгебраической геометрии в криптографии', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '2 под', 'hours': None},
        {'subject': 'Методы и средства криптографической защиты информации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Методы и средства криптографической защиты информации', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Модели безопасности компьютерных систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Модели безопасности компьютерных систем', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '', 'hours': None},
    )


class Забоев_Максим_Владиславович(TeacherProfile):
    name = 'Забоев Максим Владиславович'
    source = 'https://www.sgu.ru/schedule/teacher/4958'
    courses = (
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '2 под', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '2 под', 'hours': None},
    )


class Зайцев_Максим_Вячеславович(TeacherProfile):
    name = 'Зайцев Максим Вячеславович'
    source = 'https://www.sgu.ru/schedule/teacher/275'
    courses = (
        {'subject': 'История России', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
    )


class Иванов_Александр_Сергеевич(TeacherProfile):
    name = 'Иванов Александр Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/147'
    courses = (
        {'subject': 'Интеллектуальные системы и технологии', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Интеллектуальные системы и технологии', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Интеллектуальные системы и технологии', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
        {'subject': 'Теоретическая информатика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151'], 'note': '', 'hours': None},
        {'subject': 'Теоретическая информатика', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'Теоретическая информатика', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
        {'subject': 'Теоретическая информатика', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'Теоретическая информатика', 'kind': 'ПРАКТИКА', 'groups': ['zo/151'], 'note': '', 'hours': None},
    )


class Иванова_Анна_Сергеевна(TeacherProfile):
    name = 'Иванова Анна Сергеевна'
    source = 'https://www.sgu.ru/schedule/teacher/148'
    courses = (
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/331', 'do/351'], 'note': '', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '2 под', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '2 под', 'hours': None},
    )


class Иванова_Дарья_Валерьевна(TeacherProfile):
    name = 'Иванова Дарья Валерьевна'
    source = 'https://www.sgu.ru/schedule/teacher/993'
    courses = (
        {'subject': 'Английский язык(перев.)', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/321', 'do/331', 'do/341', 'do/351', 'do/381'], 'note': '', 'hours': None},
    )


class Ионов_Кирилл_Игоревич(TeacherProfile):
    name = 'Ионов Кирилл Игоревич'
    source = 'https://www.sgu.ru/schedule/teacher/4926'
    courses = (
        {'subject': 'Разработка WEB- приложений', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/273'], 'note': '', 'hours': None},
        {'subject': 'Разработка WEB- приложений', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '1 под', 'hours': None},
        {'subject': 'Разработка WEB- приложений', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '2 под', 'hours': None},
    )


class Кабанова_Любовь_Валентиновна(TeacherProfile):
    name = 'Кабанова Любовь Валентиновна'
    source = 'https://www.sgu.ru/schedule/teacher/149'
    courses = (
        {'subject': 'История и методология компьютерных наук', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171', 'do/173', 'do/174'], 'note': '', 'hours': None},
        {'subject': 'История и методология компьютерных наук', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'История и методология компьютерных наук', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '', 'hours': None},
        {'subject': 'История и методология компьютерных наук', 'kind': 'ПРАКТИКА', 'groups': ['do/174'], 'note': '', 'hours': None},
        {'subject': 'Экономико-правовые основы рынка программного обеспечения', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/273'], 'note': '', 'hours': None},
        {'subject': 'Экономико-правовые основы рынка программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '', 'hours': None},
    )


class Казачкова_Анна_Андреевна(TeacherProfile):
    name = 'Казачкова Анна Андреевна'
    source = 'https://www.sgu.ru/schedule/teacher/3920'
    courses = (
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '1 под', 'hours': None},
        {'subject': 'Инструменты анализа данных', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '2 под', 'hours': None},
        {'subject': 'Инструменты анализа данных', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '2 под', 'hours': None},
        {'subject': 'Интеллектуальные системы поддержки принятия решений', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '', 'hours': None},
        {'subject': 'Программирование на языке С++', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/341'], 'note': '', 'hours': None},
        {'subject': 'Программирование на языке С++', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '2 под', 'hours': None},
    )


class Калинкин_Михаил_Юрьевич(TeacherProfile):
    name = 'Калинкин Михаил Юрьевич'
    source = 'https://www.sgu.ru/schedule/teacher/678'
    courses = (
        {'subject': 'Конструкторско-технологическое обеспечение производства ЭВМ', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Конструкторско-технологическое обеспечение производства ЭВМ', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
    )


class Клецов_Алексей_Александрович(TeacherProfile):
    name = 'Клецов Алексей Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/2976'
    courses = (
        {'subject': 'Сети и системы передачи информации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Сети и системы передачи информации', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '1 под', 'hours': None},
        {'subject': 'Сети и системы передачи информации', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '2 под', 'hours': None},
    )


class Ковешников_Даниил_Вадимович(TeacherProfile):
    name = 'Ковешников Даниил Вадимович'
    source = 'https://www.sgu.ru/schedule/teacher/5285'
    courses = (
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '2 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '4 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '1 под', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '', 'hours': None},
        {'subject': 'Современные информационные технологии', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Современные информационные технологии', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
    )


class Колосов_Дмитрий_Андреевич(TeacherProfile):
    name = 'Колосов Дмитрий Андреевич'
    source = 'https://www.sgu.ru/schedule/teacher/4144'
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/421', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431', 'do/441'], 'note': '', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '2 под', 'hours': None},
    )


class Комиссарова_Наталья_Евгеньевна(TeacherProfile):
    name = 'Комиссарова Наталья Евгеньевна'
    source = 'https://www.sgu.ru/schedule/teacher/436'
    courses = (
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
    )


class Кондратова_Юлия_Николаевна(TeacherProfile):
    name = 'Кондратова Юлия Николаевна'
    source = 'https://www.sgu.ru/schedule/teacher/155'
    courses = (
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '3 под', 'hours': None},
    )


class Конюхов_Андрей_Иванович(TeacherProfile):
    name = 'Конюхов Андрей Иванович'
    source = 'https://www.sgu.ru/schedule/teacher/1212'
    courses = (
        {'subject': 'Аппаратные средства вычислительной техники', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Аппаратные средства вычислительной техники', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '1 под', 'hours': None},
        {'subject': 'Аппаратные средства вычислительной техники', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '2 под', 'hours': None},
        {'subject': 'Аппаратные средства вычислительной техники', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '3 под', 'hours': None},
        {'subject': 'Аппаратные средства вычислительной техники', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '4 под', 'hours': None},
    )


class Королева_Ольга_Артуровна(TeacherProfile):
    name = 'Королева Ольга Артуровна'
    source = 'https://www.sgu.ru/schedule/teacher/440'
    courses = (
        {'subject': 'Алгебра', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'Алгебра', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'Алгебра', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
    )


class Краснобаев_Александр_Павлович(TeacherProfile):
    name = 'Краснобаев Александр Павлович'
    source = 'https://www.sgu.ru/schedule/teacher/5410'
    courses = (
        {'subject': 'Криптографические протоколы', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '2под', 'hours': None},
        {'subject': 'Основы построения защищенных компьютерных сетей', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Программно-аппаратные средства обеспечения информационной безопасности', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '2 под', 'hours': None},
    )


class Крусс_Юлия_Сергеевна(TeacherProfile):
    name = 'Крусс Юлия Сергеевна'
    source = 'https://www.sgu.ru/schedule/teacher/1308'
    courses = (
        {'subject': 'Алгебра и геометрия', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121', 'do/141'], 'note': '', 'hours': None},
        {'subject': 'Алгебра и геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
    )


class Крючкова_Александра_Андреевна(TeacherProfile):
    name = 'Крючкова Александра Андреевна'
    source = 'https://www.sgu.ru/schedule/teacher/4398'
    courses = (
        {'subject': 'Гибкая разработка программного обеспечения', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171', 'do/173'], 'note': '', 'hours': None},
        {'subject': 'Гибкая разработка программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'Гибкая разработка программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '1 под', 'hours': None},
        {'subject': 'Гибкая разработка программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '2 под', 'hours': None},
        {'subject': 'Метрология и качество программного обеспечения', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/273'], 'note': '', 'hours': None},
        {'subject': 'Метрология и качество программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '1 под', 'hours': None},
        {'subject': 'Метрология и качество программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '2 под', 'hours': None},
        {'subject': 'Тестирование программного обеспечения', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/441', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Тестирование программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Тестирование программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Тестирование программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '2 под', 'hours': None},
        {'subject': 'Тестирование программного обеспечения', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
    )


class Кудрина_Елена_Вячеславовна(TeacherProfile):
    name = 'Кудрина Елена Вячеславовна'
    source = 'https://www.sgu.ru/schedule/teacher/157'
    courses = (
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/221', 'do/241', 'do/281'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '1 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '3 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '1 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '3 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
    )


class Кудрявцева_Елена_Владимировна(TeacherProfile):
    name = 'Кудрявцева Елена Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/1345'
    courses = (
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'Физическая культура и спорт', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Циклические виды спорта', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': 'Бассейн 1 и 2 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': 'Бассейн 3 и 4 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': 'Бассейн 1 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': 'Бассейн 2 и 3 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '2 и 3 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '3 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': 'Бассейн 1 и 2 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': 'Бассейн 1 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': 'Бассейн 1 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': 'Бассейн 2 и 3 под', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': 'Бассейн', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '', 'hours': None},
        {'subject': 'Элективные дисциплины по физической культуре и спорту', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': 'Бассейн', 'hours': None},
    )


class Кузьмина_С_В(TeacherProfile):
    name = 'Кузьмина С. В.'
    source = None
    courses = (
        {'subject': 'Деловой иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'Деловой иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/174'], 'note': '', 'hours': None},
    )


class Купцов_Павел_Владимирович(TeacherProfile):
    name = 'Купцов Павел Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/4191'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/291'], 'note': '', 'hours': None},
        {'subject': 'Технология хранения и архитектура больших данных', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/341'], 'note': '', 'hours': None},
    )


class Курбако_Александр_Васильевич(TeacherProfile):
    name = 'Курбако Александр Васильевич'
    source = 'https://www.sgu.ru/schedule/teacher/4366'
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '3 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/441'], 'note': '3 под', 'hours': None},
    )


class Кушников_Вадим_Алексеевич(TeacherProfile):
    name = 'Кушников Вадим Алексеевич'
    source = 'https://www.sgu.ru/schedule/teacher/2939'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/192'], 'note': '', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/291'], 'note': 'ИПТМУ РАН, каб.33', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/391'], 'note': 'ИПТМУ РАН, каб.33', 'hours': None},
    )


class Лапшева_Елена_Евгеньевна(TeacherProfile):
    name = 'Лапшева Елена Евгеньевна'
    source = 'https://www.sgu.ru/schedule/teacher/159'
    courses = (
        {'subject': 'Бекенд-разработка', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/221', 'do/241', 'do/281'], 'note': '', 'hours': None},
        {'subject': 'Инструменты анализа данных', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '1 под', 'hours': None},
        {'subject': 'Инструменты анализа данных', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '1 под', 'hours': None},
        {'subject': 'Интеллектуальные системы поддержки принятия решений', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '1 под', 'hours': None},
    )


class Лобов_Александр_Андреевич(TeacherProfile):
    name = 'Лобов Александр Андреевич'
    source = 'https://www.sgu.ru/schedule/teacher/4170'
    courses = (
        {'subject': 'Основы информационной безопасности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Основы построения защищенных компьютерных сетей', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Программно-аппаратные средства обеспечения информационной безопасности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Теория информации', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '', 'hours': None},
    )


class Луньков_Алексей_Дмитриевич(TeacherProfile):
    name = 'Луньков Алексей Дмитриевич'
    source = 'https://www.sgu.ru/schedule/teacher/457'
    courses = (
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '', 'hours': None},
    )


class Лучкова_Елена_Вячеславовна(TeacherProfile):
    name = 'Лучкова Елена Вячеславовна'
    source = 'https://www.sgu.ru/schedule/teacher/4485'
    courses = (
        {'subject': 'Программирование и конфигурирование в корпоративных информационных системах', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Программирование и конфигурирование в корпоративных информационных системах', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Программирование и конфигурирование в корпоративных информационных системах', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
    )


class Марков_Андрей_Игоревич(TeacherProfile):
    name = 'Марков Андрей Игоревич'
    source = 'https://www.sgu.ru/schedule/teacher/4483'
    courses = (
        {'subject': 'Облачные технологии', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/273'], 'note': '', 'hours': None},
        {'subject': 'Облачные технологии', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '1 под', 'hours': None},
        {'subject': 'Облачные технологии', 'kind': 'ПРАКТИКА', 'groups': ['do/273'], 'note': '2 под', 'hours': None},
    )


class Маскаев_Владимир_Алексеевич(TeacherProfile):
    name = 'Маскаев Владимир Алексеевич'
    source = 'https://www.sgu.ru/schedule/teacher/5399'
    courses = (
        {'subject': 'Структура данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '1 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '3 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '1 под', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '3 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '2 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '1 под', 'hours': None},
    )


class Матвеева_Юлия_Васильевна(TeacherProfile):
    name = 'Матвеева Юлия Васильевна'
    source = 'https://www.sgu.ru/schedule/teacher/461'
    courses = (
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121', 'do/141'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
    )


class Миронов_Сергей_Владимирович(TeacherProfile):
    name = 'Миронов Сергей Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/165'
    courses = (
        {'subject': 'Основы организации научно-исследовательская работы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171', 'do/173', 'do/174'], 'note': '', 'hours': None},
        {'subject': 'Основы организации научно-исследовательской работы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171', 'do/173', 'do/174'], 'note': '', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/351'], 'note': '', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '1 под', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '3 под', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '2 под', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '1 под', 'hours': None},
    )


class МИТРОХИН_ВЛАДИМИР_АЛЕКСЕЕВИЧ(TeacherProfile):
    name = 'МИТРОХИН ВЛАДИМИР АЛЕКСЕЕВИЧ'
    source = 'https://www.sgu.ru/schedule/teacher/584'
    courses = (
        {'subject': 'Основы Российской государственности', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/151'], 'note': '', 'hours': None},
    )


class Моденова_Ольга_Владимировна(TeacherProfile):
    name = 'Моденова Ольга Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/4997'
    courses = (
        {'subject': 'Теория графов', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
    )


class Молчанов_Владимир_Александрович(TeacherProfile):
    name = 'Молчанов Владимир Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/2494'
    courses = (
        {'subject': 'Алгоритмы алгебры и теории чисел', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Алгоритмы алгебры и теории чисел', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '', 'hours': None},
        {'subject': 'Математическая логика и теория алгоритмов', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'Математическая логика и теория алгоритмов', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Математическая логика и теория алгоритмов', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'Математическая логика и теория алгоритмов', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'Математическая логика и теория алгоритмов', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/194'], 'note': '', 'hours': None},
        {'subject': 'Теоретико-числов.методы в криптографии', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '1 под', 'hours': None},
        {'subject': 'Теоретико-числовые методы в криптографии', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Теоретико-числовые методы в криптографии', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '2 под', 'hours': None},
    )


class Мурсалов_Руслан_Кямранович(TeacherProfile):
    name = 'Мурсалов Руслан Кямранович'
    source = 'https://www.sgu.ru/schedule/teacher/5156'
    courses = (
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/251', 'do/281'], 'note': '', 'hours': None},
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '', 'hours': None},
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
    )


class Неврюев_Александр_Михайлович(TeacherProfile):
    name = 'Неврюев Александр  Михайлович'
    source = 'https://www.sgu.ru/schedule/teacher/4929'
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '4 под', 'hours': None},
    )


class Никитина_Александра_Сергеевна(TeacherProfile):
    name = 'Никитина Александра Сергеевна'
    source = 'https://www.sgu.ru/schedule/teacher/5021'
    courses = (
        {'subject': 'Нейронные сети', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '1 под', 'hours': None},
        {'subject': 'Нейронные сети', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '2 под', 'hours': None},
    )


class Новиков_Валерий_Евгеньевич(TeacherProfile):
    name = 'Новиков Валерий Евгеньевич'
    source = 'https://www.sgu.ru/schedule/teacher/167'
    courses = (
        {'subject': 'Алгебра и геометрия', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Алгебра и геометрия', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Геометрия', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'Геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'Геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'Криптографические протоколы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Криптографические протоколы', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '1 под', 'hours': None},
    )


class Огнева_Марина_Валентиновна(TeacherProfile):
    name = 'Огнева Марина Валентиновна'
    source = 'https://www.sgu.ru/schedule/teacher/168'
    courses = (
        {'subject': 'Инструменты анализа данных', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/241', 'do/341'], 'note': '', 'hours': None},
        {'subject': 'Интеллектуальные системы поддержки принятия решений', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/441'], 'note': '', 'hours': None},
        {'subject': 'Методология разработки решений на основе искусственного интеллекта', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/341'], 'note': '', 'hours': None},
        {'subject': 'Структуры данных и алгоритмы', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '', 'hours': None},
        {'subject': 'Теория графов', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/351'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/141'], 'note': '', 'hours': None},
    )


class Озеров_Данила_Николаевич(TeacherProfile):
    name = 'Озеров Данила Николаевич'
    source = 'https://www.sgu.ru/schedule/teacher/5551'
    courses = (
        {'subject': 'Технологии программирования', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
        {'subject': 'Технологии программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '1 под', 'hours': None},
        {'subject': 'Технологии программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/531'], 'note': '2 под', 'hours': None},
    )


class Павлова_Алена_Александровна(TeacherProfile):
    name = 'Павлова Алена Александровна'
    source = 'https://www.sgu.ru/schedule/teacher/5804'
    courses = (
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '2 под', 'hours': None},
    )


class Пантелеев_Дмитрий_Сергеевич(TeacherProfile):
    name = 'Пантелеев  Дмитрий Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/4543'
    courses = (
        {'subject': 'Система управления базами данных', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '2 под', 'hours': None},
    )


class Панферов_Анатолий_Дмитриевич(TeacherProfile):
    name = 'Панферов Анатолий Дмитриевич'
    source = 'https://www.sgu.ru/schedule/teacher/170'
    courses = (
        {'subject': 'Вычислительные системы', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Вычислительные системы', 'kind': 'ПРАКТИКА', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Проектирование компьютерных сетей', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/271', 'do/272'], 'note': '', 'hours': None},
        {'subject': 'Сети ЭВМ и система телекоммуникаций', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/271', 'do/272'], 'note': '', 'hours': None},
    )


class Папшев_Сергей_Владимирович(TeacherProfile):
    name = 'Папшев Сергей Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/4376'
    courses = (
        {'subject': 'Бекенд-разработка', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/251'], 'note': '', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '1 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '1 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '3 под', 'hours': None},
        {'subject': 'Проектирование архитектуры информационных систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Проектирование архитектуры информационных систем', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Проектирование архитектуры информационных систем', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
    )


class Петров_Дмитрий_Юрьевич(TeacherProfile):
    name = 'Петров Дмитрий Юрьевич'
    source = 'https://www.sgu.ru/schedule/teacher/3336'
    courses = (
        {'subject': 'Основы проектирования систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Основы проектирования систем', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Теория информационных систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/281'], 'note': '', 'hours': None},
        {'subject': 'Теория информационных систем', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
    )


class Поплавский_Дмитрий_Владиславович(TeacherProfile):
    name = 'Поплавский Дмитрий Владиславович'
    source = 'https://www.sgu.ru/schedule/teacher/484'
    courses = (
        {'subject': 'Методы вычислений', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/311', 'do/321', 'do/351', 'do/381'], 'note': '', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '2 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '2 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '3 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '2 под', 'hours': None},
        {'subject': 'Методы вычислений', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
    )


class Портенко_Марина_Сергеевна(TeacherProfile):
    name = 'Портенко Марина Сергеевна'
    source = 'https://www.sgu.ru/schedule/teacher/172'
    courses = (
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '1 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '2 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
        {'subject': 'Теория графов', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '2 под', 'hours': None},
        {'subject': 'Теория графов', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '3 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
    )


class Разумовская_Елена_Владимировна(TeacherProfile):
    name = 'Разумовская Елена Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/488'
    courses = (
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/231'], 'note': '', 'hours': None},
    )


class Рамазанов_Ибадулла_Рамзесович(TeacherProfile):
    name = 'Рамазанов  Ибадулла  Рамзесович'
    source = 'https://www.sgu.ru/schedule/teacher/4627'
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/411'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/421'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/431'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/441'], 'note': '4 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['do/451'], 'note': '4 под', 'hours': None},
    )


class Рогачко_Екатерина_Сергеевна(TeacherProfile):
    name = 'Рогачко Екатерина Сергеевна'
    source = 'https://www.sgu.ru/schedule/teacher/174'
    courses = (
        {'subject': 'Анализ цифровых сигналов в сист передачи и обработки инф', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/272'], 'note': '', 'hours': None},
        {'subject': 'Анализ цифровых сигналов в сист передачи и обработки инф', 'kind': 'ПРАКТИКА', 'groups': ['do/272'], 'note': '', 'hours': None},
        {'subject': 'Методы оптимизации', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/321'], 'note': '', 'hours': None},
        {'subject': 'Методы оптимизации', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы оптимизации', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '2 под', 'hours': None},
        {'subject': 'Методы оптимизации', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '3 под', 'hours': None},
    )


class Романов_Валерий_Александрович(TeacherProfile):
    name = 'Романов Валерий Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/4026'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/292'], 'note': '', 'hours': None},
    )


class Рыданов_Никита_Сергеевич(TeacherProfile):
    name = 'Рыданов Никита Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/4710'
    courses = (
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '2 под', 'hours': None},
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '2 под', 'hours': None},
    )


class Рыхлов_Виктор_Сергеевич(TeacherProfile):
    name = 'Рыхлов Виктор Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/493'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/194'], 'note': '', 'hours': None},
    )


class Сабитова_Л_Р(TeacherProfile):
    name = 'Сабитова Л. Р.'
    source = None
    courses = (
        {'subject': 'Иностранный язык (английский)', 'kind': 'ПРАКТИКА', 'groups': ['do/194'], 'note': '4 корпус, 7 ауд.', 'hours': None},
    )


class Сагаева_Ирина_Дмитриевна(TeacherProfile):
    name = 'Сагаева Ирина Дмитриевна'
    source = 'https://www.sgu.ru/schedule/teacher/176'
    courses = (
        {'subject': 'Дискретная математика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/251', 'do/281'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/221', 'do/231'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Методы трансляций', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Методы трансляций', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Методы трансляций', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
    )


class Сарафанников_Даниил_Александрович(TeacherProfile):
    name = 'Сарафанников  Даниил Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/5821'
    courses = (
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
    )


class Сафрончик_Мария_Ильинична(TeacherProfile):
    name = 'Сафрончик Мария Ильинична'
    source = 'https://www.sgu.ru/schedule/teacher/180'
    courses = (
        {'subject': 'Базы данных', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '2 под', 'hours': None},
        {'subject': 'Базы данных', 'kind': 'ПРАКТИКА', 'groups': ['do/341'], 'note': '2 под', 'hours': None},
        {'subject': 'Базы данных', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '2 под', 'hours': None},
        {'subject': 'ВВЕДЕНИЕ В УЧЕБНЫЙ ПРОЦЕСС', 'kind': 'ПРАКТИКА', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'Система управления базами данных', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Система управления базами данных', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '3 под', 'hours': None},
    )


class Сахно_Людмила_Владимировна(TeacherProfile):
    name = 'Сахно Людмила Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/496'
    courses = (
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/251', 'do/281'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'Математический анализ', 'kind': 'ПРАКТИКА', 'groups': ['zo/251'], 'note': '', 'hours': None},
    )


class Селифонова_Екатерина_Игоревна(TeacherProfile):
    name = 'Селифонова Екатерина Игоревна'
    source = 'https://www.sgu.ru/schedule/teacher/4077'
    courses = (
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Безопасность жизнедеятельности', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '', 'hours': None},
    )


class Сергеев_Александр_Николаевич(TeacherProfile):
    name = 'Сергеев Александр Николаевич'
    source = 'https://www.sgu.ru/schedule/teacher/498'
    courses = (
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/194'], 'note': '', 'hours': None},
    )


class Сергеев_Константин_Сергеевич(TeacherProfile):
    name = 'Сергеев Константин Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/3563'
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/421', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/431', 'do/441'], 'note': '', 'hours': None},
    )


class Сергеева_Надежда_Викторовна(TeacherProfile):
    name = 'Сергеева Надежда Викторовна'
    source = 'https://www.sgu.ru/schedule/teacher/499'
    courses = (
        {'subject': 'Системный анализ и принятие решений', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Системный анализ и принятие решений', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
    )


class Слеповичев_Иван_Иванович(TeacherProfile):
    name = 'Слеповичев Иван Иванович'
    source = 'https://www.sgu.ru/schedule/teacher/183'
    courses = (
        {'subject': 'Нейронные сети', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/531'], 'note': '', 'hours': None},
    )


class Созонов_Евгений_Александрович(TeacherProfile):
    name = 'Созонов Евгений Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/4996'
    courses = (
        {'subject': 'Администрирование операционных систем и сетей', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/241'], 'note': '', 'hours': None},
        {'subject': 'Администрирование операционных систем и сетей', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '1 под', 'hours': None},
        {'subject': 'Администрирование операционных систем и сетей', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '2 под', 'hours': None},
        {'subject': 'Администрирование операционных систем и сетей', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '3 под', 'hours': None},
    )


class Сокиркина_Любовь_Ивановна(TeacherProfile):
    name = 'Сокиркина Любовь Ивановна'
    source = 'https://www.sgu.ru/schedule/teacher/4576'
    courses = (
        {'subject': 'Английский язык(перев.)', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/421', 'do/431', 'do/441', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/191'], 'note': '', 'hours': None},
        {'subject': 'Иностранный язык', 'kind': 'ПРАКТИКА', 'groups': ['do/192'], 'note': '', 'hours': None},
    )


class Соломонов_Владимир_Анатольевич(TeacherProfile):
    name = 'Соломонов Владимир Анатольевич'
    source = 'https://www.sgu.ru/schedule/teacher/279'
    courses = (
        {'subject': 'История России', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121', 'do/141'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/131', 'do/132'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/151'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/131'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/132'], 'note': '', 'hours': None},
        {'subject': 'История России', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
    )


class Сотов_Леонид_Сергеевич(TeacherProfile):
    name = 'Сотов Леонид Сергеевич'
    source = 'https://www.sgu.ru/schedule/teacher/1211'
    courses = (
        {'subject': 'Физика', 'kind': 'ЛАБОРАТОРНАЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Физика', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
    )


class Станкевич_Елена_Петровна(TeacherProfile):
    name = 'Станкевич Елена Петровна'
    source = 'https://www.sgu.ru/schedule/teacher/185'
    courses = (
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '', 'hours': None},
    )


class СТРЫГИНА_СВЕТЛАНА_ВЛАДИМИРОВНА(TeacherProfile):
    name = 'СТРЫГИНА СВЕТЛАНА ВЛАДИМИРОВНА'
    source = 'https://www.sgu.ru/schedule/teacher/559'
    courses = (
        {'subject': 'Основы права и антикоррупционного поведения', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/421', 'do/441', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Основы права и антикоррупционного поведения', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Основы права и антикоррупционного поведения', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Основы права и антикоррупционного поведения', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '', 'hours': None},
        {'subject': 'Основы права и антикоррупционного поведения', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
    )


class Сухова_Екатерина_Владимировна(TeacherProfile):
    name = 'Сухова Екатерина Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/5019'
    courses = (
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '3 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '4 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '2 под', 'hours': None},
        {'subject': 'Бекенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '3 под', 'hours': None},
        {'subject': 'Теория графов', 'kind': 'ПРАКТИКА', 'groups': ['do/351'], 'note': '2 под', 'hours': None},
    )


class Тананко_Игорь_Евстафьевич(TeacherProfile):
    name = 'Тананко Игорь Евстафьевич'
    source = 'https://www.sgu.ru/schedule/teacher/187'
    courses = (
        {'subject': 'Введение в системный анализ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/181'], 'note': '', 'hours': None},
        {'subject': 'Введение в системный анализ', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/272'], 'note': '', 'hours': None},
    )


class Таран_Евгений_Вячеславович(TeacherProfile):
    name = 'Таран Евгений Вячеславович'
    source = 'https://www.sgu.ru/schedule/teacher/5803'
    courses = (
        {'subject': 'Сети и телекоммуникации', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '1 под', 'hours': None},
    )


class Терин_Денис_Владимирович(TeacherProfile):
    name = 'Терин Денис Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/723'
    courses = (
        {'subject': 'Конструкторско-технологическое обеспечение производства ЭВМ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/421'], 'note': '', 'hours': None},
    )


class Тимофеева_Надежда_Евгеньевна(TeacherProfile):
    name = 'Тимофеева Надежда Евгеньевна'
    source = 'https://www.sgu.ru/schedule/teacher/189'
    courses = (
        {'subject': 'Организация ЭВМ и систем', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/321'], 'note': '', 'hours': None},
        {'subject': 'Организация ЭВМ и систем', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '1 под', 'hours': None},
        {'subject': 'Организация ЭВМ и систем', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '2 под', 'hours': None},
        {'subject': 'Организация ЭВМ и систем', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '3 под', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '1 под', 'hours': None},
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '3 под', 'hours': None},
        {'subject': 'Робототехника', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '1 под', 'hours': None},
        {'subject': 'Системное программное обеспечение', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Системное программное обеспечение', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Системное программное обеспечение', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '2 под', 'hours': None},
    )


class Трубицын_Александр_Романович(TeacherProfile):
    name = 'Трубицын Александр Романович'
    source = 'https://www.sgu.ru/schedule/teacher/1705'
    courses = (
        {'subject': 'Основы экономики и финансовой грамотности', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/321'], 'note': '', 'hours': None},
        {'subject': 'Основы экономики и финансовой грамотности', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '', 'hours': None},
    )


class Тяпаев_Ливат_Борисович(TeacherProfile):
    name = 'Тяпаев Ливат Борисович'
    source = 'https://www.sgu.ru/schedule/teacher/190'
    courses = (
        {'subject': 'Дополнительные главы фундаментальной подготовки', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/171', 'do/173', 'do/174'], 'note': '', 'hours': None},
        {'subject': 'Дополнительные главы фундаментальной подготовки', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'Дополнительные главы фундаментальной подготовки', 'kind': 'ПРАКТИКА', 'groups': ['do/173'], 'note': '', 'hours': None},
        {'subject': 'Дополнительные главы фундаментальной подготовки', 'kind': 'ПРАКТИКА', 'groups': ['do/174'], 'note': '', 'hours': None},
        {'subject': 'Математическое моделирование, численные методы и комплексы программ', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/391'], 'note': '', 'hours': None},
        {'subject': 'Научная деятельность, направленная на подготовку диссертации к защите', 'kind': 'ПРАКТИКА', 'groups': ['do/292'], 'note': '', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/171'], 'note': '', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Научно-исследовательская работа', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '', 'hours': None},
        {'subject': 'Программирование в сетях', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/271', 'do/272'], 'note': '', 'hours': None},
        {'subject': 'Программирование в сетях', 'kind': 'ПРАКТИКА', 'groups': ['do/271'], 'note': '', 'hours': None},
        {'subject': 'Программирование в сетях', 'kind': 'ПРАКТИКА', 'groups': ['do/272'], 'note': '', 'hours': None},
        {'subject': 'Теория автоматов', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/321'], 'note': '', 'hours': None},
        {'subject': 'Теория автоматов', 'kind': 'ПРАКТИКА', 'groups': ['do/321'], 'note': '', 'hours': None},
    )


class Ушаков_Иван_Владимирович(TeacherProfile):
    name = 'Ушаков Иван Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/4981'
    courses = (
        {'subject': 'Алгебра и геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
    )


class Филиппов_Борис_Александрович(TeacherProfile):
    name = 'Филиппов Борис Александрович'
    source = 'https://www.sgu.ru/schedule/teacher/4013'
    courses = (
        {'subject': 'Программные средства решения математических задач', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/411', 'do/451'], 'note': '', 'hours': None},
        {'subject': 'Программные средства решения математических задач', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '', 'hours': None},
        {'subject': 'Программные средства решения математических задач', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '', 'hours': None},
    )


class Фомин_Игорь_Николаевич(TeacherProfile):
    name = 'Фомин Игорь Николаевич'
    source = 'https://www.sgu.ru/schedule/teacher/4489'
    courses = (
        {'subject': 'Теория систем и управление сложными системами', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/381'], 'note': '', 'hours': None},
        {'subject': 'Теория систем и управление сложными системами', 'kind': 'ПРАКТИКА', 'groups': ['do/381'], 'note': '', 'hours': None},
    )


class Хамутова_Мария_Васильевна(TeacherProfile):
    name = 'Хамутова Мария Васильевна '
    source = 'https://www.sgu.ru/schedule/teacher/3382'
    courses = (
        {'subject': 'Пр.: Проектная практика', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/311'], 'note': '1 под', 'hours': None},
        {'subject': 'Фронтенд-разработка', 'kind': 'ПРАКТИКА', 'groups': ['do/331'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '3 под', 'hours': None},
    )


class Харламов_Александр_Владимирович(TeacherProfile):
    name = 'Харламов Александр Владимирович'
    source = 'https://www.sgu.ru/schedule/teacher/520'
    courses = (
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/221', 'do/241'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Теория вероятностей и математическая статистика', 'kind': 'ПРАКТИКА', 'groups': ['do/241'], 'note': '', 'hours': None},
    )


class Хворостухина_Екатерина_Владимировна(TeacherProfile):
    name = 'Хворостухина Екатерина Владимировна'
    source = 'https://www.sgu.ru/schedule/teacher/4995'
    courses = (
        {'subject': 'Алгебра и геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
        {'subject': 'Алгебра и геометрия', 'kind': 'ПРАКТИКА', 'groups': ['do/181'], 'note': '', 'hours': None},
    )


class Червяков_Максим_Юрьевич(TeacherProfile):
    name = 'Червяков Максим Юрьевич'
    source = 'https://www.sgu.ru/schedule/teacher/2960'
    courses = (
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/411'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/421'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/431'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/441'], 'note': '1 под', 'hours': None},
        {'subject': 'Техническая эксплуатация и ремонт БАС', 'kind': 'ПРАКТИКА', 'groups': ['do/451'], 'note': '1 под', 'hours': None},
    )


class Черкасова_Ольга_Алексеевна(TeacherProfile):
    name = 'Черкасова Ольга Алексеевна'
    source = 'https://www.sgu.ru/schedule/teacher/1248'
    courses = (
        {'subject': 'Физика', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '3 под', 'hours': None},
    )


class Чернигин_Михаил_Андреевич(TeacherProfile):
    name = 'Чернигин Михаил Андреевич'
    source = 'https://www.sgu.ru/schedule/teacher/5024'
    courses = (
        {'subject': 'Языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '4 под', 'hours': None},
    )


class Черноусова_Елена_Михайловна(TeacherProfile):
    name = 'Черноусова Елена Михайловна'
    source = 'https://www.sgu.ru/schedule/teacher/2633'
    courses = (
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/211', 'do/251'], 'note': '', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '1 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '3 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '1 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '3 под', 'hours': None},
        {'subject': 'Машинно-зависимые языки программирования', 'kind': 'ПРАКТИКА', 'groups': ['do/251'], 'note': '1 под', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121', 'do/181'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'информационные технологии и программирование', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '1 под', 'hours': None},
    )


class Чернышова_Галина_Юрьевна(TeacherProfile):
    name = 'Чернышова Галина Юрьевна'
    source = 'https://www.sgu.ru/schedule/teacher/3705'
    courses = (
        {'subject': 'Дискретная математика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/141'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['do/141'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['do/211'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['do/221'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['do/231'], 'note': '', 'hours': None},
        {'subject': 'Дискретная математика', 'kind': 'ПРАКТИКА', 'groups': ['do/281'], 'note': '', 'hours': None},
        {'subject': 'Робототехника', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/321'], 'note': '', 'hours': None},
    )


class Шаповалова_Надежда_Геннадиевна(TeacherProfile):
    name = 'Шаповалова Надежда Геннадиевна'
    source = 'https://www.sgu.ru/schedule/teacher/2226'
    courses = (
        {'subject': 'Русский язык и культура речи', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/111', 'do/151'], 'note': '', 'hours': None},
        {'subject': 'Русский язык и культура речи', 'kind': 'ЛЕКЦИЯ', 'groups': ['zo/251'], 'note': '', 'hours': None},
        {'subject': 'Русский язык и культура речи', 'kind': 'ПРАКТИКА', 'groups': ['do/111'], 'note': '', 'hours': None},
        {'subject': 'Русский язык и культура речи', 'kind': 'ПРАКТИКА', 'groups': ['do/151'], 'note': '', 'hours': None},
    )


class Шунаев_Владислав_Викторович(TeacherProfile):
    name = 'Шунаев  Владислав Викторович'
    source = 'https://www.sgu.ru/schedule/teacher/3593'
    courses = (
        {'subject': 'Физика', 'kind': 'ЛЕКЦИЯ', 'groups': ['do/121'], 'note': '', 'hours': None},
        {'subject': 'Физика', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '1 под', 'hours': None},
        {'subject': 'Физика', 'kind': 'ПРАКТИКА', 'groups': ['do/121'], 'note': '4 под', 'hours': None},
    )


def teacher_data():
    """Независимая копия настроек и нагрузки для одного расчёта."""
    return [deepcopy(dict(name=profile.name, weekly_available=profile.weekly_available,
                          date_overrides=profile.date_overrides, courses=profile.courses))
            for profile in TeacherProfile.__subclasses__()]
