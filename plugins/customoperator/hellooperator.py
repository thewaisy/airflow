from airflow.models.baseoperator import BaseOperator


class HelloOperator(BaseOperator):
    ui_color = '#ff0000' # ui상의 아이콘 색
    ui_fgcolor = '#0000ff' # ui상의 폰트 색


    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name

    def execute(self, context):
        message = "Hello {}".format(self.name)
        print(message)
        return message
