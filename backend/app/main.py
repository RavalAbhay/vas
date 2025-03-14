from fastapi import Depends, FastAPI, HTTPException,status
from . import models
from .database import engine,get_db
from .schema import nuke
from sqlalchemy.orm import Session
# import psycopg2

models.Base.metadata.create_all(bind=engine)

# try:
#     conn = psycopg2.connect(host='localhost',database='vas',user='postgres',password='12345678')
#     cursor = conn.cursor()
#     print("connected")
# except Exception as e:
#     print('failed to connect')

app = FastAPI()     

@app.get('/')
def root():
    return "Hello!"

@app.get('/read')
def read(db: Session =Depends(get_db)):
    data = db.query(models.nuke).all()
    return data

@app.get('/read/{id}')
def read(id:int, db: Session =Depends(get_db)):
    data = db.query(models.nuke).filter(models.nuke.id==id).first()
    if data ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {id} does not exist")
    return data

@app.post('/new')
def add(row:nuke,db: Session =Depends(get_db)):
    #row.dict() converts class obj into dict and then with ** opened/unfolded it and automatically assigned all params
    #when there are too many columns it is hard to assign all params manually and this unfolding automatically does it
    new_row = models.nuke(**row.dict())     
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row

@app.delete('/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db: Session =Depends(get_db)):
    data = db.query(models.nuke).filter(models.nuke.id==id)
    if data.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {id} does not exist")
    data.delete(synchronize_session=False)
    db.commit()
    return "Success"

@app.put('/update/{id}')
def update(id: int, nuke: nuke, db: Session = Depends(get_db)):
    x = db.query(models.nuke).filter(models.nuke.id==id)
    y = x.first()
    if y== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id = {id} does not exist")
    x.update(nuke.dict(), synchronize_session=False)
    db.commit()