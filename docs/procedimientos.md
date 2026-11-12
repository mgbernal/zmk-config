# Procedimientos de trabajo

## 1. Cambio pequeño (mover una tecla, añadir un símbolo)

Directamente en `master`:

```sh
git pull --rebase                  # por si se editó algo desde la web de GitHub o desde otro equipo
# editar config/kyria.keymap
python3 scripts/check_keymap.py
git add config/kyria.keymap        # ficheros concretos, nunca git add .
git commit -m "feat: ¿ en la capa ACC"
git push
```

Tipos de commit: `feat` (nueva función), `fix` (algo que estaba mal), `refactor` (reorganizar sin
cambiar el comportamiento), `docs`, `ci`, `chore`. Los mensajes se escriben en español.

## 2. Cambio grande o experimento (trackball, capa nueva, combos)

Se hace en una rama, para que `master` tenga siempre un firmware que funciona:

```sh
git switch -c exp/trackball
# cambios + commits
git push -u origin exp/trackball   # el CI compila también las ramas
```

- Flashea el firmware de esa ejecución y pruébalo unos días.
- Si funciona, intégralo en master:
  ```sh
  git switch master && git pull --rebase
  git merge --ff-only exp/trackball   # o abre un Pull Request en GitHub y haz merge ahí
  git push
  git push origin --delete exp/trackball
  ```
- Si no funciona, vuelve a flashear el último firmware bueno (apartado 5) y deja la rama o bórrala.

Nombres de rama: `exp/...` para experimentos y `fix/...` para arreglos que necesitan probarse antes.

## 3. Descargar el firmware

1. Abre https://github.com/mgbernal/zmk-config/actions y entra en la ejecución del commit que
   quieres. Tiene que estar en verde.
2. Al final de la página, en **Artifacts**, descarga `firmware` (es un .zip) y descomprímelo.
3. Dentro hay tres ficheros:
   - `kyria_left-…uf2`: mitad izquierda, la principal, que es la que se conecta al PC.
   - `kyria_right-…uf2`: mitad derecha.
   - `settings_reset-…uf2`: borra los emparejamientos Bluetooth. Solo se usa si hay problemas.

Si el CI falla en el paso **check**, el keymap tiene un error de formato: ejecuta
`python3 scripts/check_keymap.py` en local para verlo. Si falla en **build**, el error de
compilación aparece en el registro del paso «West Build».

## 4. Flashear (nice!nano v1)

Para cada mitad, empezando por la izquierda:

1. Conéctala por USB al PC.
2. Pulsa **dos veces seguidas** el botón de reset. Aparece una unidad USB llamada `NICENANO`.
3. Copia el `.uf2` de esa mitad a la unidad. Se desconecta sola y reinicia con el firmware nuevo.

Las dos mitades llevan el mismo keymap, pero conviene flashear siempre ambas para que no se
desincronicen.

**Si las mitades no se encuentran o el PC no conecta por Bluetooth:**
1. Flashea `settings_reset` en las dos mitades.
2. Vuelve a flashear `kyria_left` y `kyria_right`.
3. En Windows: Configuración → Bluetooth → quita el Kyria y vuelve a emparejarlo.

## 5. Guardar un firmware bueno y volver atrás

Los artefactos de Actions **caducan a los 90 días**. Cuando un firmware lleve un tiempo funcionando
bien en el teclado, márcalo con una etiqueta:

```sh
git tag fw-2026-11-13 <commit>   # sin <commit> se etiqueta el último
git push origin fw-2026-11-13
```

El CI crea una **Release** con los tres `.uf2`, que se guarda para siempre en
https://github.com/mgbernal/zmk-config/releases. Para volver atrás, descarga los `.uf2` de la
última Release buena y flashéalos (apartado 4). No hace falta tocar el código.

Para deshacer también el código, `git revert <commit>` crea un commit que deshace el cambio sin
reescribir el historial. No uses `git push --force` en `master`.

## 6. Actualizar ZMK

La versión de ZMK está fijada al mismo commit en dos sitios: `config/west.yml` (`revision`) y
`.github/workflows/build.yml` (la línea `uses: …@<commit>`). Para actualizar:

1. Hazlo en una rama `exp/zmk-AAAA-MM-DD`.
2. Cambia el commit en los dos ficheros.
3. Compila, flashea, prueba y, si va bien, intégralo como en el apartado 2.

No hay que poner `main` en lugar de un commit: un cambio de ZMK podría romper la compilación sin
que hayas tocado nada.

## 7. Acceso desde el VPS

En el VPS, `origin` usa la deploy key `~/.ssh/id_github_zmk` (alias SSH `github-zmk`), que solo tiene
permiso sobre este repositorio. Se gestiona en GitHub → Settings → Deploy keys. Si se compromete,
se borra allí y se crea otra.
