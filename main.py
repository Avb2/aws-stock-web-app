from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import dotenv
from models.mySQLobj import MySQLDB
from fastapi import Form
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")
dotenv.load_dotenv()






@app.get("/", response_class=HTMLResponse)
def getIndex(request: Request):
    return templates.TemplateResponse("index.html",
                                      {
                                          "request": request
                                      })


@app.get("/stock/{name}", response_class=HTMLResponse)
async def searchStock(name, request: Request):
    ### Get this data from db and pass it to Jinja2 template
    db = MySQLDB(
        host="aws-stock.cluster-cyza8yaoc0cn.us-east-1.rds.amazonaws.com",
        db="stockInfo",
        port=3306,
        user=os.getenv("USERDB"),
        password=os.getenv("USERPWD")
    )

    connection = await db.get_conn()

    async with connection.cursor() as cursor:

        stmt = "SELECT `price` FROM info WHERE `name`=%s"
        try:
            await cursor.execute(stmt, (name,))

            result = await cursor.fetchone()

            return templates.TemplateResponse("stock_page.html", {
                "request": request,
                "name": name,
                "price": result.get("price")
            })
        except:
            return templates.TemplateResponse("stock_page.html", {
            "request": request,
            "name": name
        })


@app.get("/new-stock", response_class=HTMLResponse)
def new_stock_page(request: Request):
    return templates.TemplateResponse("new_stock.html", {
        "request": request
    })



@app.post("/create")
async def create_new_stock(name: str = Form(...), price: str = Form(...)):
    db = MySQLDB(
        host="aws-stock.cluster-cyza8yaoc0cn.us-east-1.rds.amazonaws.com",
        db="stockInfo",
        port=3306,
        user=os.getenv("USERDB"),
        password=os.getenv("USERPWD")
    )

    connection = await db.get_conn()


    async with connection.cursor() as cursor:
        insertStmt = "INSERT INTO info VALUES (%s, %d)"
        await cursor.execute(insertStmt, (name, float(price)))

