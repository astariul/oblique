"""Declaration of the DB model."""
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from oblique.database import Base


class Package(Base):
    """Table representing a Python Package registered in PyPi."""

    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    last_updated = Column(DateTime)
    name = Column(String, unique=True, index=True)

    releases = relationship("Release", back_populates="package", passive_deletes=True)


class Release(Base):
    """Table representing a single release of a python package."""

    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    date = Column(DateTime)
    is_yanked = Column(Boolean, default=False)
    package_id = Column(Integer, ForeignKey("packages.id", ondelete="CASCADE"))

    package = relationship("Package", back_populates="releases")
