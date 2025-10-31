from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import io
import re

from fastapi import HTTPException

from app.schema.prediction import *
from app.model.record import Record
from app.model.answer import Answer
from app.model.question import Question
from app.model.match import Match