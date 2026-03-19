import sys
import os

def ask(prompt, options=None):
    if options:
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        while True:
            try:
                choice = int(input(prompt)) - 1
                if 0 <= choice < len(options):
                    return choice
            except ValueError:
                pass
            print("Opción no válida.")
    return input(prompt)

def create_qwidget(name, lower, directory):
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

    write_file(os.path.join(directory, f"{lower}.h"), header)
    write_file(os.path.join(directory, f"{lower}.cpp"), cpp)
    write_file(os.path.join(directory, f"{lower}.ui"), ui)
    print(f"\n✓ Creados: {lower}.h, {lower}.cpp, {lower}.ui")


def create_qobject(name, lower, directory):
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

    write_file(os.path.join(directory, f"{lower}.h"), header)
    write_file(os.path.join(directory, f"{lower}.cpp"), cpp)
    print(f"\n✓ Creados: {lower}.h, {lower}.cpp")


def write_file(path, content):
    if os.path.exists(path):
        overwrite = input(f"  '{path}' ya existe. ¿Sobreescribir? (s/N): ").strip().lower()
        if overwrite != 's':
            print(f"  Omitido: {path}")
            return
    with open(path, 'w') as f:
        f.write(content)


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
    tipo = ask("Selecciona (1/2): ", ["QWidget (con .ui)", "QObject (sin .ui)"])

    # Directorio de destino
    print(f"\nDirectorio de destino (Enter para usar '{root}'):")
    directory = input("> ").strip() or root

    # Expandir ~ si se usa
    directory = os.path.expanduser(directory)

    if not os.path.isabs(directory):
        directory = os.path.join(root, directory)

    os.makedirs(directory, exist_ok=True)

    print()
    if tipo == 0:
        create_qwidget(name, lower, directory)
    else:
        create_qobject(name, lower, directory)

    print(f"  Directorio: {directory}\n")


if __name__ == "__main__":
    main()
