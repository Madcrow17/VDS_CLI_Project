class Command:
    def execute(self, args):
        raise NotImplementedError


class CopyCommand(Command):
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def execute(self, args):
        if len(args) != 2:
            print("Ошибка: команда copy требует 2 аргумента: источник и назначение")
            print(args)
            return
        src, dest = args
        self.file_manager.copy(src, dest)


class DeleteCommand(Command):
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def execute(self, args):
        if len(args) != 1:
            print("Ошибка: команда delete требует 1 аргумент — путь к файлу или папке")
            return
        path = args[0]
        self.file_manager.delete(path)
