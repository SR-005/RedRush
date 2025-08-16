import sqlite3
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
'''from fastapi.staticfiles import StaticFiles'''
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

#--------------------------------SQL SETUP--------------------------------

conn = sqlite3.connect("donors.db", check_same_thread=False)
cursor = conn.cursor() 

cursor.execute("DROP TABLE IF EXISTS DONORS")
cursor.execute("CREATE TABLE IF NOT EXISTS DONORS(NAME TEXT, BLOODGROUP TEXT, PHONE TEXT, LOCATION TEXT, EMAIL TEXT)")
conn.commit()

#--------------------------------APP--------------------------------
app=FastAPI(title="RedRush", description="Instant Blood Donor Matcher")


'''app.mount("/static", StaticFiles(directory="static"), name="static")'''
templates = Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
def home(request: Request):     
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
def search_donors(request: Request, bloodgroup: str = Form(...)):
    cursor.execute("SELECT name, phone, location, email FROM donors WHERE bloodgroup = ?", (bloodgroup,))
    donors = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "donors": donors})

@app.get("/add_donor", response_class=HTMLResponse)
def add_donor_page(request: Request):
    return templates.TemplateResponse("donor.html", {"request": request})


@app.post("/add_donor", response_class=HTMLResponse)
def add_donor(
    request: Request, 
    name: str = Form(...), 
    bloodgroup: str = Form(...), 
    phone: str = Form(...), 
    location: str = Form(...),
    email: str = Form(...)
):
    cursor.execute("INSERT INTO DONORS (name, bloodgroup, phone, location, email) VALUES (?, ?, ?, ?, ?)",
                   (name, bloodgroup, phone, location, email))
    conn.commit()
    return RedirectResponse("/", status_code=303)