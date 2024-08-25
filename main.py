from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from utils import generate_password
from kivy.core.window import Window 

Window.clearcolor = (0,0,0,0)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(text = 'Gerenciador de Senhas', font_size ='32sp', color =(1,1,1,1), size_hint =(1,0.2))
        layout.add_widget(title)

        btn_generate = Button(text="Gerar Senha", size_hint=(1, 0.2),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        btn_generate.bind(on_press=self.go_to_generate_password)
        layout.add_widget(btn_generate)

        btn_store = Button(text="Armazenar Senhas e Login",size_hint=(1, 0.2),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        btn_store.bind(on_press=self.go_to_store_passwords)
        layout.add_widget(btn_store)

        self.add_widget(layout)

    def go_to_generate_password(self, instance):
        self.manager.current = 'generate'

    def go_to_store_passwords(self, instance):
        self.manager.current = 'store'

class GeneratePasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.password_input = TextInput(hint_text='Generated Password',readonly=True,font_size=24)
        layout.add_widget(self.password_input)

        generate_button = Button(text='Generate Password', size_hint=(1, 0.2),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        generate_button.bind(on_press=self.generate_password)
        layout.add_widget(generate_button)

        copy_button = Button(text='Copy Password', size_hint=(1, 0.2),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        copy_button.bind(on_press=self.copy_password)
        layout.add_widget(copy_button)

        back_button = Button(text='Voltar', size_hint=(1, 0.2),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def generate_password(self, instance):
        password = generate_password()
        self.password_input.text = password

    def copy_password(self, instance):
        Clipboard.copy(self.password_input.text)

    def go_back(self, instance):
        self.manager.current = 'menu'

class StorePasswordsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logins = []

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # ScrollView para exibir os logins armazenados
        self.scroll_view = ScrollView(size_hint=(1, 0.7))
        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)

        # Botão para adicionar login
        add_button = Button(text='Adicionar Login', size_hint=(1, 0.1),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        add_button.bind(on_press=self.show_add_popup)
        layout.add_widget(add_button)

        # Botão para voltar
        back_button = Button(text='Voltar', size_hint=(1, 0.1),background_color=(0.4, 0.4, 0.4, 1),font_size ='20sp',color=(1, 1, 1, 1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.login_name_input = TextInput(hint_text='Nome do Login (Ex: Serasa)', multiline=False)
        self.login_user_input = TextInput(hint_text='Email ou Nome de Usuário', multiline=False)
        self.login_password_input = TextInput(hint_text='Senha', multiline=False)

        content.add_widget(self.login_name_input)
        content.add_widget(self.login_user_input)
        content.add_widget(self.login_password_input)

        save_button = Button(text='Salvar', size_hint=(1, 0.2))
        save_button.bind(on_press=self.save_login)
        content.add_widget(save_button)

        self.add_popup = Popup(title='Adicionar Novo Login', content=content, size_hint=(0.9, 0.5))
        self.add_popup.open()

    def save_login(self, instance):
        login_name = self.login_name_input.text
        login_user = self.login_user_input.text
        login_password = self.login_password_input.text

        if login_name and login_user and login_password:
            login_data = f"{login_name}\nUsuário: {login_user}\nSenha: {login_password}"
            self.logins.append(login_data)

            login_label = Label(text=login_data, size_hint_y=None, height=80)
            remove_button = Button(text='Remover', size_hint_y=None, height=40)
            remove_button.bind(on_press=lambda x: self.remove_login(login_label, remove_button))

            self.grid.add_widget(login_label)
            self.grid.add_widget(remove_button)
        
        self.add_popup.dismiss()  # Fecha o popup

    def remove_login(self, login_label, remove_button):
        self.grid.remove_widget(login_label)
        self.grid.remove_widget(remove_button)

    def go_back(self, instance):
        self.manager.current = 'menu'


def show_add_popup(self, instance):
    content = BoxLayout(orientation='vertical', padding=20, spacing=10)

    self.login_name_input = TextInput(hint_text='Nome do Login (Ex: Serasa)', multiline=False,background_color=(0.4, 0.4, 0.4, 1))
    self.login_user_input = TextInput(hint_text='Email ou Nome de Usuário', multiline=False,background_color=(0.4, 0.4, 0.4, 1))
    self.login_password_input = TextInput(hint_text='Senha', multiline=False,background_color=(0.4, 0.4, 0.4, 1))

    content.add_widget(self.login_name_input)
    content.add_widget(self.login_user_input)
    content.add_widget(self.login_password_input)

    save_button = Button(text='Salvar', size_hint=(1, 0.2))
    save_button.bind(on_press=self.save_login)
    content.add_widget(save_button)

    self.add_popup = Popup(title='Adicionar Novo Login', content=content, size_hint=(0.9, 0.5))
    self.add_popup.open()

def save_login(self, instance):
    login_name = self.login_name_input.text
    login_user = self.login_user_input.text
    login_password = self.login_password_input.text

    if login_name and login_user and login_password:
        login_data = f"{login_name}\nUsuário: {login_user}\nSenha: {login_password}"
        self.logins.append(login_data)

        login_label = Label(text=login_data, size_hint_y=None, height=80)
        remove_button = Button(text='Remover', size_hint_y=None, height=40)
        remove_button.bind(on_press=lambda x: self.remove_login(login_label, remove_button))

        self.grid.add_widget(login_label)
        self.grid.add_widget(remove_button)
    
    self.add_popup.dismiss()  # Fecha o popup


    def remove_login(self, login_label, remove_button):
        self.grid.remove_widget(login_label)
        self.grid.remove_widget(remove_button)

    def go_back(self, instance):
        self.manager.current = 'menu'

class PasswordApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GeneratePasswordScreen(name='generate'))
        sm.add_widget(StorePasswordsScreen(name='store'))
        return sm

if __name__ == '__main__':
    PasswordApp().run()
