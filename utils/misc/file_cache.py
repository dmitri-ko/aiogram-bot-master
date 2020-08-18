import logging
import os
from loader import bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils.db_api.db_map import Base, MediaIds
from data.config import DB_FILENAME


class TelegramFileCache():
    engine = create_engine(f'sqlite:///{DB_FILENAME}')
    if not os.path.isfile(f'./{DB_FILENAME}'):
        Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    def __init__(self):
        pass

    def get_id(self, media_name:str) -> str:
        session = self.Session()
        try:
            q = session.query(MediaIds).filter_by(filename=media_name).all()
            for row in q:
               return row.file_id 
        except Exception as e:
            logging.error(
                'Couldn\'t get id for {}. Error is {}'.format(media_name, e))
            return None   
        finally:
            session.close()  
            
    async def generate_id(self, media_name:str, chat_id: int) -> str:
        with open(media_name, 'rb') as file:
            msg = await bot.send_photo(chat_id, file, disable_notification=True)
            file_id = msg.photo[-1].file_id

            session = self.Session()
            newItem = MediaIds(file_id=file_id, filename=media_name)
            try:
                session.add(newItem)
                session.commit()
            except Exception as e:
                logging.error(
                    'Couldn\'t upload {}. Error is {}'.format(media_name, e))
                return None    
            else:
                logging.info(
                    f'Successfully uploaded and saved to DB file {media_name} with id {file_id}')  
            finally:
                session.close()       
            return file_id      