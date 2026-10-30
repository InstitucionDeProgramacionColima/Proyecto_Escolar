# ==========================================
# Encabezados y Librerias
# ==========================================
import os
import json
from typing import Optional, List, Dict, Any

try:
    from google import genai
    from google.genai import types
    TIENE_GOOGLE_GENAI = True
except ImportError:
    genai = None  # type: ignore
    types = None  # type: ignore
    TIENE_GOOGLE_GENAI = False

# ==========================================
# Declaracion de Constantes
# ==========================================
MODELO_GEMINI_DEFAULT = "gemini-2.0-flash"
MODELOS_DISPONIBLES = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-flash",
    "gemini-1.5-pro",
]
TEMPERATURA_DEFAULT = 0.2
MAX_TOKENS_DEFAULT = 1500

_modelo_activo_cache: Optional[str] = None

PROMPT_SISTEMA_BASE = """
Eres un analista financiero experto y asesor de crédito integrado en el Simulador de Préstamos.
Tus funciones y restricciones estrictas son las siguientes:
1. ÚNICAMENTE debes responder, interpretar, opinar o generar reportes sobre:
   a) Los datos numéricos de préstamos, tablas de amortización, indicadores financieros (TIR, CAT, total de intereses pagados) y gráficas generadas por el simulador.
   b) Los archivos generados por el simulador: el formato del archivo (.pdf o .xlsx de Excel), la carpeta donde se guardan (la ruta seleccionada por el usuario en la interfaz o carpeta predeterminada) y si se pueden modificar (los archivos Excel .xlsx son editables libremente en hojas de cálculo, mientras que los archivos .pdf son documentos formales de solo lectura pensados como dictamen final, aunque pueden editarse con lectores/editores de PDF).
2. NO realices nuevos cálculos manuales ni inventes fórmulas: opera y confía únicamente en las cifras exactas provistas por el sistema de cálculo en C++.
3. Si el usuario te hace preguntas o consultas ajenas a préstamos, finanzas personales o a los archivos generados y resultados calculados, responde amablemente y de forma tajante: "Solo puedo responder y asesorar sobre los datos y resultados financieros del simulador de préstamos y sobre los archivos generados (formato, ubicación y posibilidad de modificación)."
4. Sé profesional, claro, estructurado y explicativo para cualquier persona.
"""

# ==========================================
# Declaracion de Funciones Auxiliares
# ==========================================

def _obtener_ruta_configuracion() -> str:
    """Retorna la ruta absoluta del archivo config.json."""
    dir_modulo = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(dir_modulo, "..", "config.json"))


def _obtener_clave_api() -> Optional[str]:
    """
    Busca la API Key de Gemini con la siguiente prioridad:
    1. Campo 'api_key' dentro de config.json (permite actualizar la clave sin reiniciar terminales).
    2. Variable de entorno GEMINI_API_KEY.
    """
    ruta_config = _obtener_ruta_configuracion()
    if os.path.exists(ruta_config):
        try:
            with open(ruta_config, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                if isinstance(datos, dict) and datos.get("api_key") and str(datos["api_key"]).strip():
                    return str(datos["api_key"]).strip()
        except Exception:
            pass

    clave_entorno = os.getenv("GEMINI_API_KEY")
    if clave_entorno and clave_entorno.strip():
        return clave_entorno.strip()

    return None


def _obtener_cliente_gemini(cad_api_key: Optional[str] = None):
    """Inicializa y retorna una instancia del cliente de Google GenAI."""
    if not TIENE_GOOGLE_GENAI or genai is None:
        raise ImportError(
            "La librería 'google-genai' no está instalada. "
            "Por favor ejecuta: pip install google-genai"
        )

    clave_final = cad_api_key or _obtener_clave_api()
    if not clave_final:
        raise ValueError(
            "No se encontró ninguna clave de API para Gemini. "
            "Configura la variable de entorno GEMINI_API_KEY o añade 'api_key' en config.json."
        )

    return genai.Client(api_key=clave_final)


# ==========================================
# Declaracion de Funciones de Interaccion con IA
# ==========================================

def llamar_api(
    cad_prompt: str,
    cad_instruccion_sistema: str = PROMPT_SISTEMA_BASE,
    num_temperatura: float = TEMPERATURA_DEFAULT,
    num_max_tokens: int = MAX_TOKENS_DEFAULT,
    cad_api_key: Optional[str] = None
) -> str:
    """
    Funcion base para enviar prompts y comunicarse con la API de Gemini de forma segura.
    Aplica controles estrictos de temperatura y limites de tokens.
    """
    try:
        cliente = _obtener_cliente_gemini(cad_api_key)

        if not TIENE_GOOGLE_GENAI or types is None:
            raise ImportError("La librería 'google-genai' no está disponible.")

        config_generacion = types.GenerateContentConfig(
            system_instruction=cad_instruccion_sistema,
            temperature=num_temperatura,
            max_output_tokens=num_max_tokens,
        )

        global _modelo_activo_cache
        lista_modelos_intento = ([_modelo_activo_cache] if _modelo_activo_cache else []) + [m for m in MODELOS_DISPONIBLES if m != _modelo_activo_cache]

        ultimo_error = None
        for str_modelo in lista_modelos_intento:
            try:
                respuesta = cliente.models.generate_content(
                    model=str_modelo,
                    contents=cad_prompt,
                    config=config_generacion,
                )
                if respuesta and respuesta.text:
                    _modelo_activo_cache = str_modelo
                    return respuesta.text.strip()
            except Exception as error_intento:
                ultimo_error = error_intento
                cad_error = str(error_intento)
                # Si la clave es invalida, reportar inmediatamente
                if "API_KEY_INVALID" in cad_error or "invalid api key" in cad_error.lower() or "permission_denied" in cad_error.lower():
                    return f"[Error de Clave de API]: La clave de Gemini no es válida o no tiene permisos. Detalle: {cad_error}"

                # Si el modelo no existe (404), esta saturado (503), o excede limite de tasa (429), prueba el siguiente
                if (
                    "503" in cad_error
                    or "UNAVAILABLE" in cad_error
                    or "high demand" in cad_error.lower()
                    or "429" in cad_error
                    or "RESOURCE_EXHAUSTED" in cad_error
                    or "404" in cad_error
                    or "NOT_FOUND" in cad_error
                ):
                    continue

                # Otros errores imprevistos
                return f"[Error en Servicio IA]: {cad_error}"

        # Descubrimiento dinamico: Si los modelos fijos no respondieron, consultar directamente los modelos de la cuenta
        try:
            modelos_remotos = []
            for obj_modelo in cliente.models.list():
                nom = getattr(obj_modelo, "name", "") or ""
                # Limpiar prefijo 'models/' si viene incluido
                nom_limpio = nom.replace("models/", "")
                if "gemini" in nom.lower() and "embedding" not in nom.lower():
                    if nom_limpio not in modelos_remotos:
                        modelos_remotos.append(nom_limpio)
                    if nom not in modelos_remotos:
                        modelos_remotos.append(nom)

            for str_modelo_remoto in modelos_remotos:
                try:
                    respuesta = cliente.models.generate_content(
                        model=str_modelo_remoto,
                        contents=cad_prompt,
                        config=config_generacion,
                    )
                    if respuesta and respuesta.text:
                        _modelo_activo_cache = str_modelo_remoto
                        return respuesta.text.strip()
                except Exception as error_remoto:
                    ultimo_error = error_remoto
                    continue
        except Exception as error_listado:
            ultimo_error = error_listado

        if ultimo_error:
            detalle_modelos = ""
            try:
                lista_nombres = [getattr(m, "name", str(m)) for m in cliente.models.list()]
                detalle_modelos = f" | Modelos detectados en tu cuenta: {lista_nombres[:8] if lista_nombres else 'Ninguno'}"
            except Exception as e_lista:
                detalle_modelos = f" | No se pudo listar modelos: {str(e_lista)}"

            return f"[Error en Servicio IA]: No se pudo conectar con ningún modelo de Gemini disponible. Último error: {str(ultimo_error)}{detalle_modelos}"
        return "No se recibió respuesta de texto del modelo de IA."

    except Exception as error:
        return f"[Error en Servicio IA]: {str(error)}"


def explicar_tabla_amortizacion(
    dict_resumen: Dict[str, Any],
    lista_tabla: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Arma el prompt e interpreta los resultados financieros de la tabla calculada.
    Analiza costo total, distribucion de capital e intereses y la evolucion de la cuota.
    """
    detalles_tabla = ""
    if lista_tabla and len(lista_tabla) > 0:
        primera = lista_tabla[0]
        ultima = lista_tabla[-1]
        mitad = lista_tabla[len(lista_tabla) // 2]
        detalles_tabla = (
            f"\nMuestras de la tabla calculada:"
            f"\n- Periodo inicial (Mes {primera.get('periodo', 1)}): Cuota ${primera.get('cuota', 0):,.2f}, Interés ${primera.get('interes', 0):,.2f}, Capital ${primera.get('capital', 0):,.2f}"
            f"\n- Periodo medio (Mes {mitad.get('periodo', len(lista_tabla)//2)}): Cuota ${mitad.get('cuota', 0):,.2f}, Interés ${mitad.get('interes', 0):,.2f}, Capital ${mitad.get('capital', 0):,.2f}"
            f"\n- Periodo final (Mes {ultima.get('periodo', len(lista_tabla))}): Cuota ${ultima.get('cuota', 0):,.2f}, Interés ${ultima.get('interes', 0):,.2f}, Capital ${ultima.get('capital', 0):,.2f}"
        )

    cad_prompt = f"""
Por favor genera una interpretación y reporte analítico claro para el cliente sobre los siguientes resultados:

DATOS GENERALES DEL PRÉSTAMO:
- Sistema de amortización: {dict_resumen.get('sistema', 'N/D')}
- Monto financiado: ${dict_resumen.get('monto', 0):,.2f}
- Plazo convenido: {dict_resumen.get('plazo', 0)} meses
- Tasa de Interés Anual: {dict_resumen.get('tasa', 0)}%
- Total de Intereses a pagar: ${dict_resumen.get('total_intereses', 0):,.2f}
- Costo Total a liquidar: ${dict_resumen.get('pago_total', 0):,.2f}
- Costo Anual Total / TIR: {dict_resumen.get('cat', 'N/D')}%
{detalles_tabla}

INSTRUCCIONES DEL REPORTE:
1. Explica el impacto del costo financiero total (cuánto pagará de más en relación al capital prestado).
2. Explica cómo evoluciona la cuota y los intereses a lo largo del tiempo bajo este sistema.
3. Brinda una recomendación u opinión ejecutiva sobre si este esquema es conveniente o en qué circunstancias.
"""
    return llamar_api(cad_prompt)


def comparar_sistemas(
    dict_frances: Dict[str, Any],
    dict_aleman: Dict[str, Any],
    dict_americano: Dict[str, Any]
) -> str:
    """
    Compara los 3 escenarios calculados (Francés, Alemán, Americano)
    y recomienda la mejor opción según el perfil o necesidades del usuario.
    """
    cad_prompt = f"""
Por favor compara objetivamente los 3 sistemas de amortización calculados para el mismo monto y plazo:

1. SISTEMA FRANCÉS:
   - Total intereses: ${dict_frances.get('total_intereses', 0):,.2f}
   - Pago total final: ${dict_frances.get('pago_total', 0):,.2f}
   - Primera cuota: ${dict_frances.get('primera_cuota', 0):,.2f}
   - Última cuota: ${dict_frances.get('ultima_cuota', 0):,.2f}

2. SISTEMA ALEMÁN:
   - Total intereses: ${dict_aleman.get('total_intereses', 0):,.2f}
   - Pago total final: ${dict_aleman.get('pago_total', 0):,.2f}
   - Primera cuota: ${dict_aleman.get('primera_cuota', 0):,.2f}
   - Última cuota: ${dict_aleman.get('ultima_cuota', 0):,.2f}

3. SISTEMA AMERICANO:
   - Total intereses: ${dict_americano.get('total_intereses', 0):,.2f}
   - Pago total final: ${dict_americano.get('pago_total', 0):,.2f}
   - Cuota mensual regular: ${dict_americano.get('cuota_interes', 0):,.2f}
   - Cuota final con capital: ${dict_americano.get('cuota_final', 0):,.2f}

INSTRUCCIONES:
1. Resalta brevemente las diferencias clave en intereses totales y flujo de efectivo.
2. Identifica cuál es el sistema más económico en intereses y cuál da mayor estabilidad mensual.
3. Recomienda a qué perfil de cliente le conviene cada uno.
"""
    return llamar_api(cad_prompt)


def simular_escenario_personalizado(
    cad_pregunta_usuario: str,
    dict_resumen: Dict[str, Any],
    lista_tabla: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Responde consultas o dudas libres del usuario sobre el escenario calculado actual,
    asegurando no salirse del contexto financiero de la simulación.
    """
    cad_contexto = f"""
CONTEXTO DEL ESCENARIO ACTUAL DEL USUARIO:
- Sistema: {dict_resumen.get('sistema', 'N/D')}
- Monto: ${dict_resumen.get('monto', 0):,.2f}
- Plazo: {dict_resumen.get('plazo', 0)} meses
- Tasa: {dict_resumen.get('tasa', 0)}%
- Total Intereses: ${dict_resumen.get('total_intereses', 0):,.2f}
- Pago Total: ${dict_resumen.get('pago_total', 0):,.2f}
- CAT/TIR: {dict_resumen.get('cat', 'N/D')}%
"""
    cad_prompt_completo = (
        f"{cad_contexto}\n"
        f"PREGUNTA DEL USUARIO:\n"
        f"\"{cad_pregunta_usuario}\"\n\n"
        f"Responde a su duda financiera apoyándote estrictamente en los datos del escenario."
    )
    return llamar_api(cad_prompt_completo)
