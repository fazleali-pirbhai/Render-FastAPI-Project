from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#DB Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 



#Read specific blog
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def show_specific_blog(id:int, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    return blog



#Home
@app.get("/")
def home():
    return{
        "message": "Blog API Started"
    }

#Create Blog
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db:Session=Depends(get_db)):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Read all blogs
@app.get("/blogs", response_model=list[schemas.BlogResponse])
def show_all_blogs(db:Session=Depends(get_db)):
    return db.query(models.Blog).all()



