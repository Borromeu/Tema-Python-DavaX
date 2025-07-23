from fastapi import APIRouter, HTTPException, Query
import math
from database.connectionDB import get_db_connection, save_operation
from functions.fibonacci import fibonacci
from model.fibonacci_input_model import FibonacciInput
from model.factorial_input_model import FactorialInput
from model.power_input_model import PowerInput

# We define the router to call the routes
router = APIRouter()


# Post method for inserting and saving a fibonacci operation in database
@router.post("/fibonacci")
def post_fibonacci(data: FibonacciInput):
    try:
        result = fibonacci(data.n)
        save_operation("fibonacci", f"n={data.n}", str(result))
        return {
            "operation": "fibonacci",
            "n": data.n,
            "result": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



# Post method for inserting and saving a factorial operation in database
@router.post("/factorial")
def post_factorial(data: FactorialInput):
  try:
      result = factorial(data.n)
      save_operation("fibonacci", f"n={data.n}", str(result))
      return {
          "operation": "factorial",
          "n": data.n,
          "result": result
      }
      except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


#Post method for inserting and saving a power operation in database
@router.post("/pow")
def post_power(data: PowerInput):
    try:
        result = math.pow(data.base, data.exp)
        save_operation("pow", f"{data.base}^{data.exp}", str(result))
        return {
            "operation": "pow",
            "base": data.base,
            "exp": data.exp,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# This method will get and display the rows that used the pow operation
@router.get("/pow")
def compute_power(base: float = Query(...), exp: float = Query(...)):
    result = math.pow(base, exp)
    save_operation("pow", f"{base}^{exp}", str(result))
    return {"operation": "pow", "base": base, "exp": exp, "result": result}



# This method will get and display a row that used the fibonacci operation
@router.get("/fibonacci")
def compute_fibonacci(n: int = Query(..., ge=0)):
    try:
        result = fibonacci(n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    save_operation("fibonacci", f"n={n}", str(result))
    return {"operation": "fibonacci", "n": n, "result": result}



# This method will get and display a row that used the fibonacci operation
@router.get("/factorial")
def compute_factorial(n: int = Query(..., ge=0)):
    try:
        result = math.factorial(n)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    save_operation("factorial", f"n={n}", str(result))
    return {"operation": "factorial", "n": n, "result": result}



# This method is used to display an historian of all operations that have been
# executed and saved
@router.get("/history")
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM operations ORDER BY timestamp DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/history/fibonacci")
def get_fibonacci_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM operations WHERE operation = 'fibonacci' ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/history/factorial")
def get_factorial_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM operations WHERE operation = 'factorial' ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/history/pow")
def get_fibonacci_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT * FROM operations WHERE operation = 'pow' ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]