from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from calculs import calculer

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Valeurs par défaut du TP (concentrations en %)
DEFAUTS = {
    "m0": 1000, "x0": 10, "residus": 20, "mR": 100, "xR": 40,
    "Cp": 3.8, "T2": 20, "T3": 80, "x4": 40,
    "lambda_v": 2300, "T4": 80, "T5": 25,
}


def calculer_depuis_formulaire(v, **modifs):
    """Convertit les % en fractions, puis appelle calculer()."""
    p = dict(v)
    p.update(modifs)
    return calculer(
        m0=p["m0"], x0=p["x0"] / 100, residus=p["residus"],
        mR=p["mR"], xR=p["xR"] / 100, Cp=p["Cp"],
        T2=p["T2"], T3=p["T3"], x4=p["x4"] / 100,
        lambda_v=p["lambda_v"], T4=p["T4"], T5=p["T5"],
    )


def courbes(v):
    """Calcule les points des deux graphiques."""
    concentrations = list(range(40, 51))   # 40 % à 50 %
    temperatures = list(range(80, 91))     # 80 °C à 90 °C
    return {
        "x4": concentrations,
        "vapeur": [round(calculer_depuis_formulaire(v, x4=x)["mv"], 2)
                   for x in concentrations],
        "T3": temperatures,
        "chauffage": [round(calculer_depuis_formulaire(v, T3=t)["Q3"], 2)
                      for t in temperatures],
    }


@app.get("/")
def accueil(request: Request):
    return templates.TemplateResponse(
        request, "index.html",
        {"valeurs": DEFAUTS, "resultats": None, "courbes": courbes(DEFAUTS)},
    )


@app.post("/")
def calcul(
    request: Request,
    m0: float = Form(...), x0: float = Form(...),
    residus: float = Form(...), mR: float = Form(...),
    xR: float = Form(...), Cp: float = Form(...),
    T2: float = Form(...), T3: float = Form(...),
    x4: float = Form(...), lambda_v: float = Form(...),
    T4: float = Form(...), T5: float = Form(...),
):
    valeurs = {
        "m0": m0, "x0": x0, "residus": residus, "mR": mR, "xR": xR,
        "Cp": Cp, "T2": T2, "T3": T3, "x4": x4,
        "lambda_v": lambda_v, "T4": T4, "T5": T5,
    }
    resultats = calculer_depuis_formulaire(valeurs)
    return templates.TemplateResponse(
        request, "index.html",
        {"valeurs": valeurs, "resultats": resultats, "courbes": courbes(valeurs)},
    )