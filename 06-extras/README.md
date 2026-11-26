<img src="../img/06.svg" width="90" align="right" alt="">

# 06 · Extras que te van a salvar

**Objetivo:** conocer las herramientas que usarás en casi todos tus proyectos.

## 1. `.gitignore`: lo que no se sube

Hay archivos que **no deben** ir al repo: contraseñas, archivos temporales,
carpetas enormes de dependencias. Crea un archivo llamado `.gitignore` en la
raíz del proyecto y escribe ahí qué ignorar:

```gitignore
# Archivos con contraseñas o llaves
.env
*.key

# Carpetas de dependencias
node_modules/
venv/

# Basura del sistema
.DS_Store
Thumbs.db
```

> [!WARNING]
> **Nunca subas contraseñas, tokens ni llaves** a un repo, aunque sea privado.
> Si se te va una, borrarla del archivo no basta porque queda en el historial:
> hay que **cambiar esa contraseña** de inmediato.

## 2. Deshacer cosas

| Situación | Comando |
|---|---|
| Edité un archivo y quiero dejarlo como en el último commit | `git restore archivo.txt` |
| Hice `git add` de algo por error | `git restore --staged archivo.txt` |
| Me equivoqué en el mensaje del último commit (sin haber hecho push) | `git commit --amend -m "Mensaje correcto"` |
| Quiero deshacer un commit que ya subí | `git revert ID-DEL-COMMIT` |

El ID del commit lo ves con `git log --oneline`.

> [!NOTE]
> `git revert` no borra historia: crea un commit nuevo que deshace el anterior.
> Por eso es la forma segura cuando ya compartiste tus cambios.

## 3. Issues: la lista de pendientes del proyecto

En la pestaña **Issues** de cualquier repo puedes reportar errores, proponer
ideas o anotar tareas. Para crear uno: **Issues → New issue**, pon un título
claro y describe qué pasa y cómo reproducirlo.

Si en la descripción de un Pull Request escribes `Closes #3`, el issue número 3
se cierra solo cuando acepten el PR.

## 4. Markdown: para que tu README se vea bien

Los archivos `.md` usan Markdown, una forma sencilla de dar formato:

| Escribes | Obtienes |
|---|---|
| `# Título` | Título grande |
| `## Subtítulo` | Subtítulo |
| `**negritas**` | **negritas** |
| `*cursiva*` | *cursiva* |
| `` `código` `` | `código` |
| `- elemento` | Lista con viñetas |
| `[texto](https://ejemplo.com)` | Un enlace |
| `![descripción](imagen.png)` | Una imagen |

Un buen README responde tres preguntas: **qué es** el proyecto, **cómo se usa**
y **quién lo hizo**.

## 5. GitHub Pages: tu sitio web gratis

Con GitHub Pages puedes publicar un repo como página web:

1. En tu repo: **Settings → Pages**.
2. En **Source** elige **Deploy from a branch**.
3. Selecciona la rama `main` y la carpeta `/ (root)` → **Save**.
4. Espera un par de minutos. Tu sitio queda en
   `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`

## 6. Tu perfil también es un repo

Si creas un repo público que se llame **exactamente igual que tu usuario** y le
pones un `README.md`, ese contenido aparece en tu perfil de GitHub. Es tu carta
de presentación.

## ✏️ Ejercicio

**1. 💻 Crea el `.gitignore`** (en Git Bash, dentro de `~/Downloads/mi-primer-repo`):

```bash
echo "*.log" > .gitignore
git add .gitignore
git commit -m "Agrego .gitignore para ignorar archivos .log"
```

**2. Comprueba que funciona:**

```bash
echo "esto no se debe subir" > prueba.log
git status
```

✔️ En `git status` **no** debe aparecer `prueba.log`: Git lo está ignorando.

**3. Mejora tu README con Markdown:**

```bash
notepad README.md
```

📝 Agrega un título `## Sobre mí`, una palabra en `**negritas**` y una lista con
tres guiones `-`. Guarda (**Ctrl + S**), cierra y súbelo todo:

```bash
git add README.md
git commit -m "Mejoro mi README con Markdown"
git push
```

**4. 🌐 Abre un Issue** en la página de tu `mi-primer-repo`: pestaña **Issues** →
botón verde **New issue** → escribe un título como *"Agregar una foto al README"*
→ botón verde **Create** (o *Submit new issue*).

✔️ **Resultado esperado:** en GitHub, tu repo tiene el archivo `.gitignore`, el
README se ve con título y lista, y en la pestaña **Issues** aparece **1 Open**.

## 🔎 Evidencia para el reto final

> [!IMPORTANT]
> Tu `mi-primer-repo` debe tener un `.gitignore` con `*.log` y al menos un Issue.

> [!TIP]
> **¿Ya quedó bien?** Haz `git push` y comenta `/revisar` en tu Issue de avance.
> Si todavía no lo tienes, ábrelo aquí: [📈 Revisar mi avance](https://github.com/git-master-utn/aprende-github/issues/new?template=revisar-avance.md&title=Revisar+mi+avance).

## ✅ Antes de continuar

- [ ] Mi repo tiene un `.gitignore`
- [ ] Sé deshacer un cambio con `git restore`
- [ ] Ya creé un Issue
- [ ] Mi README usa Markdown

---

[⬅️ Anterior: 05 · Colaborar](../05-colaborar/) · [🏠 Inicio](../README.md) · [Siguiente: 07 · Git y GitHub juntos ➡️](../07-git-y-github-juntos/)
