from pydantic import BaseModel


class ResponseModel(BaseModel):

  status_message: str = 'OK',
  content: dict
