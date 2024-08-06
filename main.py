from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.routers import router as router_contacts


app = FastAPI()

app.include_router(router_contacts, prefix="/contacts", tags=["contacts"])


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))  #.fetchone()  # Welcome to FastAPI!
        # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
        # 'coroutine' object has no attribute 'fetchone'
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connecting to the database")
