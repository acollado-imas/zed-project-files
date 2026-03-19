import os
import re
import sys


def ask_choice(prompt, options):
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        try:
            choice = int(input(prompt)) - 1
            if 0 <= choice < len(options):
                return choice
        except ValueError:
            pass
        print("  Opción no válida.")


def write_file(path, content):
    if os.path.exists(path):
        overwrite = (
            input(f"  '{path}' ya existe. ¿Sobreescribir? (s/N): ").strip().lower()
        )
        if overwrite != "s":
            print(f"  Omitido: {path}")
            return False
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    return True


def add_to_pro(pro_path, sources=None, headers=None, forms=None):
    """Inserta entradas al final del primer SOURCES, HEADERS y FORMS del .pro."""
    with open(pro_path, "r") as f:
        content = f.read()

    def insert_at_last(content, block_name, new_entry):
        # Busca el bloque: líneas que continúan con \ al final
        # La última línea del bloque es la que NO termina en \
        pattern = rf"({re.escape(block_name)}\s*\+=\s*\\\n(?:[ \t]+\S[^\n]*\\\n)*)([ \t]+\S[^\n]*\n)"
        match = re.search(pattern, content)
        if match:
            # Añade \ a la última línea actual e inserta la nueva al final
            last_line = match.group(2)
            new_last = last_line.rstrip("\n") + " \\\n" + f"    {new_entry}\n"
            content = content[: match.start(2)] + new_last + content[match.end(2) :]
        else:
            print(f"  ⚠ No se encontró '{block_name} +=' en el .pro")
        return content

    if sources:
        content = insert_at_last(content, "SOURCES", sources)
    if headers:
        content = insert_at_last(content, "HEADERS", headers)
    if forms:
        content = insert_at_last(content, "FORMS", forms)

    with open(pro_path, "w") as f:
        f.write(content)

    print(f"  ✓ Actualizado: {os.path.basename(pro_path)}")


def find_pro_file(root):
    """Busca el primer .pro en la raíz del proyecto."""
    for f in os.listdir(root):
        if f.endswith(".pro"):
            return os.path.join(root, f)
    return None


def create_qwidget(name, lower, directory, root, rel_dir):
    header = f"""#ifndef {name.upper()}_H
#define {name.upper()}_H

#include <QWidget>

namespace Ui {{
class {name};
}}

class {name} : public QWidget
{{
    Q_OBJECT

public:
    explicit {name}(QWidget *parent = nullptr);
    ~{name}();

private:
    Ui::{name} *ui;
}};

#endif // {name.upper()}_H
"""

    cpp = f"""#include "{lower}.h"
#include "ui_{lower}.h"

{name}::{name}(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::{name})
{{
    ui->setupUi(this);
}}

{name}::~{name}()
{{
    delete ui;
}}
"""

    ui = f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>{name}</class>
 <widget class="QWidget" name="{name}">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>{name}</string>
  </property>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

    h_ok = write_file(os.path.join(directory, f"{lower}.h"), header)
    cpp_ok = write_file(os.path.join(directory, f"{lower}.cpp"), cpp)
    ui_ok = write_file(os.path.join(directory, f"{lower}.ui"), ui)

    print(f"\n  ✓ Creados: {lower}.h, {lower}.cpp, {lower}.ui")

    prefix = f"{rel_dir}/" if rel_dir else ""
    pro_path = find_pro_file(root)
    if pro_path:
        add_to_pro(
            pro_path,
            sources=f"{prefix}{lower}.cpp" if cpp_ok else None,
            headers=f"{prefix}{lower}.h" if h_ok else None,
            forms=f"{prefix}{lower}.ui" if ui_ok else None,
        )
    else:
        print("  ⚠ No se encontró ningún .pro en la raíz del proyecto")


def create_qobject(name, lower, directory, root, rel_dir):
    header = f"""#ifndef {name.upper()}_H
#define {name.upper()}_H

#include <QObject>

class {name} : public QObject
{{
    Q_OBJECT

public:
    explicit {name}(QObject *parent = nullptr);

signals:

}};

#endif // {name.upper()}_H
"""

    cpp = f"""#include "{lower}.h"

{name}::{name}(QObject *parent)
    : QObject(parent)
{{
}}
"""

    h_ok = write_file(os.path.join(directory, f"{lower}.h"), header)
    cpp_ok = write_file(os.path.join(directory, f"{lower}.cpp"), cpp)

    print(f"\n  ✓ Creados: {lower}.h, {lower}.cpp")

    prefix = f"{rel_dir}/" if rel_dir else ""
    pro_path = find_pro_file(root)
    if pro_path:
        add_to_pro(
            pro_path,
            sources=f"{prefix}{lower}.cpp" if cpp_ok else None,
            headers=f"{prefix}{lower}.h" if h_ok else None,
        )
    else:
        print("  ⚠ No se encontró ningún .pro en la raíz del proyecto")


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    print("=== Nueva clase Qt ===\n")

    # Nombre de la clase
    while True:
        name = input("Nombre de la clase (ej: MyWidget): ").strip()
        if name and name[0].isupper():
            break
        print("  El nombre debe empezar por mayúscula.")

    lower = name.lower()

    # Tipo de clase
    print("\nTipo de clase:")
    tipo = ask_choice("Selecciona (1/2): ", ["QWidget (con .ui)", "QObject (sin .ui)"])

    # Directorio de destino
    print(f"\nDirectorio de destino relativo a la raíz (Enter para usar la raíz):")
    rel_dir = input("> ").strip()

    directory = os.path.join(root, rel_dir) if rel_dir else root
    directory = os.path.expanduser(directory)
    os.makedirs(directory, exist_ok=True)

    print()
    if tipo == 0:
        create_qwidget(name, lower, directory, root, rel_dir)
    else:
        create_qobject(name, lower, directory, root, rel_dir)

    print(f"  Directorio: {directory}\n")


if __name__ == "__main__":
    main()
