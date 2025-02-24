from sqlalchemy import Column, String, Integer, Text, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database import Base 

class ImageRequest(Base):
    __tablename__ = "image_requests"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    input_urls = Column(Text, nullable=False)
    output_urls = Column(Text, nullable=True)
    status = Column(Enum("Pending", "Processing", "Completed", name="status"), default="Pending")

    __table_args__ = {"extend_existing": True}  # Prevents redefinition error
