from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///product.sqlite3')
Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    genre = Column(String(20))
    name = Column(String(50))
    description = Column(String(255))
    image = Column(String(50))
    url = Column(String(100))
    favorit = Column(Boolean())

    def __init__(self, genre, name, description, image, url):
        self.genre = genre
        self.name = name
        self.description = description
        self.image = image
        self.url = url
        self.favorit = False



# insert
def create(genre:str, name:str, description:str, image:str, url:str):
    
    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()

    data = Product(genre, name, description, image, url)

    ses.add(data)
    ses.commit()
    ses.close()


def read_all():
    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()

    data = ses.query(Product).all()
    ses.close()
    return data


def read_id(id):
    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()

    data = ses.query(Product).filter(Product.id==id)[0]
    ses.close()
    return data


def chage_favorit(id):
    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()

    data = ses.query(Product).filter(Product.id==id)[0]
    data.favorit = not data.favorit
    ses.commit()
    ses.close()


def read_genre(genre):
    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()

    if genre == 'sofa':
        genre_str = 'ソファ'
    elif genre == 'shelf':
        genre_str = 'シェルフ'

    data = ses.query(Product).filter(Product.genre==genre_str)
    ses.close()
    return data

def read_favorit():
    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()
    
    data = ses.query(Product).filter(Product.favorit==True)
    ses.close()
    return data


def initDB():
    """csvデータをまとめて登録"""

    # 削除
    import os
    os.remove('./product.sqlite3')

    # 新規立ち上げ
    Base.metadata.create_all(engine)

    # csvをまとめて立ち上げ
    import pandas as pd
    df = pd.read_csv('./csv/init.csv')
    # print(df)

    data = []
    for r in df.itertuples():
        data.append(Product(r.genre, r.name, r.description, r.image, r.url))

    # session作成
    Session = sessionmaker(bind=engine)
    ses = Session()

    ses.add_all(data)
    ses.commit()
    ses.close()

# # DB作成
# Base.metadata.create_all(engine)

# # 単体で入れる場合
# genre = 'ソファ'
# name = 'ソファ1'
# description = 'ソファ1です'
# image = 'image1.png'
# create(genre, name, description, image)

# csvデータをまとめて入力
initDB()

