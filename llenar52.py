import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = (
    "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?"
    "id=lWO64WR6kkuq86fAIMPRj0DnTb2o6IhJt3FHWDmocd5UMElMNTc1QkJPOVQxOTJDRFJZNU8xRUVEOS4u"
)

ARCHIVO = "52_respuestas_simuladas copy.csv"

GASTOS_VALIDOS = {
    "Transporte",
    "Alimentación",
    "Materiales escolares",
    "Internet y servicios digitales",
    "Colegiatura o cuotas escolares",
    "Otros",
}

DIFICULTADES_VALIDAS = {
    "Nunca",
    "Rara vez",
    "Algunas veces",
    "Frecuentemente",
    "Siempre",
}

df = pd.read_csv(ARCHIVO, encoding="utf-8-sig")

columnas = {"Monto", "Gasto_principal", "Dificultad"}
if not columnas.issubset(df.columns):
    raise ValueError(
        f"El CSV debe contener estas columnas: {columnas}"
    )

if df.empty:
    raise ValueError("El CSV no contiene registros.")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    # Se carga una fila por vez para validar el formulario.
    for indice, fila in df.iterrows():
        monto = str(fila["Monto"]).strip()
        gasto = str(fila["Gasto_principal"]).strip()
        dificultad = str(fila["Dificultad"]).strip()

        # Validar antes de abrir o rellenar el formulario.
        try:
            valor = float(monto)
            assert valor > 0
        except (ValueError, AssertionError):
            print(f"Fila {indice + 1}: monto inválido.")
            continue

        if gasto not in GASTOS_VALIDOS:
            print(f"Fila {indice + 1}: gasto no válido: {gasto}")
            continue

        if dificultad not in DIFICULTADES_VALIDAS:
            print(
                f"Fila {indice + 1}: dificultad no válida: "
                f"{dificultad}"
            )
            continue

        print(f"\nPreparando fila {indice + 1}")
        driver.get(URL)

        # Pregunta 1: monto mensual.
        campo_monto = wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                'input[data-automation-id="textInput"]'
                '[placeholder="Please enter a number greater than 0"]'
            ))
        )
        campo_monto.clear()
        campo_monto.send_keys(monto)

        # Pregunta 2: grupo que contiene la opción Transporte.
        grupo_gasto = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@role="radiogroup"]'
                '[.//input[@value="Transporte"]]'
            ))
        )
        opcion_gasto = grupo_gasto.find_element(
            By.XPATH,
            './/input[@type="radio" and @value="' + gasto + '"]'
        )
        driver.execute_script(
            "arguments[0].click();", opcion_gasto
        )

        # Pregunta 3: grupo que contiene la opción Nunca.
        grupo_dificultad = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[@role="radiogroup"]'
                '[.//input[@value="Nunca"]]'
            ))
        )
        opcion_dificultad = grupo_dificultad.find_element(
            By.XPATH,
            './/input[@type="radio" and @value="'
            + dificultad + '"]'
        )
        driver.execute_script(
            "arguments[0].click();", opcion_dificultad
        )

        # Verificar que el navegador conserva las selecciones.
        monto_actual = campo_monto.get_attribute("value")
        gasto_marcado = opcion_gasto.is_selected()
        dificultad_marcada = opcion_dificultad.is_selected()

        print("Monto:", monto_actual)
        print("Gasto seleccionado:", gasto_marcado)
        print("Dificultad seleccionada:", dificultad_marcada)
        print(
            "Formulario rellenado, pero NO enviado. "
            "Revisa los campos antes de continuar."
        )

        input(
            "Pulsa Enter para pasar a la siguiente fila "
            "o cierra el programa para detenerlo..."
        )

finally:
    driver.quit()