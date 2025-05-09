from pydantic import BaseModel, constr, StrictInt


class User(BaseModel):
    name : constr(min_length=1)
    age : StrictInt

