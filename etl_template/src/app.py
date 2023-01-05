import time

from tasks import TASKS, STAGES
from setup_logging import *

logger = setup_applevel_logger()


class ETLApp:
    """
    Приложение ETL
    """

    def __init__(self):
        """
        Собираем пайплайн ETL на основании того, как он описан в TASKS
        """
        self.pipeline = []
        for task_key in TASKS:
            task = TASKS[task_key]

            task_batch = {}
            for command_key in task:
                cur_stage = task[command_key]["stage"]
                callable_command = STAGES[cur_stage]
                task_batch[command_key] = callable_command(task, task_key, command_key)

            self.pipeline.append(task_batch)

    def loop_run(self):
        """
        Бесконечный цикл переноса данных
        """
        counter = 1
        while True:
            # перебираем цепочки задач
            for task_batch in self.pipeline:
                counter = counter + 1
                logger.info(f"\n\nLOOP CYCLE {counter} \n\n")

                data = {}
                task_complete_flag = True

                # прогоняем все команды в задаче,
                # запоминаем результат выполнения в кумулятивном флаге
                for command_key in task_batch:
                    data[command_key] = {}
                    command_flag = task_batch[command_key].run(data=data)
                    task_complete_flag = task_complete_flag and command_flag
                    if not command_flag:
                        break

                # если успех всей цепочки, то делаем подтверждение транзакции
                if task_complete_flag:
                    logger.info("Commit task")
                    for command_key in task_batch:
                        task_batch[command_key].commit(data=data)

                # если не успех хотя бы одной команды цепочки, то делаем откат всех команд
                else:
                    logger.info("Rollback task")
                    for command_key in task_batch:
                        task_batch[command_key].rollback(data=data)

                # пауза между командами
                time.sleep(1)


app = ETLApp()
app.loop_run()
