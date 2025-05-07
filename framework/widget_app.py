import streamlit as st
from abc import ABC, abstractmethod

class Widget(ABC):
    def __init__(self, label: str, key: str = None):
        self.label = label
        self.key = key or label

    @abstractmethod
    def render(self):
        """Comportamento genérico do widget base."""
        st.markdown(f"⚠️ Widget genérico chamado: `{self.label}`")
        return None


class TextWidget(Widget):
    def __init__(self, label: str, default: str = "", key: str = None):
        super().__init__(label, key)
        self.default = default

    def render(self):
        return st.text_input(self.label, value=self.default, key=self.key)


class ButtonWidget(Widget):
    def __init__(self, label: str, key: str = None):
        super().__init__(label, key)

    def render(self):
        return st.button(self.label, key=self.key)


class SliderWidget(Widget):
    def __init__(self, label: str, min_value: int, max_value: int, default: int = None, key: str = None):
        super().__init__(label, key)
        self.min_value = min_value
        self.max_value = max_value
        self.default = default or min_value

    def render(self):
        return st.slider(self.label, min_value=self.min_value, max_value=self.max_value, value=self.default, key=self.key)


# Exemplo de uso
def main():
    st.title("Exemplo de Widgets Genéricos")

    nome = TextWidget("Digite seu nome", default="Fulano").render()
    idade = SliderWidget("Idade", min_value=0, max_value=120, default=25).render()

    if ButtonWidget("Enviar").render():
        st.success(f"Nome: {nome}, Idade: {idade}")
        st.toast(f"Nome: {nome}, Idade: {idade}")


if __name__ == "__main__":
    main()