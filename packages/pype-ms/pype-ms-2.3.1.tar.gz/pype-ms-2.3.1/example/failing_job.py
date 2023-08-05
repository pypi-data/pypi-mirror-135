from pype.baseconfig import BaseConfig


class Config(BaseConfig):
    script_path = "example/failing_job.py"

def main(config, logger):
    _ = config
    1/0
