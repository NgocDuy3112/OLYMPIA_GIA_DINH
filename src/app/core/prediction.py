from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

import io
import re

from fastapi import HTTPException


from app.schema.prediction import *
from app.model.record import Record