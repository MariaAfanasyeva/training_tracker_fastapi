import sqlachemy
from fastapi import APIRouter, Depends, HTTPException, Request

from training_tracker.database import trainings
from training_tracker.models.schemas import Training

