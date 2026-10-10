import random
import pandas as pd

random.seed(42)

# -----------------------------------------
# CONFIGURACIÓN
# -----------------------------------------
N = 52

ORDEN_DIFICULTAD = [
    "Nunca",
    "Rara vez",
    "Algunas veces",
    "Frecuentemente",
    "Siempre"
]

GASTOS = [
    "Transporte",
    "Alimentación",
    "Materiales escolares",
    "Internet y servicios digitales",
    "Colegiatura o cuotas escolares"
]

# Distribuciones ilustrativas para los datos sintéticos.
PESOS_GASTOS = [20, 30, 10, 8, 22]
PESOS_DIFICULTAD = [10, 20, 35, 25, 10]


def generar_simulados(n):
    filas = []

    for i in range(n):
        gasto = random.choices(
            GASTOS, weights=PESOS_GASTOS, k=1
        )[0]

        dificultad = random.choices(
            ORDEN_DIFICULTAD,
            weights=PESOS_DIFICULTAD,
            k=1
        )[0]

        # Montos ilustrativos en pesos mexicanos.
        # No representan una estimación de la población.
        monto = random.randrange(300, 6001, 100)

        filas.append({
            "Monto": monto,
            "Gasto_principal": gasto,
            "Dificultad": dificultad
        })

    return pd.DataFrame(filas)


# -----------------------------------------
# GENERAR Y GUARDAR DATOS SINTÉTICOS
# -----------------------------------------
simulados = generar_simulados(N)

simulados.to_excel(
    "52_respuestas_simuladas.xlsx",
    index=False
)

simulados.to_csv(
    "52_respuestas_simuladas.csv",
    index=False,
    encoding="utf-8-sig"
)

print(f"Registros sintéticos generados: {len(simulados)}")
