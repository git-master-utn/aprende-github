# 📋 Cheatsheet de Git y GitHub

Todos los comandos del curso en una sola página.

## Configuración (una sola vez)

| Comando | Qué hace |
|---|---|
| `git config --global user.name "Tu Nombre"` | Define tu nombre |
| `git config --global user.email "correo@ejemplo.com"` | Define tu correo |
| `git config --global --list` | Muestra tu configuración |
| `ssh-keygen -t ed25519 -C "correo@ejemplo.com"` | Crea tu llave SSH |
| `ssh -T git@github.com` | Prueba la conexión con GitHub |

## Empezar un proyecto

| Comando | Qué hace |
|---|---|
| `git init` | Convierte la carpeta actual en un repo |
| `git clone DIRECCION` | Descarga un repo de GitHub |
| `git remote add origin DIRECCION` | Conecta tu repo local con GitHub |
| `git remote -v` | Muestra a qué remoto estás conectado |

## El ciclo de todos los días

| Comando | Qué hace |
|---|---|
| `git status` | Muestra qué cambió |
| `git add archivo` | Prepara un archivo |
| `git add .` | Prepara todos los cambios |
| `git commit -m "mensaje"` | Guarda una foto con mensaje |
| `git push` | Sube tus commits a GitHub |
| `git pull` | Baja los commits nuevos de GitHub |

## Ver el historial

| Comando | Qué hace |
|---|---|
| `git log --oneline` | Historial resumido |
| `git log --oneline --graph --all` | Historial con el dibujo de las ramas |
| `git diff` | Muestra los cambios que aún no preparas |

## Ramas

| Comando | Qué hace |
|---|---|
| `git branch` | Lista las ramas |
| `git switch -c nombre` | Crea una rama y te cambia a ella |
| `git switch nombre` | Te cambia a una rama existente |
| `git merge nombre` | Une esa rama a la rama actual |
| `git merge --abort` | Cancela una unión con conflictos |
| `git branch -d nombre` | Borra una rama ya unida |
| `git push -u origin nombre` | Sube una rama nueva a GitHub |

## Deshacer

| Comando | Qué hace |
|---|---|
| `git restore archivo` | Descarta los cambios de un archivo |
| `git restore --staged archivo` | Saca un archivo del área de preparación |
| `git commit --amend -m "mensaje"` | Corrige el mensaje del último commit (antes del push) |
| `git revert ID` | Crea un commit que deshace otro |

## Sincronizar con GitHub

| Comando | Qué hace |
|---|---|
| `git remote -v` | Muestra la dirección del remoto |
| `git fetch` | Descarga las novedades sin tocar tus archivos |
| `git pull` | Descarga las novedades y las une a tu rama |
| `git push` | Sube tus commits |
| `git status` | Dice si vas adelante o atrás del remoto |
| `git branch -a` | Lista ramas locales y remotas |

## Flujo para colaborar

```text
Fork  →  git clone  →  git switch -c mi-rama  →  cambios
      →  git add .  →  git commit -m "..."  →  git push -u origin mi-rama
      →  Pull Request
```

---

[🏠 Inicio](README.md)
