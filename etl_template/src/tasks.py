from datanode_postgres import DataNodePostgres
from datanode_es_raw import DataNodeES
from transform_movies import TransformMovies
from etl_extractor import ETLExtractor
from etl_transformer import ETLTransformer
from etl_loader import ETLLoader
from etl_enricher import ETLEnricher


# Стадии ETL
STAGES = {
    # Подготовка списков извлечения
    "prefetch": ETLExtractor,
    # Извлечение основных данных
    "extract": ETLExtractor,
    # Извлечение связанных данных
    "aggregate": ETLEnricher,
    # Извлечение связанных данных
    "transform": ETLTransformer,
    # Загрузка в конечную систему
    "load": ETLLoader,
}


# Команды, которые повторяются из задачи в задачу
# Так как задача решалась в общем случае, без привязки к конкретной БД,
# то запросы не связаны между собой.
AUGMENT_ACTORS_COMMAND = {
    "sql_query": "SELECT pers.id, pers.full_name "
    "FROM content.person as pers, content.person_film_work as pfw "
    "WHERE pfw.film_work_id = '$parent_id' "
    "AND pers.id = pfw.person_id "
    "AND pfw.role = 'actor' ",
    "worker": DataNodePostgres,
    "stage": "aggregate",
    "depends_on": "fetch_movies",
}

AUGMENT_WRITERS_COMMAND = {
    "sql_query": "SELECT pers.id, pers.full_name "
    "FROM content.person as pers, content.person_film_work as pfw "
    "WHERE pfw.film_work_id = '$parent_id' "
    "AND pers.id = pfw.person_id "
    "AND pfw.role = 'writer' ",
    "worker": DataNodePostgres,
    "stage": "aggregate",
    "depends_on": "fetch_movies",
}

AUGMENT_DIRECTORS_COMMAND = {
    "sql_query": "SELECT pers.id, pers.full_name "
    "FROM content.person as pers, content.person_film_work as pfw "
    "WHERE pfw.film_work_id = '$parent_id' "
    "AND pers.id = pfw.person_id "
    "AND pfw.role = 'director' ",
    "worker": DataNodePostgres,
    "stage": "aggregate",
    "depends_on": "fetch_movies",
}

AUGMENT_GENRES_COMMAND = {
    "sql_query": "SELECT gnr.id, gnr.name "
    "FROM content.genre as gnr, content.genre_film_work as gfw "
    "WHERE gfw.film_work_id = '$parent_id' "
    "AND gnr.id = gfw.genre_id ",
    "worker": DataNodePostgres,
    "stage": "aggregate",
    "depends_on": "fetch_movies",
}

TRANSFORM_COMMAND = {
    "worker": TransformMovies,
    "stage": "transform",
    "depends_on": "fetch_movies",
    "enrich_with": {
        "actors": "augment_actors",
        "writers": "augment_writers",
        "directors": "augment_directors",
        "genres": "augment_genres",
    },
}

LOAD_COMMAND = {"worker": DataNodeES, "stage": "load", "depends_on": "transform"}

# Словарь с задачами (task)
# Каждая задача состоит из команд (command)
# У каждой задачи есть
#  -stage - реализует менеджмент данных, ссылка на Класс команды,см STAGES
#  - worker - Класс, непосредственно обрабатывает данные
#  - sql_query - SQL запрос с параметризацией
#  - depends_on - предыдущая команда, по ней будет строиться параметризация
#  - enrich_with -  #названия зависимостей от нод в списке задач, которые используются для обогащения данных
TASKS = {
    "update_films": {
        "fetch_movies": {
            "sql_query": "SELECT id, modified, title, description, rating "
            "FROM content.film_work "
            "WHERE modified > '$modified_last' "
            "ORDER BY modified "
            "LIMIT $batch_size ",
            "worker": DataNodePostgres,
            "stage": "extract",
        },
        "augment_actors": AUGMENT_ACTORS_COMMAND,
        "augment_writers": AUGMENT_WRITERS_COMMAND,
        "augment_directors": AUGMENT_DIRECTORS_COMMAND,
        "augment_genres": AUGMENT_GENRES_COMMAND,
        "transform": TRANSFORM_COMMAND,
        "load": LOAD_COMMAND,
    },
    "update_pers": {
        "prefetch_person": {
            "sql_query": "SELECT id, modified "
            "FROM content.person "
            "WHERE modified > '$modified_last' "
            "ORDER BY modified "
            "LIMIT $batch_size ",
            "stage": "prefetch",
            "worker": DataNodePostgres,
        },
        "prefetch_movies": {
            "sql_query": "SELECT pfw.film_work_id "
            "FROM content.person as prs, content.person_film_work as pfw "
            "WHERE prs.id IN ($list_id) "
            "AND prs.id = pfw.person_id ",
            "worker": DataNodePostgres,
            "stage": "prefetch",
            "depends_on": "prefetch_person",
        },
        "fetch_movies": {
            "sql_query": "SELECT id, modified, title, description, rating "
            "FROM content.film_work "
            "WHERE id IN ($list_id) "
            "ORDER BY modified ",
            "worker": DataNodePostgres,
            "stage": "extract",
            "depends_on": "prefetch_movies",
        },
        "augment_actors": AUGMENT_ACTORS_COMMAND,
        "augment_writers": AUGMENT_WRITERS_COMMAND,
        "augment_directors": AUGMENT_DIRECTORS_COMMAND,
        "augment_genres": AUGMENT_GENRES_COMMAND,
        "transform": TRANSFORM_COMMAND,
        "load": LOAD_COMMAND,
    },
    "update_genre": {
        "prefetch_genre": {
            "sql_query": "SELECT id, modified "
            "FROM content.genre "
            "WHERE modified > '$modified_last' ",
            "stage": "prefetch",
            "worker": DataNodePostgres,
        },
        "prefetch_movies": {
            "sql_query": "SELECT gfw.film_work_id "
            "FROM content.genre as gnr, content.genre_film_work as gfw "
            "WHERE gnr.id IN ($list_id) "
            "AND gnr.id = gfw.genre_id ",
            "worker": DataNodePostgres,
            "stage": "prefetch",
            "depends_on": "prefetch_genre",
        },
        "fetch_movies": {
            "sql_query": "SELECT id, modified, title, description, rating "
            "FROM content.film_work "
            "WHERE id IN ($list_id) "
            "ORDER BY modified ",
            "worker": DataNodePostgres,
            "stage": "extract",
            "depends_on": "prefetch_movies",
        },
        "augment_actors": AUGMENT_ACTORS_COMMAND,
        "augment_writers": AUGMENT_WRITERS_COMMAND,
        "augment_directors": AUGMENT_DIRECTORS_COMMAND,
        "augment_genres": AUGMENT_GENRES_COMMAND,
        "transform": TRANSFORM_COMMAND,
        "load": LOAD_COMMAND,
    },
}
