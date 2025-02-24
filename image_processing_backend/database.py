from sqlalchemy import Column, String, Integer, Text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ImageRequest(Base):
    __tablename__ = "image_requests"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    input_urls = Column(Text, nullable=False)
    output_urls = Column(Text, nullable=True)
    status = Column(Enum("Pending", "Processing", "Completed", name="status"), default="Pending")

DATABASE_URL = "postgresql://myuser:newpassword@localhost/image_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
