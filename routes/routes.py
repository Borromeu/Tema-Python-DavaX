from fastapi import FastAPI, HTTPException, Query
import math
from contextlib import asynccontextmanager
from database.connectionDB import app, get_db_connection, init_db, save_operation
from functions.fibonacci import fibonacci

# Set the lifespan of the server app
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# This method will get and display the rows that used the pow operation
@app.get("/pow")
def compute_power(base: float = Query(...), exp: float = Query(...)):
    result = math.pow(base, exp)
    save_operation("pow", f"{base}^{exp}", str(result))
    return {"operation": "pow", "base": base, "exp": exp, "result": result}

# This method will get and display a row that used the fibonacci operation
@app.get("/fibonacci")
def compute_fibonacci(n: int = Query(..., ge=0)):
    try:
        result = fibonacci(n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    save_operation("fibonacci", f"n={n}", str(result))
    return {"operation": "fibonacci", "n": n, "result": result}

# This method will get and display a row that used the fibonacci operation
@app.get("/factorial")
def compute_factorial(n: int = Query(..., ge=0)):
    try:
        result = math.factorial(n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    save_operation("factorial", f"n={n}", str(result))
    return {"operation": "factorial", "n": n, "result": result}

# This method is used to display an historian of all operations that have been
# executed and saved
@app.get("/history")
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM operations ORDER BY timestamp DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]