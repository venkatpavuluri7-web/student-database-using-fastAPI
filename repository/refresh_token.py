from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import RefreshToken
def insert_token(db:Session,data:RefreshToken):
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except IntegrityError:
        db.rollback()
        raise
def get_tokenby_gti(db:Session,token_id:str):
    stmt=Select(RefreshToken).where(RefreshToken.token_id==token_id)
    return db.execute(stmt).scalars().first()
def revoke_refresh_token(db:Session,token:RefreshToken):
   token.revokeed=True
   db.commit()
   db.refresh(token)


