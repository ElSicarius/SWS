
from src.arguments import get_parser
from src.session import Session
from loguru import logger

if __name__ == '__main__':

    arguments = get_parser()
    session = Session(arguments)
    session.load_session()
    arguments.func(arguments, session)
    session.save()
    logger.success(session)
