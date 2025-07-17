"""
This file makes the SQLAlchemy models available
at the package level, simplifying imports in other parts of the application.
"""
from .expense import Expense, expense_participants
from .group import Group, group_members
from .user import User
