import json
import os
import sys


from setup_logging import *

logger = get_logger()


class TransformMovies:
    def __init__(self, task):
        self.task = task

    def transform(self, data_table, augment_tables):
        def get_plain_list(data):
            return ",".join(f"{str(x[1])}" for x in data)

        def get_dict_list(data):
            temp_list = []
            for row in data:
                temp_dict = {"id": row[0], "name": row[1]}
                temp_list.append(temp_dict)

            return temp_list

        processed_data = []
        for item in data_table:
            (id_, modified, title, description, rating) = item

            genres_list = get_plain_list(augment_tables["genres"][id_])
            actors_names_list = get_plain_list(augment_tables["actors"][id_])
            writers_names_list = get_plain_list(augment_tables["writers"][id_])
            director_list = get_plain_list(augment_tables["directors"][id_])

            actors_full_list = get_dict_list(augment_tables["actors"][id_])
            writers_full_list = get_dict_list(augment_tables["writers"][id_])

            odd = {
                "id": id_,
                "imdb_rating": rating,
                "genre": genres_list,
                "title": title,
                "description": description,
                "director": director_list,
                "actors_names": actors_names_list,
                "writers_names": writers_names_list,
                "actors": actors_full_list,
                "writers": writers_full_list,
            }

            processed_data.append(odd)

        return processed_data
