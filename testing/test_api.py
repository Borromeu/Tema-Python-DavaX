import os
import sys
import pytest
from fastapi.testclient import TestClient
from main import app  # import app and relevant modules for patching
import database.connectionDB as db_module
import functions.fibonacci as fib_module
import functions.factorial as fact_module
import functions.pow as pow_module

# Add project root to path so that all modules can be imported correctly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(autouse=True)
def client(monkeypatch):
    # Stub out save_operation to avoid real database writes during tests
    monkeypatch.setattr(db_module, "save_operation",
                        lambda *args, **kwargs: None)
    return TestClient(app)


# ----- Fibonacci POST tests -----

def test_post_fibonacci_success(monkeypatch, client):
    # Given: fibonacci(5) returns 5
    monkeypatch.setattr(fib_module, "fibonacci",
                        lambda n: 5 if n == 5 else None)

    # When: Posting n=5 to /fibonacci
    resp = client.post("/fibonacci", json={"n": 5})

    # Then: Response is 200 with correct JSON payload
    assert resp.status_code == 200
    assert resp.json() == {"operation": "fibonacci", "n": 5, "result": 5}


def test_post_fibonacci_invalid(monkeypatch, client):
    # Given: fibonacci() raises ValueError for negative input
    monkeypatch.setattr(
        fib_module,
        "fibonacci",
        lambda n: (_ for _ in ()).throw(ValueError(
            "Negative index not allowed for Fibonacci.")),
    )

    # When: Posting n=-1 to /fibonacci
    resp = client.post("/fibonacci", json={"n": -1})

    # Then: Response is 400 with error detail
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Negative index not allowed for Fibonacci."


# ----- Factorial POST tests -----

def test_post_factorial_success(monkeypatch, client):
    # Given: factorial(5) returns 120
    monkeypatch.setattr(fact_module, "factorial",
                        lambda n: 120 if n == 5 else None)

    # When: Posting n=5 to /factorial
    resp = client.post("/factorial", json={"n": 5})

    # Then: Response is 200 with correct JSON payload
    assert resp.status_code == 200
    assert resp.json() == {"operation": "factorial",
                           "n": 5, "result": 120}


def test_post_factorial_invalid(monkeypatch, client):
    # Given: factorial() raises ValueError for negative input
    monkeypatch.setattr(
        fact_module,
        "factorial",
        lambda n: (_ for _ in ()).throw(ValueError(
            "Factorial is undefined for negative numbers.")),
    )

    # When: Posting n=-3 to /factorial
    resp = client.post("/factorial", json={"n": -3})

    # Then: Response is 400 with error detail
    assert resp.status_code == 400
    assert (resp.json()["detail"] ==
            "Factorial is undefined for negative numbers.")


# ----- Power POST tests -----

def test_post_pow_success(monkeypatch, client):
    # Given: pow(2,3) returns 8.0
    monkeypatch.setattr(pow_module, "pow",
                        lambda b, e: 8.0 if (b, e) == (2, 3) else None)

    # When: Posting base=2, exp=3 to /pow
    resp = client.post("/pow", json={"base": 2, "exp": 3})
    data = resp.json()

    # Then: Response is 200 and result matches approximately 8.0
    assert resp.status_code == 200
    assert data["result"] == pytest.approx(8.0, abs=1e-6)
    assert data == {"operation": "pow",
                    "base": 2, "exp": 3, "result": data["result"]}


def test_post_pow_exception(monkeypatch, client):
    # Given: pow() throws generic Exception on invalid args
    monkeypatch.setattr(
        pow_module,
        "pow",
        lambda b, e: (_ for _ in ())
        .throw(Exception("Base and exponent "
                         "must be positive for logarithmic exponentiation.")),
    )

    # When: Posting an invalid request to /pow
    resp = client.post("/pow", json={"base": 2, "exp": -1})

    # Then: Response is 400 with correct detail message
    assert resp.status_code == 400
    assert (resp.json()["detail"] ==
            "Base and exponent "
            "must be positive for logarithmic exponentiation.")


# ----- Power GET tests -----

def test_get_pow_query_exact(monkeypatch, client):
    # Given: pow(2,4) returns 16.0
    monkeypatch.setattr(pow_module, "pow",
                        lambda b, e: 16.0 if (b, e) == (2, 4) else None)

    # When: Querying /pow?base=2&exp=4
    resp = client.get("/pow?base=2&exp=4")
    data = resp.json()

    # Then: Response is 200 and all values approx match
    assert resp.status_code == 200
    assert data["result"] == pytest.approx(16.0, abs=1e-6)
    assert data["base"] == pytest.approx(2.0, abs=1e-6)
    assert data["exp"] == pytest.approx(4.0, abs=1e-6)


def test_get_pow_query_fractional(monkeypatch, client):
    # Given: pow module uses real exponentiation for fractional
    monkeypatch.setattr(pow_module, "pow", lambda b, e: b ** e)

    # When: Querying /pow?base=9&exp=0.5
    resp = client.get("/pow?base=9&exp=0.5")
    data = resp.json()

    # Then: sqrt(9) approx 3.0 and parameters returned correctly
    assert resp.status_code == 200
    assert data["result"] == pytest.approx(3.0, rel=1e-6)
    assert data["base"] == pytest.approx(9.0, rel=1e-6)
    assert data["exp"] == pytest.approx(0.5, rel=1e-6)


# ----- Fibonacci GET tests -----

def test_get_fibonacci_query_success(monkeypatch, client):
    # Given: fibonacci(7) returns 13
    monkeypatch.setattr(fib_module, "fibonacci",
                        lambda n: 13 if n == 7 else None)

    # When: GET /fibonacci?n=7
    resp = client.get("/fibonacci?n=7")

    # Then: Returns correct operation JSON
    assert resp.status_code == 200
    assert resp.json() == {"operation": "fibonacci", "n": 7, "result": 13}


# ----- Factorial GET tests -----

def test_get_factorial_query_success(monkeypatch, client):
    # Given: factorial(6) returns 720
    monkeypatch.setattr(fact_module, "factorial",
                        lambda n: 720 if n == 6 else None)

    # When: GET /factorial?n=6
    resp = client.get("/factorial?n=6")

    # Then: Returns correct operation JSON
    assert resp.status_code == 200
    assert resp.json() == {"operation": "factorial", "n": 6, "result": 720}
