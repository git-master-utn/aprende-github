<p align="center">
  <img src="img/banner.svg" alt="Aprende Git y GitHub" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Nivel-Principiante-3fb950" alt="Nivel: principiante">
  <img src="https://img.shields.io/badge/M%C3%B3dulos-8-58a6ff" alt="8 módulos">
  <img src="https://img.shields.io/badge/Idioma-Espa%C3%B1ol-a371f7" alt="Idioma: español">
  <img src="https://img.shields.io/badge/Incluye-Reto%20final-f0883e" alt="Incluye reto final">
</p>

# 👋 Bienvenido

Este repositorio es un **curso práctico para aprender Git y GitHub desde cero**.
No necesitas saber nada antes de empezar: solo una computadora, internet y ganas.

La idea es sencilla: **aprendes GitHub usando GitHub**. Lees un módulo, haces el
ejercicio y al final mandas tu primer *Pull Request* a este mismo repositorio.

## 🗺️ Ruta de aprendizaje

```mermaid
flowchart LR
    M1["01<br/>¿Qué es Git?"] --> M2["02<br/>Instalación"]
    M2 --> M3["03<br/>Primer repo"]
    M3 --> M4["04<br/>Ramas"]
    M4 --> M5["05<br/>Colaborar"]
    M5 --> M6["06<br/>Extras"]
    M6 --> M7["07<br/>Git + GitHub"]
    M7 --> M8["08<br/>Permisos"]
    M8 --> R["🏆<br/>Reto final"]
```

|  | Módulo | Qué vas a aprender | Tiempo |
|:-:|---|---|:-:|
| <img src="img/01.svg" width="44" alt=""> | [**01 · ¿Qué es Git?**](01-que-es-git/) | Para qué sirve el control de versiones y la diferencia entre Git y GitHub | 15 min |
| <img src="img/02.svg" width="44" alt=""> | [**02 · Instalación**](02-instalacion/) | Instalar Git, crear tu cuenta y conectar tu computadora con GitHub | 30 min |
| <img src="img/03.svg" width="44" alt=""> | [**03 · Tu primer repositorio**](03-primer-repo/) | `init`, `add`, `commit` y `push`: el ciclo básico de trabajo | 40 min |
| <img src="img/04.svg" width="44" alt=""> | [**04 · Ramas**](04-ramas/) | Crear ramas, unirlas y resolver conflictos sin miedo | 40 min |
| <img src="img/05.svg" width="44" alt=""> | [**05 · Colaborar**](05-colaborar/) | Fork, clone y Pull Request: cómo se trabaja en equipo | 40 min |
| <img src="img/06.svg" width="44" alt=""> | [**06 · Extras**](06-extras/) | `.gitignore`, Issues, deshacer cambios y GitHub Pages | 30 min |
| <img src="img/07.svg" width="44" alt=""> | [**07 · Git y GitHub juntos**](07-git-y-github-juntos/) | Cómo se sincronizan tu computadora y la nube, y el flujo completo de trabajo | 30 min |
| <img src="img/08.svg" width="44" alt=""> | [**08 · Permisos**](08-permisos/) | Quién puede ver y modificar un repo: visibilidad, colaboradores, roles y protección de ramas | 30 min |
| 🏆 | [**Reto final**](reto-final/) | Agrega tu nombre a este repo con un Pull Request | 20 min |

## 🤖 Antes de empezar: un robot revisa tu trabajo

Este curso **no se aprueba solo con el último paso**. Cuando mandas tu Pull Request
del [reto final](reto-final/), un robot revisa tu repositorio de práctica y comprueba
que hiciste los ejercicios de **cada módulo**. Te deja un comentario con ✅ lo que
cumpliste y ❌ lo que te falta.

Para que no te marque error, ten claros **tus dos repositorios**:

```mermaid
flowchart LR
    subgraph TU["Tu cuenta de GitHub"]
        P["📦 mi-primer-repo<br/>Aquí haces TODOS los ejercicios<br/>(módulos 03 al 08)"]
        F["🍴 Fork de aprende-github<br/>Aquí SOLO agregas tu fila<br/>(reto final)"]
    end
    F -- "Pull Request<br/>con tu fila" --> C["🏫 git-master-utn/aprende-github"]
    C -. "🤖 el robot revisa" .-> P
```

> [!IMPORTANT]
> **Las 3 reglas para que el robot te apruebe:**
> 1. Crea en **tu** cuenta un repo **público** llamado **exactamente** `mi-primer-repo` y haz ahí los ejercicios.
> 2. **No hagas los ejercicios dentro del fork del curso.** El fork es solo para agregar tu fila.
> 3. Al final de cada módulo hay una caja **"🔎 Evidencia para el reto final"**: cúmplela antes de seguir.

> [!TIP]
> ¿El robot te marcó algo en rojo? **No es que esté descompuesto:** te está diciendo
> exactamente qué te falta. Lee la tabla
> [Si el robot marca algo en rojo](reto-final/#si-el-robot-marca-algo-en-rojo),
> arréglalo y pide otra revisión.

## 📈 Revisa tu avance en cualquier momento

No tienes que esperar al final para saber si vas bien. Cuando termines un
ejercicio y hagas `git push`:

1. Abre el Issue **[📈 Revisar mi avance](https://github.com/git-master-utn/aprende-github/issues/new?template=revisar-avance.md&title=Revisar+mi+avance)** y da clic en **Create** (o *Submit new issue*).
2. En un minuto el robot te contesta con tu **calificación hasta ahora**, una
   tabla de lo que ya está bien ✅ y lo que falta ❌, y **tu siguiente paso**.
3. Cada vez que termines otro ejercicio, escribe en **ese mismo Issue** un
   comentario que diga `/revisar` y el robot vuelve a revisar.

```mermaid
flowchart TD
    A["1️⃣ Terminas un ejercicio<br/>y haces git push"]
    B["2️⃣ Comentas /revisar<br/>en tu Issue de avance"]
    C["3️⃣ 🤖 El robot te dice qué está bien<br/>y cuál es tu siguiente paso"]
    A --> B --> C
```

> [!NOTE]
> Abre **un solo** Issue de avance y úsalo todo el curso. Para entregar, al final
> haz el [reto final](reto-final/).

## 🚀 ¿Cómo usar este repo?

1. Sigue los módulos **en orden**; cada uno usa lo del anterior.
2. **Escribe los comandos tú mismo**. Copiar y pegar sirve, pero teclear enseña más.
3. Haz el **ejercicio** al final de cada módulo antes de pasar al siguiente.
4. Ten a la mano el [**cheatsheet**](cheatsheet.md) con todos los comandos en una página.
5. Termina con el [**reto final**](reto-final/): el robot revisa que hayas hecho todo.

> [!TIP]
> Si algo sale mal, no pasa nada. Git casi nunca pierde tu trabajo y equivocarse
> es la forma más rápida de aprenderlo.

## 📎 Material de apoyo

- Dirección de este repositorio: <https://github.com/git-master-utn/aprende-github>

- [Cheatsheet de comandos](cheatsheet.md)
- [Lista de alumnos que completaron el reto](reto-final/alumnos.md)

## 🙌 Créditos

<!-- Logo de la UTN: guarda el archivo como img/logo-utn.png y quita los signos de comentario de la línea de abajo -->
<!-- <img src="img/logo-utn.png" width="110" alt="Universidad Tecnológica de Nezahualcóyotl"> -->

Elaborado por [**Luis Ángel Pérez González**](https://github.com/luisperezglz) como parte de su servicio social en la
División Académica de Telemática de la **Universidad Tecnológica de Nezahualcóyotl**.

Puedes usar y adaptar este material libremente para dar clases.
