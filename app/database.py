from app.extensions import db
from sqlalchemy import and_

Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD operations."""
    @classmethod
    def all(cls):
        """Get all record from the database except is_deleted."""
        return cls.query.filter_by(is_deleted=False).all()

    @classmethod
    def filter_by(cls, **kwargs):
        """
        apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        Exclude invalid records.(is_deleted)
        """
        return cls.query.filter_by(is_deleted=False, **kwargs)

    @classmethod
    def filter(cls, *criterion):
        """
        apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        Exclude invalid records.(is_deleted)
        """
        conditions = (and_(cls.is_deleted == 0, *criterion), )
        return cls.query.filter(*conditions)

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it in the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record.  """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Mark record as deleted in the database."""
        self.update(is_deleted=True)
        return commit and self.save() or self

    def remove(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that include CRUD convenience methods."""
    __abstract__ = True


class SurrogateBaseKey(object):
    """
    A mixin that adds some base key column to any declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = Column(db.Integer, primary_key=True)
    is_deleted = Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by id """
        if any(
            (isinstance(record_id, (str, bytes)) and record_id.isdigit(),
             isinstance(record_id, (int, float)))
        ):
            record = cls.query.get(int(record_id))
            if not record.is_deleted:
                return record
        return None
