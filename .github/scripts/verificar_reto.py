#!/usr/bin/env python3
"""Verificador del curso aprende-github.

Revisa en el repositorio de práctica de cada alumno (USUARIO/mi-primer-repo)
las evidencias que dejan los ejercicios de los módulos 02 a 08.

Modos:
  pr     Revisa el Pull Request del reto final y deja un comentario con el resultado.
  todos  Revisa a todos los alumnos de reto-final/alumnos.md y genera un reporte.
  avance Contesta el Issue "Revisar mi avance" con lo que lleva el alumno.

Solo lee datos públicos con la API de GitHub. No ejecuta código de los alumnos.
"""
import base64
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_PRACTICA = "mi-primer-repo"
ARCHIVO_LISTA = "reto-final/alumnos.md"
MARCA = "<!-- verificador-reto -->"
URL_CURSO = "https://github.com/git-master-utn/aprende-github"
ETIQUETAS = {
    True: ("✅ completo", "2da44e", "El alumno completó todos los módulos"),
    False: ("❌ incompleto", "d1242f", "Al alumno le falta evidencia de algún módulo"),
}
URL_AYUDA = URL_CURSO + "/tree/main/reto-final#si-el-robot-marca-algo-en-rojo"

MODULOS = {
    "02": "02-instalacion",
    "03": "03-primer-repo",
    "04": "04-ramas",
    "05": "05-colaborar",
    "06": "06-extras",
    "07": "07-git-y-github-juntos",
    "08": "08-permisos",
}


# Evidencias que se revisan, en orden, con sus puntos (suman 10).
# Pesan más los ejercicios más difíciles: conflicto, colaborar y sincronizar.
EVIDENCIAS = [
    ("02", "Commits ligados a tu cuenta (correo bien configurado)", 0.5),
    ("03", "README.md y al menos 3 commits", 1),
    ("04", "Unión de ramas hecha en tu computadora (ejercicio del conflicto)", 2),
    ("05", "Aceptaste un Pull Request de un compañero", 2),
    ("06", "`.gitignore` que ignora archivos `.log`", 0.5),
    ("06", "Al menos un Issue creado", 0.5),
    ("07", "Sincronizaste con `git pull` después de editar en GitHub", 2),
    ("08", "Rama `main` protegida", 1.5),
]
TOTAL = sum(p for _, _, p in EVIDENCIAS)


def fmt(n):
    return str(int(n)) if float(n).is_integer() else str(n)


def con_puntos(res):
    """Agrega a cada revisión sus puntos: (modulo, descripcion, ok, detalle, puntos)."""
    return [r + (EVIDENCIAS[i][2],) for i, r in enumerate(res)]


def calificacion(res):
    return sum(pts for _, _, ok, _, pts in res if ok)


def api(metodo, ruta, datos=None):
    req = urllib.request.Request(API + ruta, method=metodo)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "verificador-reto-aprende-github")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    cuerpo = None
    if datos is not None:
        cuerpo = json.dumps(datos).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, cuerpo, timeout=30) as r:
            texto = r.read().decode()
            return r.status, (json.loads(texto) if texto else None)
    except urllib.error.HTTPError as e:
        return e.code, None


def get(ruta):
    return api("GET", ruta)


def primera_linea(commit):
    return commit["commit"]["message"].splitlines()[0] if commit["commit"]["message"] else ""


def revisar(usuario):
    """Devuelve (lista de revisiones, info). Cada revisión: (modulo, descripcion, ok, detalle)."""
    res = []
    base = f"/repos/{usuario}/{REPO_PRACTICA}"

    st, repo = get(base)
    if st != 200:
        res = [(m, d, False, "Sin repo de práctica") for m, d, _ in EVIDENCIAS]
        res[1] = ("03", f"Repo público `{usuario}/{REPO_PRACTICA}` con README.md y al menos 3 commits",
                  False, "No existe, es privado o tiene otro nombre")
        return con_puntos(res), None
    rama = repo["default_branch"]

    _, commits = get(f"{base}/commits?sha={rama}&per_page=100")
    commits = commits or []

    # 02 · Nombre y correo configurados: GitHub liga los commits a la cuenta
    propios = [c for c in commits
               if (c.get("author") or {}).get("login", "").lower() == usuario.lower()]
    res.append(("02", "Commits ligados a tu cuenta (correo bien configurado)",
                len(propios) >= 1, f"{len(propios)} de {len(commits)} commits"))

    # 03 · Primer repo
    st_readme, _ = get(f"{base}/contents/README.md?ref={rama}")
    res.append(("03", "README.md y al menos 3 commits",
                st_readme == 200 and len(commits) >= 3, f"{len(commits)} commits"))

    # 04 · Merge local (ejercicio del conflicto)
    merges = [c for c in commits if len(c.get("parents", [])) >= 2]
    def de_pull(c):
        return re.match(r"Merge (remote-tracking )?branch '.+' of ", primera_linea(c)) is not None
    locales = [c for c in merges
               if not primera_linea(c).startswith("Merge pull request") and not de_pull(c)]
    res.append(("04", "Unión de ramas hecha en tu computadora (ejercicio del conflicto)",
                bool(locales), primera_linea(locales[0]) if locales else ""))

    # 05 · Pull Request de un compañero aceptado
    _, prs = get(f"{base}/pulls?state=closed&per_page=100")
    ajenos = [p for p in (prs or [])
              if p.get("merged_at") and p["user"]["login"].lower() != usuario.lower()]
    res.append(("05", "Aceptaste un Pull Request de un compañero", bool(ajenos),
                ", ".join("@" + p["user"]["login"] for p in ajenos[:3])))

    # 06 · .gitignore e Issue
    st_gi, gi = get(f"{base}/contents/.gitignore?ref={rama}")
    tiene_log = False
    if st_gi == 200 and gi and gi.get("content"):
        tiene_log = ".log" in base64.b64decode(gi["content"]).decode(errors="ignore")
    res.append(("06", "`.gitignore` que ignora archivos `.log`", tiene_log, ""))

    _, issues = get(f"{base}/issues?state=all&per_page=100")
    n_issues = len([i for i in (issues or []) if "pull_request" not in i])
    res.append(("06", "Al menos un Issue creado", n_issues >= 1, f"{n_issues} issues"))

    # 07 · git pull que unió cambios hechos en GitHub
    pulls = [c for c in merges
             if re.match(r"Merge (remote-tracking )?branch '.+' of ", primera_linea(c))]
    res.append(("07", "Sincronizaste con `git pull` después de editar en GitHub",
                bool(pulls), ""))

    # 08 · Rama principal protegida
    st_b, b = get(f"{base}/branches/{rama}")
    protegida = bool(st_b == 200 and b and b.get("protected"))
    if not protegida:
        st_r, reglas = get(f"{base}/rules/branches/{rama}")
        protegida = st_r == 200 and any(r.get("type") == "pull_request" for r in (reglas or []))
    res.append(("08", f"Rama `{rama}` protegida", protegida, ""))

    fechas = sorted(c["commit"]["author"]["date"][:10] for c in commits)
    info = {"commits": len(commits), "desde": fechas[0] if fechas else "",
            "hasta": fechas[-1] if fechas else ""}
    return con_puntos(res), info


def tabla_revisiones(res):
    lineas = ["| Módulo | Evidencia | Estado | Puntos | Detalle |", "|:-:|---|:-:|:-:|---|"]
    for mod, desc, ok, det, pts in res:
        enlace = f"[{mod}]({URL_CURSO}/tree/main/{MODULOS[mod]})"
        lineas.append(f"| {enlace} | {desc} | {'✅' if ok else '❌'} | "
                      f"{fmt(pts if ok else 0)} / {fmt(pts)} | {det} |")
    lineas.append(f"| | **Calificación** | | **{fmt(calificacion(res))} / {fmt(TOTAL)}** | |")
    return "\n".join(lineas)


FILA_DEL_PR = {}  # celdas de la última fila revisada, para agregarla a la lista


def revisar_fila(repo, numero, autor):
    """Revisa que el PR solo agregue una fila válida del propio autor."""
    problemas = []
    FILA_DEL_PR.clear()
    _, archivos = get(f"/repos/{repo}/pulls/{numero}/files?per_page=100")
    archivos = archivos or []
    nombres = [a["filename"] for a in archivos]
    otros = [n for n in nombres if n != ARCHIVO_LISTA]
    if otros:
        problemas.append("Solo debes modificar `reto-final/alumnos.md` (también cambiaste: "
                         + ", ".join(f"`{o}`" for o in otros) + ")")
    if ARCHIVO_LISTA not in nombres:
        problemas.append("No agregaste tu fila en `reto-final/alumnos.md`")
        return problemas

    parche = next(a for a in archivos if a["filename"] == ARCHIVO_LISTA).get("patch", "")
    agregadas = [l[1:].strip() for l in parche.splitlines()
                 if l.startswith("+") and not l.startswith("+++")]
    quitadas = [l[1:].strip() for l in parche.splitlines()
                if l.startswith("-") and not l.startswith("---") and l[1:].strip()]
    # Una fila que aparece quitada y agregada igual solo cambió el salto de línea final
    realmente_quitadas = [l for l in quitadas if l not in agregadas]
    filas_nuevas = [l for l in agregadas if l.startswith("|") and l not in quitadas]

    if realmente_quitadas:
        problemas.append("No borres ni cambies las filas de tus compañeros")
    if len(filas_nuevas) != 1:
        problemas.append(f"Debes agregar exactamente una fila (agregaste {len(filas_nuevas)})")
        return problemas

    fila = filas_nuevas[0]
    celdas = [c.strip() for c in fila.strip().strip("|").split("|")]
    if len(celdas) != 4 or not all(celdas):
        problemas.append("Tu fila debe tener las 4 columnas llenas: Nombre | Usuario | Grupo | Fecha")
    m = re.search(r"github\.com/([A-Za-z0-9-]+)", fila) or re.search(r"@([A-Za-z0-9-]+)", fila)
    if not m or m.group(1).lower() != autor.lower():
        problemas.append(f"El usuario de tu fila debe ser el tuyo: `@{autor}`")
    if len(celdas) == 4:
        FILA_DEL_PR.update(nombre=celdas[0], grupo=celdas[2])
    return problemas


def limpiar(texto, largo):
    """Deja solo texto plano en una celda (sin enlaces, HTML ni separadores de tabla)."""
    texto = re.sub(r"<[^>]*>|https?://\S+|www\.\S+", "", texto)
    texto = re.sub(r"[|<>\[\]()`*_~#!\\]", "", texto)
    return " ".join(texto.split())[:largo] or "—"


def agregar_a_lista(repo, autor):
    """Agrega la fila del alumno a reto-final/alumnos.md en main. Devuelve True si quedó en la lista."""
    nombre = limpiar(FILA_DEL_PR.get("nombre", autor), 80)
    grupo = limpiar(FILA_DEL_PR.get("grupo", ""), 20)
    hoy = datetime.now(timezone(timedelta(hours=-6))).strftime("%Y-%m-%d")
    fila = f"| {nombre} | [@{autor}](https://github.com/{autor}) | {grupo} | {hoy} |"
    ruta = f"/repos/{repo}/contents/{ARCHIVO_LISTA}"
    for _ in range(5):  # reintenta si otro alumno se agregó al mismo tiempo
        st, actual = get(ruta)
        if st != 200 or not actual:
            return False
        texto = base64.b64decode(actual["content"]).decode()
        if re.search(rf"github\.com/{re.escape(autor)}\)", texto, re.IGNORECASE):
            return True  # ya estaba
        nuevo = texto.rstrip("\n") + "\n" + fila + "\n"
        st, _ = api("PUT", ruta, {
            "message": f"Agrego a {nombre} (@{autor}) a la lista de alumnos",
            "content": base64.b64encode(nuevo.encode()).decode(),
            "sha": actual["sha"],
        })
        if st in (200, 201):
            return True
        time.sleep(2)
    return False


def modo_pr():
    completo = verificar_pr(os.environ["REPO"], os.environ["PR_NUMBER"], os.environ["PR_AUTHOR"])
    sys.exit(0 if completo else 1)


def verificar_pr(repo, numero, autor, resumen_en_log=True):
    """Revisa un PR, deja (o actualiza) el comentario del robot y dice si está completo."""
    problemas = revisar_fila(repo, numero, autor)
    res, info = revisar(autor)
    completo = not problemas and all(r[2] for r in res)
    en_lista = completo and agregar_a_lista(repo, autor)

    partes = [MARCA, f"## 🔎 Verificación del curso para @{autor}", "",
              f"**Calificación: {fmt(calificacion(res))} / {fmt(TOTAL)}**", ""]
    if completo:
        if en_lista:
            partes.append(f"🎉 **¡Felicidades, terminaste el curso!** Tu repositorio de práctica tiene "
                          f"la evidencia de todos los módulos y ya apareces en la "
                          f"[lista de alumnos]({URL_CURSO}/blob/main/{ARCHIVO_LISTA}). "
                          "Cerré este Pull Request porque ya no hace falta: tu fila ya está en la lista.")
        else:
            partes.append("✅ **Todo completo.** Tu repositorio de práctica tiene la evidencia de "
                          "todos los módulos. No pude agregarte a la lista automáticamente; "
                          "el instructor lo hará a mano.")
    else:
        partes.append("❌ **Todavía falta algo.** Revisa lo que está en rojo, complétalo y "
                      "después **edita la descripción de este Pull Request** para que se vuelva a revisar: "
                      "en el primer recuadro (el tuyo) da clic en **⋯** → **Edit**, agrega un espacio "
                      "al final y da clic en **Update comment**.")
    if problemas:
        partes += ["", "### Tu Pull Request", ""] + [f"- ❌ {p}" for p in problemas]

    pistas = []
    if any(p.startswith("Solo debes modificar") for p in problemas):
        pistas.append("Parece que hiciste los ejercicios **dentro de tu fork del curso**. Los ejercicios "
                      f"van en tu propio repo `{REPO_PRACTICA}`. Cierra este PR, borra tu fork y vuelve a "
                      "hacer el reto final desde un fork nuevo, agregando **solo** tu fila.")
    if any(p.startswith("Debes agregar exactamente una fila") for p in problemas):
        pistas.append("Cada alumno manda **su propio** Pull Request, desde su cuenta, con **una sola** fila.")
    if info is None:
        pistas.append(f"No encontré `{autor}/{REPO_PRACTICA}`. Crea en **tu** cuenta un repo **público** "
                      f"llamado **exactamente** `{REPO_PRACTICA}` (módulo 03) y haz ahí los ejercicios. "
                      "Si ya lo tienes, revisa que el nombre sea idéntico y que no sea privado.")
    if pistas:
        partes += ["", "### 💡 Pistas", ""] + [f"- {p}" for p in pistas]
    partes += ["", f"### Tu repositorio de práctica: [{autor}/{REPO_PRACTICA}]"
               f"(https://github.com/{autor}/{REPO_PRACTICA})", "", tabla_revisiones(res)]
    if info:
        partes += ["", f"Commits revisados: **{info['commits']}** · "
                       f"del **{info['desde']}** al **{info['hasta']}**"]
    if not completo:
        partes += ["", f"📖 ¿No entiendes algún ❌? Lee **[Si el robot marca algo en rojo]({URL_AYUDA})**. "
                       "Cuando lo arregles, edita la descripción de este PR; **no abras otro**."]
    partes += ["", "<sub>El módulo 01 es teórico y se evalúa en clase.</sub>"]
    cuerpo = "\n".join(partes)

    # Actualiza el comentario anterior del verificador en vez de crear otro
    _, comentarios = get(f"/repos/{repo}/issues/{numero}/comments?per_page=100")
    previo = next((c for c in (comentarios or []) if MARCA in (c.get("body") or "")), None)
    if previo:
        api("PATCH", f"/repos/{repo}/issues/comments/{previo['id']}", {"body": cuerpo})
    else:
        api("POST", f"/repos/{repo}/issues/{numero}/comments", {"body": cuerpo})
    etiquetar(repo, numero, completo)
    if en_lista:
        api("PATCH", f"/repos/{repo}/pulls/{numero}", {"state": "closed"})

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen and resumen_en_log:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(cuerpo.replace(MARCA, "") + "\n")
    if resumen_en_log:
        print(cuerpo)
    return completo


def etiquetar(repo, numero, completo):
    """Pone la etiqueta ✅ completo o ❌ incompleto y quita la contraria."""
    for nombre, color, desc in ETIQUETAS.values():
        api("POST", f"/repos/{repo}/labels",
            {"name": nombre, "color": color, "description": desc})  # 422 si ya existe
    poner, quitar = ETIQUETAS[completo][0], ETIQUETAS[not completo][0]
    api("POST", f"/repos/{repo}/issues/{numero}/labels", {"labels": [poner]})
    api("DELETE", f"/repos/{repo}/issues/{numero}/labels/{urllib.parse.quote(quitar)}")


def prs_abiertos(repo):
    """Lista (numero, autor) de los Pull Requests abiertos de alumnos.

    Se omiten los de dueños, miembros de la organización y colaboradores."""
    equipo = {"OWNER", "MEMBER", "COLLABORATOR"}
    lista, pagina = [], 1
    while True:
        st, prs = get(f"/repos/{repo}/pulls?state=open&per_page=100&page={pagina}")
        if st != 200 or not prs:
            break
        lista += [(p["number"], p["user"]["login"]) for p in prs
                  if p.get("author_association") not in equipo]
        if len(prs) < 100:
            break
        pagina += 1
    return lista


def usuarios_de_la_lista(ruta):
    usuarios = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            m = re.search(r"github\.com/([A-Za-z0-9-]+)", linea)
            if linea.strip().startswith("|") and m and m.group(1) != "usuario-ejemplo":
                usuarios.append(m.group(1))
    return list(dict.fromkeys(usuarios))


def modo_todos():
    repo = os.environ.get("REPO", "")
    comentar = os.environ.get("COMENTAR", "").lower() == "true"
    extra = [u.strip().lstrip("@") for u in os.environ.get("USUARIOS", "").split(",") if u.strip()]
    abiertos = prs_abiertos(repo) if repo else []
    pr_de = {}
    for numero, autor in abiertos:
        pr_de.setdefault(autor.lower(), []).append(numero)
    usuarios = list(dict.fromkeys(usuarios_de_la_lista(ARCHIVO_LISTA)
                                  + [a for _, a in abiertos] + extra))
    if comentar:
        for numero, autor in abiertos:
            verificar_pr(repo, numero, autor, resumen_en_log=False)
    cols = list(MODULOS)
    lineas = ["# 📊 Avance de los alumnos", "",
              f"Repositorio revisado de cada alumno: `USUARIO/{REPO_PRACTICA}`", "",
              f"Pull Requests abiertos de alumnos: **{len(abiertos)}** · "
              f"alumnos revisados: **{len(usuarios)}**", "",
              "| Alumno | PR | " + " | ".join(cols) + " | Avance | Calificación | Commits | Periodo |",
              "|---|---|" + "|".join(":-:" for _ in cols) + "|:-:|:-:|:-:|---|"]
    for u in usuarios:
        res, info = revisar(u)
        por_mod = {m: [r[2] for r in res if r[0] == m] for m in cols}
        marcas = [("✅" if por_mod[m] and all(por_mod[m]) else "❌") for m in cols]
        hechos = marcas.count("✅")
        periodo = f"{info['desde']} → {info['hasta']}" if info else "sin repo"
        commits = info["commits"] if info else 0
        prs = " ".join(f"[#{n}](https://github.com/{repo}/pull/{n})"
                       for n in pr_de.get(u.lower(), [])) or "—"
        lineas.append(f"| [@{u}](https://github.com/{u}/{REPO_PRACTICA}) | {prs} | "
                      + " | ".join(marcas) + f" | {hechos}/{len(cols)} | {fmt(calificacion(res))} / {fmt(TOTAL)} | {commits} | {periodo} |")
    if not usuarios:
        lineas.append("| (no hay alumnos registrados todavía) |" + " |" * (len(cols) + 5))
    if comentar:
        lineas += ["", f"Se dejó o actualizó el comentario del robot en {len(abiertos)} Pull Requests."]
    lineas += ["", "Módulos: 02 correo ligado a la cuenta · 03 README y 3 commits · "
               "04 unión de ramas local · 05 PR de un compañero aceptado · "
               "06 `.gitignore` e Issue · 07 `git pull` con cambios de GitHub · 08 rama protegida"]
    reporte = "\n".join(lineas)
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(reporte + "\n")
    print(reporte)


MARCA_AVANCE = "<!-- avance-curso -->"
TITULO_AVANCE = "Revisar mi avance"


def modo_avance():
    """Revisa el avance de quien abrió el Issue "Revisar mi avance" y le contesta ahí mismo."""
    repo = os.environ["REPO"]
    numero = os.environ["ISSUE_NUMBER"]
    autor = os.environ["AUTOR"]
    res, info = revisar(autor)
    nota = calificacion(res)
    llenos = round(nota / TOTAL * 10)
    barra = "🟩" * llenos + "⬜" * (10 - llenos)

    partes = [MARCA_AVANCE, f"## 📈 Tu avance en el curso, @{autor}", "",
              f"**Calificación hasta ahora: {fmt(nota)} / {fmt(TOTAL)}**", "", barra, ""]
    pendientes = sorted((r for r in res if not r[2]), key=lambda r: r[0])
    if info is None:  # sin repo: el primer paso es crearlo
        pendientes.sort(key=lambda r: "No existe" not in r[3])
    if not pendientes:
        partes += ["🎉 **¡Tienes todo completo!** Ya puedes hacer el "
                   f"[reto final]({URL_CURSO}/tree/main/reto-final) para aparecer en la lista de alumnos.", ""]
    else:
        mod, desc, _, det, _ = pendientes[0]
        partes += [f"👉 **Tu siguiente paso:** módulo [{mod}]({URL_CURSO}/tree/main/{MODULOS[mod]}) · {desc}"
                   + (f" ({det})" if det else ""), ""]
    if info is None:
        partes += [f"💡 No encontré tu repo `{autor}/{REPO_PRACTICA}`. Créalo **público** en tu cuenta, "
                   "con ese nombre exacto, como dice el curso.", ""]
    partes += [f"### Tu repositorio de práctica: [{autor}/{REPO_PRACTICA}](https://github.com/{autor}/{REPO_PRACTICA})",
               "", tabla_revisiones(res), "",
               "🔁 **Para volver a revisar**, termina tu siguiente ejercicio, haz `git push` y escribe aquí "
               "un comentario que diga `/revisar`.",
               "", "<sub>Este Issue solo revisa tu avance. Para entregar, haz el reto final.</sub>"]
    cuerpo = "\n".join(partes)
    api("POST", f"/repos/{repo}/issues/{numero}/comments", {"body": cuerpo})

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(cuerpo.replace(MARCA_AVANCE, "") + "\n")
    print(cuerpo)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "todos"
    {"pr": modo_pr, "avance": modo_avance}.get(modo, modo_todos)()
