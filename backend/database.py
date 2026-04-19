import sqlalchemy as sa

if not hasattr(sa, '__all__'):
    sa.__all__ = tuple(name for name in dir(sa) if not name.startswith('_'))

if hasattr(sa, 'orm') and not hasattr(sa.orm, '__all__'):
    sa.orm.__all__ = tuple(name for name in dir(sa.orm) if not name.startswith('_'))

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
