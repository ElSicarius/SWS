
from src.arguments import get_parser
from src.session import Session
from loguru import logger

if __name__ == '__main__':

    arguments = get_parser()
    session = Session(arguments.project_path)
    arguments.func(arguments, session)
    session.save()
    logger.warning(session)
