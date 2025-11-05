Investigación de 3 APIs Nutricionales

1. USDA FoodData Central API

Qué es

Una base de datos del Departamento de Agricultura de EE.UU. que contiene información detallada sobre la composición nutricional de miles de alimentos, tanto genéricos como de marcas comerciales.

Cómo funciona

Es una API REST con endpoints para:

- Buscar alimentos por nombre o palabras clave.
- Obtener los detalles de nutrientes de un alimento específico.
- Listar grupos de alimentos.

Requiere una clave de acceso (API Key) y tiene límites de peticiones por hora y normativas de uso.

Ventajas

- Datos públicos y confiables.
- Excelente nivel de detalle en macro y micronutrientes.
- Gratuita, ideal para proyectos académicos o sin fines de lucro.

Desventajas

- Los datos son algo “en bruto”; no está pensada para recetas completas.
- Algunos productos de marca no tienen información tan completa.
- Puede no cubrir alimentos específicos de otros países.

Ejemplo de uso

Una aplicación permite al usuario escribir “½ taza de arroz blanco”.
La API devuelve los datos del alimento “arroz blanco”, y el sistema calcula la nutrición total multiplicando por la cantidad indicada. También se pueden armar tablas nutricionales completas combinando varios alimentos.

---

2. Edamam Nutrition / Food Database APIs

Qué es

Conjunto de APIs que permiten analizar recetas o listas de ingredientes, además de acceder a una base de datos de alimentos y productos con etiquetas de dietas y alergias.

Cómo funciona

Incluye:

- API de análisis de recetas: se envía texto (ingredientes/recetas) y devuelve nutrientes, calorías y etiquetas (como “vegano”, “sin gluten”).
- API de base de datos de alimentos: permite buscar por nombre, filtrar por dietas/alergias, e incluir productos envasados o comidas rápidas.

Ofrece planes gratuitos y de pago según el volumen de peticiones.

Ventajas

- Interpreta texto en lenguaje natural (“2 huevos, 1 taza de leche”).
- Incluye etiquetas de dietas y alergias.
- Soporte para varios idiomas.

Desventajas

- Plan gratuito con limitaciones de uso.
- Posibles errores si el texto del usuario es ambiguo.
- Algunos ingredientes pueden no estar registrados o tener nombres distintos.

Ejemplo de uso

Una app para planear menús semanales podría recibir las recetas escritas por el usuario y:

- Calcular datos nutricionales automáticamente.
- Advertir sobre alérgenos.
- Sugerir sustituciones (“leche sin lactosa”, por ejemplo).

Todo esto gracias al procesamiento inteligente de Edamam.

---

3. Spoonacular Nutrition / Recipe / Food API

Qué es

Una API muy completa que combina información de alimentos, recetas, menús y análisis nutricional, con soporte para filtros dietéticos y búsqueda semántica.

Cómo funciona

Ofrece endpoints para:

- Calcular la información nutricional de una receta.
- Buscar recetas según restricciones dietéticas.
- Buscar alimentos o ingredientes específicos.
- Analizar productos o imágenes.

Requiere clave de API (apiKey) y tiene planes gratuitos y de pago.

Ventajas

- Amplia gama de funciones: nutrición, recetas, menús, filtros, imágenes, etc.
- Soporte para múltiples dietas.
- Documentación clara y bien estructurada.

Desventajas

- Costos altos en planes de uso intensivo.
- Dificultad con ingredientes locales o nombres no estandarizados.
- Algunos productos regionales no aparecen y deben ingresarse manualmente.

---

Comparativa general

API| Tipo de datos| Costo (plan gratuito)| Límites de uso| Facilidad de implementación| Calidad de documentación
USDA FoodData Central| Nutrientes macro y micro de alimentos genéricos y algunos de marca| Gratis| Límite por hora| Media (datos crudos que hay que procesar)| Buena, pero técnica
Edamam| Análisis de recetas, ingredientes, dietas y alergias| Plan gratuito limitado| Pocas consultas mensuales| Alta (interpreta texto natural)| Muy buena, con ejemplos
Spoonacular| Recetas, menús, análisis nutricional, búsqueda de ingredientes| Plan gratuito con registro| Consultas diarias limitadas| Alta (endpoints sencillos)| Muy buena, con guías paso a paso

---

Justificación del API Seleccionado

Se eligió el API de Nutritionix por ser una de las más completas y prácticas en el ámbito de la nutrición.
Permite acceder a una base de datos muy amplia con alimentos genéricos y de marcas comerciales, proporcionando información precisa sobre calorías, macronutrientes y micronutrientes.

Además:

- Tiene un plan gratuito razonable.
- Está bien documentada.
- Es fácil de implementar, ideal para proyectos educativos o de investigación.

---

Ejemplos de Solicitudes y Respuestas de la API

Solicitud (ejemplo)

curl -X POST "https://trackapi.nutritionix.com/v2/natural/nutrients" \
 -H "Content-Type: application/json" \
 -H "x-app-id: TU_APP_ID" \
 -H "x-app-key: TU_APP_KEY" \
 -d '{"query":"1 manzana"}'

Respuesta (ejemplo simplificado)

{
  "foods": [
    {
      "food_name": "apple",
      "serving_qty": 1,
      "serving_unit": "medium (3\" dia)",
      "nf_calories": 95,
      "nf_total_fat": 0.3,
      "nf_total_carbohydrate": 25,
      "nf_protein": 0.5
    }
  ]
}

---

Otra solicitud

curl -X GET "https://trackapi.nutritionix.com/v2/search/item?nix_item_id=513fceb375b8dbbc21000fd5" \
 -H "x-app-id: TU_APP_ID" \
 -H "x-app-key: TU_APP_KEY"

Respuesta

{
  "foods": [
    {
      "food_name": "Big Mac",
      "brand_name": "McDonald's",
      "serving_qty": 1,
      "serving_unit": "burger",
      "nf_calories": 563,
      "nf_total_fat": 33,
      "nf_protein": 25,
      "nf_total_carbohydrate": 44
    }
  ]
}

---

Dificultades Encontradas y Soluciones

Problema| Descripción| Solución
Autenticación con credenciales| La API no respondía por falta de App ID y App Key.| Generar credenciales desde la web y agregarlas en las cabeceras.
Formato de solicitudes| Errores por formato JSON incorrecto.| Verificar comillas dobles, llaves y corchetes.
Límites de uso (Rate Limits)| La API devolvía errores por exceso de consultas.| Espaciar las peticiones o actualizar el plan.
Alimentos no reconocidos| Descripciones coloquiales no devolvían resultados.| Usar nombres estándar o IDs de productos.
Documentación en inglés| Dificulta la comprensión inicial.| Usar traductores y ejemplos oficiales.

---

Conclusión:
El análisis de distintas APIs nutricionales demuestra que existen opciones variadas según el objetivo del proyecto.
Mientras USDA destaca por su exactitud científica, Edamam y Spoonacular ofrecen herramientas más prácticas para el desarrollo de aplicaciones. Sin embargo, Nutritionix equilibra accesibilidad, amplitud de datos y facilidad de uso, siendo una excelente elección para fines educativos o de investigación.