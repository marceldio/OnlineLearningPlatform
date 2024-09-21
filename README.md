Шаг 3. (текущий)
Задание 1
Реализуйте CRUD для пользователей, в том числе регистрацию пользователей, настройте в проекте использование JWT-авторизации и закройте каждый эндпоинт авторизацией.
    Эндпоинты для авторизации и регистрации должны остаться доступны для неавторизованных пользователей.

Задание 2
Заведите группу модераторов и опишите для нее права работы с любыми уроками и курсами, но без возможности их удалять и создавать новые. Заложите функционал такой проверки в контроллеры.

Задание 3
Опишите права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть, редактировать и удалять только свои курсы и уроки.
    Примечание
    Заводить группы лучше через админку и не реализовывать для этого дополнительных эндпоинтов.

Дополнительное задание
    Для профиля пользователя введите ограничения, чтобы авторизованный пользователь мог просматривать любой профиль, но редактировать только свой. При этом для просмотра чужого профиля должна быть доступна только общая информация, в которую не входят: пароль, фамилия, история платежей.
Примечание: дополнительные задания, помеченные звездочкой, желательны, но не обязательны к выполнению.

Шаг 2. (выполнен)

Задание 1
Для модели курса добавьте в сериализатор поле вывода количества уроков. Поле реализуйте с помощью
SerializerMethodField()

Задание 2
Добавьте новую модель в приложение users:
Платежи
    пользователь,
    дата оплаты,
    оплаченный курс или урок,
    сумма оплаты,
    способ оплаты: наличные или перевод на счет.
    Поля:
    пользователь,
    оплаченный курс
    и
    отдельно оплаченный урок
    должны быть ссылками на соответствующие модели.
Запишите в таблицу, соответствующую этой модели данные через инструмент фикстур или кастомную команду.
    Если вы забыли как работать с фикстурами или кастомной командой - можете вернуться к уроку 20.1 Работа с ORM в Django чтобы вспомнить материал.

Задание 3
Для сериализатора для модели курса реализуйте поле вывода уроков. Вывод реализуйте с помощью сериализатора для связанной модели.
    Один сериализатор должен выдавать и количество уроков курса и информацию по всем урокам курса одновременно.

Задание 4
Настроить фильтрацию для эндпоинта вывода списка платежей с возможностями:
    менять порядок сортировки по дате оплаты,
    фильтровать по курсу или уроку,
    фильтровать по способу оплаты.

Дополнительное задание
    Для профиля пользователя сделайте вывод истории платежей, расширив сериализатор для вывода списка платежей


Шаг 1. (выполнен)

Задание 1
Создайте новый Django-проект, подключите DRF в настройках проекта.

Задание 2
Создайте следующие модели:
    Пользователь:
        все поля от обычного пользователя, но авторизацию заменить на email;
        телефон;
        город;
        аватарка.
    Модель пользователя разместите в приложении users
    Курс:
        название,
        превью (картинка),
        описание.
    Урок:
        название,
        описание,
        превью (картинка),
        ссылка на видео.
    Урок и курс - это связанные между собой сущности. Уроки складываются в курс, в одном курсе может быть много уроков. Реализуйте связь между ними.
Модель курса и урока разместите в отдельном приложении. Название для приложения выбирайте такое, чтобы оно описывало то, с какими сущностями приложение работает. Например, lms или materials - отличные варианты.

Задание 3
Опишите CRUD для моделей курса и урока. Для реализации CRUD для курса используйте Viewsets, а для урока - Generic-классы.
Для работы контроллеров опишите простейшие сериализаторы.
    При реализации CRUD для уроков реализуйте все необходимые операции (получение списка, получение одной сущности, создание, изменение и удаление).
Для работы контроллеров опишите простейшие сериализаторы.
    Работу каждого эндпоинта необходимо проверять с помощью Postman.
    Также на данном этапе работы мы не заботимся о безопасности и не закрываем от редактирования объекты и модели даже самой простой авторизацией.
