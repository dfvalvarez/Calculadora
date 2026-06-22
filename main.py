from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

# Ajustar el tamaño de la ventana para que parezca un móvil
Window.size = (350, 550)

KV = '''
MDBoxLayout:
    orientation: "vertical"
    padding: 20
    spacing: 10
    md_bg_color: app.theme_cls.bg_light

    # Nuevo bloque para el historial
    MDLabel:
        id: history_label
        text: ""
        halign: "right"
        theme_text_color: "Secondary"
        size_hint_y: 0.15
        font_size: "16sp"

    # Pantalla principal
    MDTextField:
        id: display
        text: ""
        halign: "right"
        font_size: 48
        readonly: True
        mode: "fill"
        size_hint_y: 0.20

    MDGridLayout:
        cols: 4
        spacing: 10
        size_hint_y: 0.65

        # Fila 1
        MDRaisedButton:
            text: "AC"
            size_hint: 1, 1
            md_bg_color: 1, 0.3, 0.3, 1
            on_release: app.clear_all()
        MDRaisedButton:
            text: "DEL"
            size_hint: 1, 1
            md_bg_color: 1, 0.6, 0.2, 1
            on_release: app.delete_char()
        MDRaisedButton:
            text: ""
            disabled: True
            size_hint: 1, 1
        MDRaisedButton:
            text: "/"
            size_hint: 1, 1
            md_bg_color: 0.2, 0.6, 1, 1
            on_release: app.add_to_display("/")

        # Fila 2
        MDRaisedButton:
            text: "7"
            size_hint: 1, 1
            on_release: app.add_to_display("7")
        MDRaisedButton:
            text: "8"
            size_hint: 1, 1
            on_release: app.add_to_display("8")
        MDRaisedButton:
            text: "9"
            size_hint: 1, 1
            on_release: app.add_to_display("9")
        MDRaisedButton:
            text: "*"
            size_hint: 1, 1
            md_bg_color: 0.2, 0.6, 1, 1
            on_release: app.add_to_display("*")

        # Fila 3
        MDRaisedButton:
            text: "4"
            size_hint: 1, 1
            on_release: app.add_to_display("4")
        MDRaisedButton:
            text: "5"
            size_hint: 1, 1
            on_release: app.add_to_display("5")
        MDRaisedButton:
            text: "6"
            size_hint: 1, 1
            on_release: app.add_to_display("6")
        MDRaisedButton:
            text: "-"
            size_hint: 1, 1
            md_bg_color: 0.2, 0.6, 1, 1
            on_release: app.add_to_display("-")

        # Fila 4
        MDRaisedButton:
            text: "1"
            size_hint: 1, 1
            on_release: app.add_to_display("1")
        MDRaisedButton:
            text: "2"
            size_hint: 1, 1
            on_release: app.add_to_display("2")
        MDRaisedButton:
            text: "3"
            size_hint: 1, 1
            on_release: app.add_to_display("3")
        MDRaisedButton:
            text: "+"
            size_hint: 1, 1
            md_bg_color: 0.2, 0.6, 1, 1
            on_release: app.add_to_display("+")

        # Fila 5
        MDRaisedButton:
            text: "0"
            size_hint: 1, 1
            on_release: app.add_to_display("0")
        MDRaisedButton:
            text: ""
            disabled: True
            size_hint: 1, 1
        MDRaisedButton:
            text: "."
            size_hint: 1, 1
            on_release: app.add_to_display(".")
        MDRaisedButton:
            text: "="
            size_hint: 1, 1
            md_bg_color: 0.1, 0.8, 0.4, 1
            on_release: app.calculate()
'''

class CalculatorApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inicializamos la lista que guardará el historial
        self.history = []

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)

    def add_to_display(self, value):
        if self.root.ids.display.text == "Error":
            self.root.ids.display.text = ""
        self.root.ids.display.text += value

    # --- LÓGICA DE HISTORIAL ---
    def update_history(self, expression, result):
        # Guardamos el formato "2+2 = 4"
        entry = f"{expression} = {result}"
        self.history.append(entry)
        
        # Si nos pasamos de 5, eliminamos el más viejo (índice 0)
        if len(self.history) > 5:
            self.history.pop(0)
            
        # Actualizamos la etiqueta de la interfaz uniendo la lista con saltos de línea
        self.root.ids.history_label.text = "\n".join(self.history)

    # --- LÓGICA RECURSIVA DE BORRADO ---
    def delete_recursively(self, text, chars_to_delete):
        if chars_to_delete <= 0 or text == "":
            return text
        return self.delete_recursively(text[:-1], chars_to_delete - 1)

    def delete_char(self):
        current_text = self.root.ids.display.text
        self.root.ids.display.text = self.delete_recursively(current_text, 1)

    def clear_all(self):
        current_text = self.root.ids.display.text
        self.root.ids.display.text = self.delete_recursively(current_text, len(current_text))

    # --- LÓGICA RECURSIVA MATEMÁTICA ---
    def evaluate_recursive(self, expr):
        if not expr:
            return 0.0
        
        try:
            return float(expr)
        except ValueError:
            pass

        for op in ['+', '-']:
            idx = expr.rfind(op)
            if idx > 0 and expr[idx-1] not in ['+', '-', '*', '/']:
                left = self.evaluate_recursive(expr[:idx])
                right = self.evaluate_recursive(expr[idx+1:])
                if op == '+': return left + right
                if op == '-': return left - right

        for op in ['*', '/']:
            idx = expr.rfind(op)
            if idx > 0:
                left = self.evaluate_recursive(expr[:idx])
                right = self.evaluate_recursive(expr[idx+1:])
                if op == '*': return left * right
                if op == '/': 
                    if right == 0:
                        raise ZeroDivisionError
                    return left / right

        return 0.0

    def calculate(self):
        expression = self.root.ids.display.text
        if expression:
            try:
                result = self.evaluate_recursive(expression)
                
                if result.is_integer():
                    result_str = str(int(result))
                else:
                    result_str = str(result)
                
                # Actualizar el historial antes de cambiar la pantalla principal
                self.update_history(expression, result_str)
                self.root.ids.display.text = result_str
                
            except ZeroDivisionError:
                self.root.ids.display.text = "Error"
            except Exception:
                self.root.ids.display.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()