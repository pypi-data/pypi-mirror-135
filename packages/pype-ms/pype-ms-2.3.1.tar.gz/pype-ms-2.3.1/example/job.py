from pype.baseconfig import BaseConfig


class Config(BaseConfig):
    script_path = "example/job.py"
    params = {"append": "good day"}
    outputs = {"msg": "msg.txt"}


def main(config, logger):
    logger.info('running job')
