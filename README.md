# Tema-Python

## Resurse:



- fastapi	The main web framework


- uvicorn	Runs the FastAPI app as a local web server


- pydantic	Data validation & serialization


- flake8	(Optional) Linting / clean code checker

-pip install fastapi uvicorn pydantic flake8



- the pow function

- the n-th fibbonaci number

- the factorial of the number

Multiple threads!!!



## 📘 Tutorial de utilizare a aplicației de înregistrare a operațiilor matematice cu FastAPI


### 💻 Pasul 1 – Clonarea repository-ului în PyCharm
Vom clona repo-ul din GitHub în PyCharm folosind comanda:

bash

git clone Borromeu/Tema-Python-DavaX



### 📦 Pasul 2 – Crearea venv-ului si instalarea pachetelor necesare
Pentru inceput, user-ul va crea un environment separat (venv) astfel incat acesta sa poata testa si instala local pachetele

Dupa care, pentru ca programul să funcționeze cum trebuie, vom instala următoarele pachete:

- fastapi – pentru framework-ul web FastAPI

- uvicorn – pentru a rula aplicația drept un server web local

- pydantic – pentru serializarea și validarea datelor

- flake – pentru lintare (verifică cât de curat este scris codul)

Comandă instalare:

bash

pip install fastapi uvicorn pydantic flake8 pytest httpx



### 🧠 Pasul 3 – Rularea scripturilor în Python
#### ▶️ Pasul 3.1 – Rularea scriptului main.py 
Scop:
Lansează execuția aplicației, creează și deschide serverul web local, și definește rutele pentru operații și istoricul acestora.



#### 🧾 Pasul 3.2 – Modele de input pentru operații
Pentru a salva datele în baza de date, va fi nevoie să definim structura modelelor de input-uri ale operațiilor astfel încât să putem verifica dacă datele sunt existente în momentul în care verificăm existența rutelor.
- Cream directorul model
- Adăugăm următoarele modele: 3.2.a: fibonacci_input_model.py3.2.b: factorial_input_model.py3.2.c: power_input_model.py



#### 📐 Pasul 3.3 – Funcții de calcul
Adăugăm următoarele scripturi de calcule matematice:

- 4.3.a: fibonacci.py

- 4.3.b: factorial.py

- 4.3.c: pow.py



#### 🗃️ Pasul 3.4 – Scriptul connectionDB.py
Scop:
Să genereze o bază de date SQLite care salvează datele operațiilor efectuate.



#### 🔁 Pasul 3.5 – Executarea metodelor rutelor
Folosim APIRouter() pentru definirea rutelor GET și POST:

- POST – inserare și salvare date

- GET – verificare existență date

#### Scopul:
Să putem accesa:

- istoricul tuturor operațiilor;

- istoricul filtrat per operație;

- o linie specifică de date în funcție de valorile introduse.



### 🚀 Pasul 4 – Execuția server-ului
Deschidem terminalul din PyCharm și rulăm comanda:

bash

python -m uvicorn main:app --reload --port 8080



### 🧪 Pasul 5 – Inserarea datelor cu Postman
Exemplu pentru POST Fibonacci:

Setăm metoda POST

URL: http://localhost:8080/fibonacci

Body → raw → JSON:

json

{ "n": 10 }

Click pe Send



### 🔍 Pasul 6 – Verificarea apelurilor
#### ✅ Opțiunea 1 – Din Postman:
Metoda GET

Introduci URL-ul corespunzător

Click Send

#### ✅ Opțiunea 2 – Direct din browser:
http

http://localhost:8080/fibonacci?n=10

## 🔗 Exemple de apeluri
#### Fibonacci of 10:
http://localhost:8080/fibonacci?n=10

#### 2 la puterea 5:
http://localhost:8080/pow?base=2&exp=5

#### Factorial of 6:
http://localhost:8080/factorial?n=6

#### Istoric complet:
http://localhost:8080/history

#### Istoric Fibonacci:
http://localhost:8080/history/fibonacci

#### Istoric Factorial:
http://localhost:8080/history/factorial

#### Istoric Power:
http://localhost:8080/history/pow

## Membrii echipei:
- ### Andrei Alexandru Gheorghe
- ### Adelin Andrei Fulop
- ### Alexandru Alin Potângă
