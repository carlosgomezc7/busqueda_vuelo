"""
Genera el documento de entrega del proyecto (documento_proyecto.html)
incrustando el código completo de main.py.
Uso:  python3 generar_documento.py
Luego convertir a PDF con: soffice --headless --convert-to pdf documento_proyecto.html
"""

import html

CODIGO = open("main.py", encoding="utf-8").read()
CODIGO_HTML = html.escape(CODIGO)

CSS = """
<style>
body { font-family: 'DejaVu Sans', sans-serif; font-size: 10.5pt; margin: 2cm; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 20pt; text-align: center; color: #14532d; margin-top: 0.4cm; }
h2 { font-size: 14pt; color: #14532d; border-bottom: 2px solid #14532d; padding-bottom: 3px; margin-top: 0.9cm; }
h3 { font-size: 12pt; color: #1e6f3e; }
p  { text-align: justify; }
pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.5pt; background: #f5f5f5;
      border: 1px solid #ccc; padding: 8px; white-space: pre-wrap; line-height: 1.25; }
.captura { border: 2px dashed #999; background: #fafafa; text-align: center;
           padding: 30px 10px; margin: 12px 0; font-weight: bold; color: #555; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #888; padding: 5px 8px; font-size: 9.5pt; text-align: left; }
th { background: #e2efe4; }
.portada { text-align: center; margin-top: 3cm; }
.portada p { text-align: center; }
li { margin-bottom: 3px; }
</style>
"""

INTRO_GRAFO = """
<p>Un <b>grafo</b> es una estructura matemática formada por un conjunto de
<b>nodos</b> (también llamados vértices) y un conjunto de <b>aristas</b>
(también llamadas conexiones o arcos) que unen pares de nodos. Los grafos se
utilizan para representar relaciones entre objetos: cada nodo representa un
elemento y cada arista representa una relación o conexión entre dos de ellos.
Por ejemplo, en un mapa de carreteras los nodos son las ciudades y las aristas
son las carreteras que las conectan.</p>

<p>Un <b>grafo dirigido</b> (tambi&eacute;n llamado digrafo) es un grafo en el
que cada arista tiene una <b>direcci&oacute;n</b>: va desde un nodo de origen
hasta un nodo de destino. Esto significa que la conexi&oacute;n no es
sim&eacute;trica; es decir, si existe una arista de A hacia B, no
necesariamente existe una arista de B hacia A. Los grafos dirigidos son
ideales para modelar situaciones en las que el sentido importa, como el
tr&aacute;fico en calles de un solo sentido, las redes sociales (donde se
puede seguir a alguien sin que esa persona te siga) o los vuelos de una
aerol&iacute;nea.</p>

<p>Algunos <b>ejemplos de uso de los grafos en la vida real</b> son:</p>
<ul>
<li><b>Mapas y navegadores (GPS):</b> las calles y carreteras forman un grafo
donde los nodos son las intersecciones y las aristas son las v&iacute;as;
los algoritmos de ruta m&aacute;s corta (como el de Dijkstra) se usan para
calcular el mejor camino.</li>
<li><b>Redes sociales:</b> los usuarios son nodos y las amistades o
seguimientos son aristas (en el caso de los seguimientos, aristas
dirigidas).</li>
<li><b>Internet y telecomunicaciones:</b> las computadoras o servidores son
nodos y los cables o enlaces inal&aacute;mbricos son las aristas por donde
viajan los datos.</li>
<li><b>Rutas a&eacute;reas:</b> las ciudades son nodos y los vuelos entre
ellas son las aristas dirigidas; es exactamente el problema que se simula en
este proyecto.</li>
<li><b>Redes el&eacute;ctricas y de agua potable:</b> las centrales, las
subestaciones y los hogares se conectan mediante redes que se representan
como grafos.</li>
<li><b>Organigramas y procesos:</b> las jerarqu&iacute;as de una empresa o
los diagramas de flujo de un algoritmo tambi&eacute;n son grafos dirigidos.</li>
</ul>
"""

JUSTIFICACION = """
<p>Los <b>grafos son la herramienta ideal para representar redes de
transporte y rutas a&eacute;reas</b> por varias razones:</p>

<ul>
<li><b>Modelado natural:</b> una red de vuelos se compone de ciudades
(nodos) y conexiones entre ellas (aristas). La correspondencia es directa:
cada ciudad del pa&iacute;s es un nodo y cada vuelo es una arista.</li>

<li><b>Direccionalidad:</b> un vuelo de la Ciudad de M&eacute;xico a Canc&uacute;n
no implica que exista el vuelo de regreso en el mismo horario o por la misma
aerol&iacute;nea. El uso de un <b>grafo dirigido</b> permite representar
exactamente qu&eacute; rutas existen en cada sentido, igual que en la
realidad.</li>

<li><b>C&aacute;lculo de rutas &oacute;ptimas:</b> con algoritmos de teor&iacute;a
de grafos, como el de Dijkstra, se puede calcular la ruta m&aacute;s corta
(por kil&oacute;metros o por n&uacute;mero de escalas) entre dos ciudades,
que es el problema central de cualquier aerol&iacute;nea o agencia de
viajes.</li>

<li><b>An&aacute;lisis de la red:</b> los grafos permiten identificar
ciudades "hub" (las m&aacute;s conectadas), saber si la red es conexa o si
alguna ciudad quedar&iacute;a incomunicada si se cancela una ruta.</li>

<li><b>Generalizaci&oacute;n:</b> los mismos modelos se usan en log&iacute;stica,
mensajer&iacute;a, reparto de paqueter&iacute;a y transporte terrestre, por lo
que lo aprendido se aplica a muchos problemas reales.</li>
</ul>
"""

DESARROLLO = """
<h3>3.1 C&oacute;mo funciona el programa</h3>
<p>El programa se ejecuta desde la terminal con <code>python3 main.py</code>.
Al iniciar, construye autom&aacute;ticamente una red inicial con 13 ciudades
principales de M&eacute;xico (Ciudad de M&eacute;xico, Guadalajara, Monterrey,
Tijuana, Canc&uacute;n, M&eacute;rida, Veracruz, Oaxaca, Puebla, Le&oacute;n,
Puerto Vallarta, La Paz y San Luis Potos&iacute;) y 25 rutas de ejemplo. A
continuaci&oacute;n muestra un men&uacute; con 9 opciones que permite al
usuario administrar la red completa. Todas las ciudades precargadas son
editables: se pueden eliminar o a&ntilde;adir rutas, igual que cualquier
ciudad agregada despu&eacute;s.</p>

<p>El sistema incluye un <b>cat&aacute;logo de 65 ciudades de M&eacute;xico</b>
con sus coordenadas geogr&aacute;ficas reales (latitud y longitud). Al agregar
una ciudad nueva, el usuario la busca por nombre (sin necesidad de escribir
acentos) y el programa la coloca autom&aacute;ticamente en su posici&oacute;n
real sobre el mapa.</p>

<h3>3.2 C&oacute;mo est&aacute; estructurado el grafo</h3>
<p>El grafo se construye con la librer&iacute;a <b>NetworkX</b> usando la clase
<code>nx.DiGraph()</code>, es decir, un <b>grafo dirigido</b>:</p>
<ul>
<li>Cada <b>nodo</b> es una ciudad y almacena como atributo su posici&oacute;n
geogr&aacute;fica <code>pos = (latitud, longitud)</code>.</li>
<li>Cada <b>arista dirigida</b> es un vuelo y almacena como atributo su
distancia en kil&oacute;metros (<code>km</code>), calculada con la
<b>f&oacute;rmula de Haversine</b> a partir de las coordenadas de las dos
ciudades.</li>
<li>Con la distancia y una velocidad de crucero promedio de 850 km/h se
estima la <b>duraci&oacute;n del vuelo</b> (m&aacute;s 45 minutos de
despegue y aterrizaje).</li>
<li>El territorio mexicano se dibuja con <b>Matplotlib</b> usando los
pol&iacute;gonos (anillos de coordenadas) que forman la frontera del pa&iacute;s;
las ciudades se colocan en sus coordenadas reales, simulando un mapa tipo
"Google Maps".</li>
</ul>

<h3>3.3 C&oacute;mo funciona el men&uacute;</h3>
<table>
<tr><th>Opci&oacute;n</th><th>Descripci&oacute;n</th></tr>
<tr><td>1. Agregar Ciudad</td><td>Muestra el cat&aacute;logo de 65 ciudades
de M&eacute;xico con b&uacute;squeda por nombre; el usuario elige una y se
agrega al grafo en sus coordenadas reales.</td></tr>
<tr><td>2. Agregar Ruta de Vuelo</td><td>Pide ciudad de origen y destino
(acepta nombres con o sin acentos), valida que ambas existan y crea la
arista dirigida con su distancia. Pregunta si se desea crear tambi&eacute;n
el vuelo de regreso (ida y vuelta).</td></tr>
<tr><td>3. Eliminar Ciudad</td><td>Elimina una ciudad y todas sus rutas
asociadas (incluye las precargadas).</td></tr>
<tr><td>4. Eliminar Ruta</td><td>Elimina una conexi&oacute;n espec&iacute;fica
entre dos ciudades.</td></tr>
<tr><td>5. Mostrar Mapa de Rutas</td><td>Dibuja la red completa sobre el mapa
de M&eacute;xico: fronteras del pa&iacute;s, ciudades en sus coordenadas,
flechas dirigidas y distancia en km sobre cada ruta.</td></tr>
<tr><td>6. Ruta M&aacute;s Corta (Dijkstra)</td><td>Calcula la mejor ruta
entre dos ciudades minimizando la distancia (kil&oacute;metros) o el
n&uacute;mero de escalas, y la resalta en rojo sobre el mapa.</td></tr>
<tr><td>7. Distancia y Duraci&oacute;n</td><td>Muestra kil&oacute;metros y
tiempo estimado de un vuelo directo o del mejor recorrido con escalas.</td></tr>
<tr><td>8. Listar Ciudades y Rutas</td><td>Imprime en consola todas las
ciudades con sus coordenadas y todas las rutas con su distancia.</td></tr>
<tr><td>9. Salir</td><td>Termina el programa.</td></tr>
</table>
<p>Si el usuario selecciona una opci&oacute;n inv&aacute;lida (no num&eacute;rica
o fuera de rango), el programa muestra un mensaje de error y vuelve a pedir
la opci&oacute;n.</p>

<h3>3.4 Qu&eacute; hace cada funci&oacute;n del programa</h3>
<ul>
<li><code>normalizar_nombre()</code>: limpia el nombre de una ciudad
(espacios, may&uacute;sculas correctas sin capitalizar preposiciones como
"de" o "del").</li>
<li><code>plegar_acentos()</code>: convierte el texto a min&uacute;sculas sin
acentos para que "Ciudad Ju&aacute;rez" se encuentre escribiendo "juarez".</li>
<li><code>distancia_haversine()</code>: calcula la distancia en km entre dos
puntos geogr&aacute;ficos con la f&oacute;rmula de Haversine.</li>
<li><code>formato_duracion()</code> y <code>formato_km()</code>: dan formato
legible a horas y kil&oacute;metros.</li>
<li><code>RedVuelos.__init__()</code>: crea el grafo dirigido y precarga las
ciudades y rutas iniciales.</li>
<li><code>_agregar_nodo()</code> / <code>_agregar_arista()</code>: internas;
agregan nodos con posici&oacute;n y aristas con distancia.</li>
<li><code>_buscar_ciudad()</code>: encuentra el nombre can&oacute;nico de una
ciudad tolerando may&uacute;sculas y acentos.</li>
<li><code>agregar_ciudad()</code>: agrega una ciudad del cat&aacute;logo al
grafo validando que no exista.</li>
<li><code>agregar_ruta()</code>: crea la arista dirigida con su distancia en
km y valida ciudades y duplicados.</li>
<li><code>eliminar_ciudad()</code>: elimina el nodo y todas sus aristas.</li>
<li><code>eliminar_ruta()</code>: elimina una arista espec&iacute;fica.</li>
<li><code>ruta_mas_corta()</code>: aplica el algoritmo de <b>Dijkstra</b>
(por km) o BFS (por escalas) entre dos ciudades.</li>
<li><code>distancia_y_duracion()</code>: muestra km y tiempo del vuelo
directo o del mejor recorrido con escalas.</li>
<li><code>listar_red()</code>: imprime el estado completo de la red.</li>
<li><code>mostrar_grafo()</code>: dibuja el mapa de M&eacute;xico con la red,
las distancias y (opcionalmente) una ruta resaltada en rojo.</li>
<li><code>mostrar_menu()</code>: imprime el men&uacute; de opciones.</li>
<li><code>seleccionar_ciudad_del_catalogo()</code>: despliega el cat&aacute;logo
con b&uacute;squeda y devuelve la ciudad elegida.</li>
<li><code>principal()</code>: bucle principal que lee la opci&oacute;n del
usuario, valida errores y ejecuta la acci&oacute;n correspondiente.</li>
</ul>
"""

CAPTURAS = """
<h3>5.1 Captura 1: Men&uacute; del programa</h3>
<p><b>Pasos:</b> abrir una terminal, ubicarse en la carpeta del proyecto y
ejecutar <code>python3 main.py</code>. La pantalla inicial muestra el
men&uacute; completo con las 9 opciones.</p>
<div class="captura">[ INSERTAR AQU&Iacute; CAPTURA 1: Men&uacute; del programa ]</div>

<h3>5.2 Captura 2: Primer grafo con algunas ciudades</h3>
<p><b>Pasos:</b> en el men&uacute;, seleccionar la opci&oacute;n
<code>5</code> (Mostrar Mapa de Rutas). Se muestra la red inicial con las 13
ciudades precargadas y sus 25 rutas sobre el mapa de M&eacute;xico.</p>
<div class="captura">[ INSERTAR AQU&Iacute; CAPTURA 2: Primer grafo generado ]</div>

<h3>5.3 Captura 3: Modificaci&oacute;n agregando ciudad y ruta</h3>
<p><b>Pasos:</b></p>
<ol>
<li>Opci&oacute;n <code>1</code> (Agregar Ciudad).</li>
<li>En la b&uacute;squeda escribir <code>juar</code> y presionar Enter; la
lista filtrar&aacute; a Ciudad Ju&aacute;rez.</li>
<li>Seleccionar el n&uacute;mero correspondiente para agregarla.</li>
<li>Opci&oacute;n <code>2</code> (Agregar Ruta): origen
<code>Ciudad de M&eacute;xico</code>, destino <code>Ciudad Ju&aacute;rez</code>,
y responder <code>s</code> a la pregunta de vuelo de regreso.</li>
<li>Opci&oacute;n <code>5</code> para ver el mapa actualizado.</li>
</ol>
<div class="captura">[ INSERTAR AQU&Iacute; CAPTURA 3: Grafo modificado
(agregando ciudad y ruta) ]</div>

<h3>5.4 Captura 4: Otra modificaci&oacute;n del grafo (ruta m&aacute;s corta
resaltada)</h3>
<p><b>Pasos:</b></p>
<ol>
<li>Opci&oacute;n <code>6</code> (Ruta M&aacute;s Corta).</li>
<li>Origen <code>Tijuana</code>, destino <code>Canc&uacute;n</code>, criterio
<code>1</code> (distancia en km).</li>
<li>Responder <code>s</code> para ver la ruta resaltada en rojo sobre el
mapa.</li>
</ol>
<div class="captura">[ INSERTAR AQU&Iacute; CAPTURA 4: Grafo con la ruta m&aacute;s
corta resaltada ]</div>

<h3>5.5 Captura 5: Otra modificaci&oacute;n (eliminaci&oacute;n de una ciudad)</h3>
<p><b>Pasos:</b></p>
<ol>
<li>Opci&oacute;n <code>3</code> (Eliminar Ciudad) e ingresar
<code>Oaxaca</code>; el programa elimina la ciudad y todas sus rutas.</li>
<li>Opci&oacute;n <code>8</code> (Listar Ciudades y Rutas) para comprobar en
consola que la ciudad ya no aparece.</li>
<li>Opci&oacute;n <code>5</code> para ver el mapa sin la ciudad eliminada.</li>
</ol>
<div class="captura">[ INSERTAR AQU&Iacute; CAPTURA 5: Grafo despu&eacute;s de
eliminar una ciudad ]</div>
"""

CONCLUSION = """
<p><b>Qu&eacute; aprend&iacute; realizando el proyecto.</b> A lo largo del
proyecto aprend&iacute; a modelar un problema real (las rutas de una
aerol&iacute;nea) con una estructura matem&aacute;tica abstracta: el grafo
dirigido. Comprend&iacute; c&oacute;mo se representa un grafo en c&oacute;digo
con la librer&iacute;a NetworkX, c&oacute;mo almacenar informaci&oacute;n en
los nodos y aristas (coordenadas y distancias), y c&oacute;mo visualizarlo
con Matplotlib. Tambi&eacute;n aprend&iacute; a calcular distancias reales
entre dos puntos con la f&oacute;rmula de Haversine y a aplicar el algoritmo
de Dijkstra para encontrar la ruta m&aacute;s corta, adem&aacute;s de
manejar entradas del usuario con validaci&oacute;n de errores y organizar el
c&oacute;digo en funciones y clases.</p>

<p><b>Qu&eacute; dificultades encontr&eacute;.</b> La principal dificultad fue
la parte geogr&aacute;fica: obtener las coordenadas reales de las ciudades y
el contorno del territorio mexicano, y lograr que cada ciudad apareciera
dentro del mapa en su posici&oacute;n correcta. Otra dificultad fue
representar visualmente las flechas de un grafo dirigido cuando existen
vuelos en ambos sentidos entre dos ciudades, ya que se sobreponen; se
resolvi&oacute; curvando las flechas. Tambi&eacute;n fue un reto validar todas
las entradas del usuario (opciones inv&aacute;lidas, ciudades inexistentes,
rutas duplicadas) para que el programa nunca se detuviera por un error.</p>

<p><b>C&oacute;mo se pueden aplicar los grafos en problemas reales.</b> Los
grafos tienen aplicaci&oacute;n pr&aacute;ctica casi ilimitada: las
aerol&iacute;neas los usan para planear sus redes de vuelos y calcular
itinerarios; los navegadores GPS para encontrar la ruta m&aacute;s r&aacute;pida
en carretera; las empresas de paqueter&iacute;a para optimizar sus rutas de
reparto; las redes sociales para sugerir amigos; e incluso el internet se
modela como un grafo gigante por el que viajan los datos. Este proyecto
demuestra que con unas cuantas l&iacute;neas de Python es posible construir
una simulaci&oacute;n de un sistema de transporte nacional, y que la teor&iacute;a
de grafos, lejos de ser un tema abstracto, resuelve problemas cotidianos.</p>
"""

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Proyecto: Simulaci&oacute;n de Rutas A&eacute;reas con Grafos Dirigidos</title>
{CSS}
</head>
<body>

<div class="portada">
<h1>Simulaci&oacute;n de Rutas A&eacute;reas con Grafos Dirigidos</h1>
<h2>Red Nacional de Vuelos de M&eacute;xico</h2>
<p>Proyecto de la materia de Estructuras de Datos / Programaci&oacute;n</p>
<p><b>Nombre del alumno:</b> [ TU NOMBRE ]</p>
<p><b>Grupo / Turno:</b> [ TU GRUPO ]</p>
<p><b>Fecha:</b> [ FECHA ]</p>
</div>

<h2>1. Introducci&oacute;n</h2>
{INTRO_GRAFO}

<h2>2. Justificaci&oacute;n</h2>
{JUSTIFICACION}

<h2>3. Desarrollo del Proyecto</h2>
{DESARROLLO}

<h2>4. C&oacute;digo del Programa</h2>
<p>A continuaci&oacute;n se incluye el c&oacute;digo completo del programa en
Python. Las librer&iacute;as necesarias son <code>networkx</code> y
<code>matplotlib</code> (instalaci&oacute;n: <code>pip install networkx
matplotlib</code>).</p>
<pre>{CODIGO_HTML}</pre>

<h2>5. Capturas de Pantalla</h2>
{CAPTURAS}

<h2>6. Conclusi&oacute;n</h2>
{CONCLUSION}

</body>
</html>
"""

with open("documento_proyecto.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print("documento_proyecto.html generado correctamente.")
