from etl_command import ETLCommand
from setup_logging import *

logger = get_logger()


class ETLTransformer(ETLCommand):
    def __init__(self, task, task_name, command_name):
        super().__init__(task, task_name, command_name)
        self.log_signature("INIT")

        transform_node_callable = self.task[command_name]["worker"]
        self.transform_node = transform_node_callable(self.task)
        self.depends_on = self.task[command_name]["depends_on"]
        self.enrich_with = self.task[command_name]["enrich_with"]

    def run(self, data=None):
        self.log_signature("RUN")
        data_table = data[self.depends_on]
        enrich_table = {}

        for key in self.enrich_with:
            enrich_table[key] = data[self.enrich_with[key]]

        transformed_data = self.transform_node.transform(data_table, enrich_table)
        data[self.command_name] = transformed_data
        print(transformed_data)
        return True

    def commit(self, data=None):
        pass

    def rollback(self, data=None):
        pass
