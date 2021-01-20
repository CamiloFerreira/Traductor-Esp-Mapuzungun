# Traductor-Esp-Mapuzungun

Este proyecto trata sobre la creacion de un traductor que sea facil y rapido , Utilizando webScraping para generar un diccionario de palabras y posteriormente ser utilizadas para crear un traductor , esto siendo visualizado mediante una pagina web .

# Problematica a Resolver con este proyecto
La principal problemática a resolver para este proyecto es sobre la falta de información respecto al lenguaje mapuzungun , donde este presenta una amplia gama de palabras que no se encuentran documentadas y/o no presentan un formato web para realizar una traducción fácil y rápida , siendo algunas de estas paginas que presentan este lenguaje una simple pagina solo con texto , sin métodos de búsquedas y/o filtrado de palabras . 
Objetivos para este proyecto: 
    • Realizar traducciones desde español – Mapuzungun
    • Tener una base de datos con las palabras y sus sinónimos 
    • Realizar webScraping respecto a los diccionarios que se encuentran actualmente 
    • Generar tokens de cada palabra para identificar tanto “Adjetivos” – “Sustantivos” etc

# Como ejecutar este proyecto 

Tener en consideracion que este proyecto esta siendo creado con python3.6 , las librerias para ejecutar todos los scripts  , se encuentra en el archivo requeriments.txt , ejecutando "pip install -r requeriments.txt " .

Para ejecutar la web con flask si te encuentras en linux solo ejecuta .sh que se encuentra llamado "ejecutar.sh"

instalar un modulo de spacy  ( Modulo para trabajar con NLP)

python -m spacy download es_core_news_sm

