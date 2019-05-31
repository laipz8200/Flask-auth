from app.extensions import db

Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD operations."""
    @classmethod
    def order_by(cls, *args, **kwargs):
        """Sort records except is_deleted."""
        return cls.query.order_by(*args, **kwargs).filter_by(is_deleted=False)

    @classmethod
    def paginate(cls, *args, **kwargs):
        """Returns ``per_page`` items from page ``page``.

        If ``page`` or ``per_page`` are ``None``, they will be retrieved from
        the request query. If ``max_per_page`` is specified, ``per_page`` will
        be limited to that value. If there is no request or they aren't in the
        query, they default to 1 and 20 respectively. If ``count`` is ``False``,
        no query to help determine total page count will be run.

        When ``error_out`` is ``True`` (default), the following rules will
        cause a 404 response:

        * No items are found and ``page`` is not 1.
        * ``page`` is less than 1, or ``per_page`` is negative.
        * ``page`` or ``per_page`` are not ints.

        When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
        1 and 20 respectively.

        Returns a :class:`Pagination` object.
        """
        return cls.query.filter_by(
            is_deleted=False
        ).paginate(*args, **kwargs)

    @classmethod
    def all(cls):
        """Get all record from the database except is_deleted."""
        return cls.query.filter_by(is_deleted=False).all()

    @classmethod
    def count(cls):
        """Count the number of records except is_deleted."""
        return cls.query.filter_by(is_deleted=False).count()

    @classmethod
    def filter_by(cls, *args, **kwargs):
        """
        apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        Exclude invalid records.(is_deleted)
        """
        return cls.query.filter_by(*args, **kwargs).filter_by(is_deleted=False)

    @classmethod
    def filter(cls, *args, **kwargs):
        """
        apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        Exclude invalid records.(is_deleted)
        """
        return cls.query.filter(*args, **kwargs).filter_by(is_deleted=False)

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
