from etl_extractor import ETLExtractor
from setup_logging import *

logger = get_logger()

BATCH_SIZE = 100


class ETLEnricher(ETLExtractor):
    def __init__(self, task, task_name, command_name):
        super().__init__(task, task_name, command_name)
        self.log_signature("INIT")

    def run(self, data=None):
        self.log_signature("RUN")
        query = self.task[self.command_name]["sql_query"]
        query = self.analyze_query(query, data)

        depends_on_command = self.task[self.command_name]["depends_on"]
        depends_on_set = data[depends_on_command]

        data[self.command_name] = {}

        try:
            if self.data_node.connection == 0:
                self.data_node.connect()

            for row in depends_on_set:
                parent_id = row[0]
                row_query = self.analyze_query_item(query, parent_id)
                row_temp_data = self.data_node.pull(row_query)
                data[self.command_name][parent_id] = row_temp_data

            return True

        except ValueError as err:
            logger.warning("DB Error")
            return False

    def analyze_query(self, query, data=None):
        query = super().analyze_query(query, data)
        return query

    def analyze_query_item(self, query, parent_id=None):
        if query.find("$parent_id") > -1:
            return query.replace("$parent_id", f"{parent_id}")
        else:
            return query
