class TestErrorsStatus:
    WRONG_STATUS = "Ошибка в статусе ответа"
    WRONG_RESPONSE = "Ошибка в типе данных в ответе"
    WRONG_LENGTH = "Ошибка в длине"

    WRONG_MAX_PAGE_SIZE = (
        "Неправильный статус ответа для размера страницы со значением > 1000"
    )
    WRONG_ZERO_PAGE_SIZE = (
        "Неправильный статус ответа для размера страницы со значением == 0"
    )
    WRONG_DEFAULT_RESPONSE = "Запрос без параметров должен соответствовать запросу с параметрами по умолчанию"
    WRONG_SORT_BY_DESC = "Фильмы не отсортированы по уменьшению рейтинга"
    WRONG_SORT_BY_ASC = "Фильмы не отсортированы по возрастанию рейтинга"

    REDIS_NOT_DATA = "Отсутствуют данные в redis"
