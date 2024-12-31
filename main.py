import tkinter as tk
from tkinter import PhotoImage, StringVar, Entry, Listbox, Frame, Label, SINGLE, END, ACTIVE,ttk,LEFT
from tkinter import messagebox
import requests
import asyncio
from PIL import Image, ImageTk
import time
import re
import sys
import os
from MODULES import TypeInteractions
#                 ESSENCIAIS   ESSENCIAIS  ESSENCIAIS  ESSENCIAIS  ESSENCIAIS  ESSENCIAIS  ESSENCIAIS  ESSENCIAIS  ESSENCIAIS
from typing import List, Dict, Union, Optional, Literal
global RowCount


class PokemonCACHE:
    def __init__(self, limit: int = 50):
        self.limit = limit
        self.data: Dict[str, List[Dict]] = {}
    def GetSize(self):
        return len(self.data)
    def add_json(self, json_obj: Dict, data_type: Literal["DoRequest",  "AlternativeForms"]):
        if data_type not in self.data:
            self.data[data_type] = []

        if len(self.data[data_type]) < self.limit:
            self.data[data_type].append(json_obj)
        else:
            # Sobrescreve o mais antigo
            index = len(self.data[data_type]) % self.limit
            self.data[data_type][index] = json_obj

    def search_json(self, name: str, data_type: Literal["DoRequest",  "AlternativeForms"]) -> Optional[Dict]:
        """
        Busca um JSON pelo nome dentro do tipo especificado.
        """
        if self.GetSize()==0:
            return None
        if data_type not in self.data:
            return None
        if data_type == "DoRequest":

            for item in self.data[data_type]:
                
                if item.get("forms", {})[0].get("name",{}) == name:
                    
                    return item



        if data_type == "AlternativeForms":
            for item in self.data[data_type]:
               
                if item.get("varieties", {})[0].get("pokemon",{}).get("name",{}) == name:
                    return item
        
        return None

    def get_data(self, data_type: Literal["DoRequest",  "AlternativeForms"]) -> List[Dict]:
        """
        Retorna todos os dados armazenados para o tipo especificado.
        """
        return self.data.get(data_type, [])
global GlobalCACHE
GlobalCACHE = PokemonCACHE()

def center_SideWindow(root,targetToSide):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Obter as dimensões da janela
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calcular a posição
    x_pos = (screen_width - window_width )- 560
    y_pos = ((screen_height - window_height) // 2 )-150

    # Definir a geometria da janela
    root.geometry(f'{350}x{155}+{x_pos-150}+{y_pos}')
def center_window(root):
    # Atualizar as dimensões da janela após a criação
    root.update_idletasks()

    # Obter as dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Obter as dimensões da janela
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calcular a posição
    x_pos = screen_width - window_width  # Coloca a janela à direita
    y_pos = (screen_height - window_height) // 2  # Coloca a janela no meio verticalmente

    # Definir a geometria da janela
    root.geometry(f'{window_width}x{window_height}+{x_pos}+{y_pos}')
class BarraDeComandos():
    def __init__(self, janela):
        global RowCount 
        
        self.janela = janela

        self.barra_comandos = tk.Frame(self.janela, bg="#2E2E2E", relief="raised", bd=2)
        self.barra_comandos.pack(side="top", fill="x")

        # Botão de fechar na barra personalizada
        self.btn_fechar = tk.Button(self.barra_comandos, text="X", bg="#2E2E2E", fg="white", command=self.fechar_janela)
        self.btn_fechar.pack(side="right", padx=5, pady=2)
   
        # Canvas e Scrollbar para as abas
        self.canvas_abas = tk.Canvas(self.barra_comandos, bg="gray", height=30, highlightthickness=0)
        self.scrollbar_abas = ttk.Scrollbar(self.barra_comandos, orient="horizontal", command=self._scroll_canvas)
        self.barra_abas = tk.Frame(self.canvas_abas, bg="gray")

        # Configurar canvas para suportar rolagem
        self.canvas_abas.create_window((0, 0), window=self.barra_abas, anchor="nw")
        self.canvas_abas.configure(xscrollcommand=self.scrollbar_abas.set)

        # Posicionar canvas e scrollbar
        self.canvas_abas.pack(side="left", fill="x", expand=True, padx=5, pady=2)
        self.scrollbar_abas.pack(side="bottom", fill="x")

        # Dropdown para adicionar novas abas
        self.dropdown_menu = tk.Menubutton(self.barra_abas, text="+", bg="green", fg="white", relief="raised")
        self.menu = tk.Menu(self.dropdown_menu, tearoff=0)
        self.dropdown_menu.config(menu=self.menu)

        # Adicionar opções de tipos de abas
        self.menu.add_command(label="Buscar nome", command=lambda: self.criar_tipo_de_aba("Pokemon"))
        self.menu.add_command(label="Buscar tipos", command=lambda: self.criar_tipo_de_aba("Type"))
        self.menu.add_command(label="Duplas", command=lambda: self.criar_tipo_de_aba("Duals"))
        self.dropdown_menu.pack(side="left", padx=5, pady=2)

        RowCount = 0

        self.abas = {}
        self.SideBars = {}
        self.frames = {}

        # Vincular eventos para ajustar o canvas
        self.barra_abas.bind("<Configure>", self._ajustar_canvas)

    def _ajustar_canvas(self, event=None):
        """Ajusta a região de rolagem do canvas ao conteúdo."""
        self.canvas_abas.configure(scrollregion=self.canvas_abas.bbox("all"))

    def _scroll_canvas(self, *args):
        """Controla a rolagem horizontal com limites."""
        try:
            scroll_amount = float(args[1])  # Captura a quantidade de rolagem como um número decimal
        except ValueError:
            return  # Ignora rolagens inválidas
        
        if scroll_amount < 0 and self.canvas_abas.xview()[0] <= 0:  # Checa o limite esquerdo
            return
        elif scroll_amount > 0 and self.canvas_abas.xview()[1] >= 1:  # Checa o limite direito
            return
        
        # Realiza o deslocamento, convertendo o scroll_amount para um número inteiro
        self.canvas_abas.xview_scroll(int(scroll_amount), "units")

    def CreateSinglesSideBar(self):
        

        global RowCount
        self.SideBar = tk.Toplevel(self.janela)
    
        center_SideWindow(self.SideBar,self.SideBar)
        self.SideBar.overrideredirect(True)
        self.SideBar.attributes("-topmost", True)  # Sempre acima
        self.SideBar.config(bg="#2e2e2e")
        self.SideBars[RowCount] = self.SideBar
        return self.SideBar

    def Rename(self,OldName,NewName):
        
        for i in self.abas:
            if i == OldName:
                i = NewName
            return

    def criar_tipo_de_aba(self,type):
        if(type=="Pokemon"):
            Data = self.criar_nova_aba(type)
            Frame = Data[0]
            Btn = Data[1]
            NomeABA = Data[2]
      
            
            SearchBox(Frame,self.Rename).SearchByPokeName(self.janela,Btn,SideBar=self.CreateSinglesSideBar)

        elif(type=="Type"):
            Data = self.criar_nova_aba(type)
            Frame = Data[0]
            Btn = Data[1]
            NomeABA = Data[2]
            SearchBox(Frame,self.Rename).SearchByTypes()
        elif(type=="Duals"):
            Data = self.criar_nova_aba(type)
            Frame = Data[0]
            Btn = Data[1]
            NomeABA = Data[2]
            SearchBox(Frame,self.Rename).SearchDuals(self.janela,Btn,Zerado=True)
        
        
    def fechar_janela(self):
        self.janela.destroy()
    def selecionar_aba(self,aba):
        for frame in self.frames.values():
            frame.pack_forget()  # Esconde todos os self.frames
        if aba in self.frames:
            self.frames[aba].pack(fill="both", expand=True)  # Exibe o frame selecionado
        if aba in self.SideBars:
            self.SideBars[aba].deiconify()

        self.CloseAllSideBars()

    def CloseAllSideBars(self):
        for SideBar in self.SideBars.values():
            SideBar.withdraw()


    def criar_nova_aba(self,Pokename):
        self.CloseAllSideBars()

        global RowCount
        nome_aba = f"{Pokename} {RowCount}"
        RowCount += 1
        aba_frame = tk.Frame(self.barra_abas)
        aba_frame.pack(side="left", padx=5, pady=2)
        aba_botao = tk.Button(aba_frame, text=nome_aba, relief="raised", bg="#444",fg="#fff" ,
                            command=lambda: self.selecionar_aba(nome_aba))
        aba_botao.pack(side="left")
        aba_fechar = tk.Button(aba_frame, text="x", bg="#444", fg="white", 
                            font=("Arial", 8), command=lambda: self.fechar_aba(nome_aba, aba_frame))
        aba_fechar.pack(side="left", padx=2)
        self.abas[nome_aba] = aba_frame
        frame = tk.Frame(self.janela, bg="#2E2E2E")
        self.frames[nome_aba] = frame
   
        self.selecionar_aba(nome_aba)
        self.dropdown_menu.pack_forget()
        self.dropdown_menu.pack(side="left", padx=5, pady=2)
        return frame,aba_botao,nome_aba
    def fechar_aba(self,nome_aba, aba_frame):
        if nome_aba in self.frames:
            self.frames[nome_aba].destroy()  # Destroi o conteúdo da aba
            del self.frames[nome_aba]       # Remove a aba do dicionário
        if nome_aba in self.abas:
            aba_frame.destroy()        # Remove o botão da aba
            del self.abas[nome_aba]
class PokeJsonHandle():
    def GetPokeType(self,json):
        tipos = [t['type']['name'] for t in json['types']]
        
        return tipos

class PokemonTypeWidget(tk.Frame):
    
    def __init__(self, parent, icons_with_text,damageMultiplierText,IconSize=50, *args, **kwargs):
     
        super().__init__(parent, *args, **kwargs)
        self.configure(bg="#2E2E2E")
        # Verifica se há até 10 elementos
        if len(icons_with_text) > 15:
            raise ValueError("O widget suporta no máximo 10 ícones com texto.")

        self.images = []  # Lista para armazenar referências às imagens


        for index, (icon_path, text) in enumerate(icons_with_text):
            # Carrega a imagem do ícone
            
            try:
                img = Image.open(icon_path)
                width, height = img.size
                new_width = int(width * (IconSize/ 100))
                new_height = int(height * (IconSize/ 100))
                img = img.resize((new_width,new_height))
                image = ImageTk.PhotoImage(img)
            except:
                print("Error: Loading ico error")
        
            self.images.append(image)  # Necessário para manter a referência

            # Cria um Frame para organizar ícone e texto
            frame = tk.Frame(self)
            frame.configure(bg="#2E2E2E")
            frame.grid(row=(index // 5)+3, column=index % 5)

            # Adiciona o ícone ao Frame
            label_icon = tk.Label(frame, image=image,bg="#2E2E2E")
            label_icon.pack(side="top")

            # Adiciona o texto ao Frame
            label_text = tk.Label(frame, text=damageMultiplierText[index], font=("Arial", 12),fg="#fff",bg="#2E2E2E")
            label_text.pack(side="bottom")
           
        self.grid_rowconfigure(0, weight=0)  # Não redimensiona a primeira linha
        self.grid_columnconfigure(0, weight=1)  # Expande a coluna se necessário
class PokeInfoRequests():
    def __init__(self,pokename):
        self.pokename = pokename
        self.UrlPoke = "https://pokeapi.co/api/v2/pokemon/"
        self.UrlTCG = "https://api.pokemontcg.io/v2/cards?q=name:"
        self.SpeciesURL = "https://pokeapi.co/api/v2/pokemon-species/"
        
    def DoRequest(self):
        try:
            CheckIfOnCache =  GlobalCACHE.search_json(self.pokename,"DoRequest")
            
            if( CheckIfOnCache != None):
                print("DO REQUEST:: RETORNANDO VALOR EM CACHE!!!!")
                return CheckIfOnCache
            
            print("requisitando ao API")
            response = requests.get(self.UrlPoke+self.pokename)
            print(self.UrlPoke+self.pokename)
            response.raise_for_status()
            
            GlobalCACHE.add_json(response.json(),"DoRequest")
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return self.DoPokeNumberRequest(self.DoRequestViaTCG())
        
    def CapitalizeFirstLetter(self,A):
        if(A != None):
            Capitalized = ""
            Capitalized += A[0].upper()
            Capitalized += A[1:]
            return Capitalized
        return A
    def DoPokeNumberRequest(self,pokedexNumber):
        try:

            response = requests.get(self.UrlPoke+str(pokedexNumber))
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os dados do Pokémon: {e}")
    def DoRequestViaTCG(self):
       
        try:
            


            response = requests.get(self.UrlTCG+self.CapitalizeFirstLetter(self.pokename))
            response.raise_for_status()
            data = response.json().get('data', [])
            if not data:
                print(f"Nenhuma carta encontrada para o Pokémon '{self.pokename}'.")
                return 1
            for card in data:
                if 'nationalPokedexNumbers' in card:
                    pokedex_number = card['nationalPokedexNumbers'][0]
                    
                    
                    return pokedex_number
        except:
            return 1
    def DoRequestPokeForms(self):

        Pokedexnumber = self.DoRequestViaTCG()
        print("Requesting pokeform")
        try:        
            response = requests.get(self.SpeciesURL + str(Pokedexnumber))
    
            if response.status_code != 200:
                return f"Erro: Não foi possível encontrar o Pokémon '{Pokedexnumber}'."

            pokemon_data = response.json()


            return pokemon_data['varieties']

        except:
            return None
class GetPokeInfo(tk.Frame): # 5 referencias (possivelmente não necessárias)

    
    def __init__(self, parent,poke_view_instance):
        super().__init__(parent)
        self.parent = parent
        self.FramePokeinfo = Frame(parent, bg="#2E2E2E")
       
        self.AbilitiesList = tk.Listbox(parent)
        self.poke_view_instance = poke_view_instance  
        self.Pokename = ""
       
        self.FramePokeinfo.pack()
        
   
    def GetPokeAbilities(self,Name): # OK!!
        self.Pokename = Name
        Poke_Abilities = []
        response = PokeInfoRequests(Name).DoRequest()  
        

        for i in range(0,len(response['abilities'])):
            Poke_Abilities.append(response['abilities'][i]['ability']['name'])

        return Poke_Abilities


    # Valores de exemplo
    
    def GetPokeAlternativeForms(self, Listbox):
        alternative_forms = PokeInfoRequests(self.Pokename).DoRequestPokeForms()
        for i in alternative_forms:           
            Listbox.insert(END, i['pokemon']['name'])
        Listbox.delete(0)
        Listbox.bind("<<ListboxSelect>>", self.SelectAlternativeForm)
    def SelectAlternativeFormOnDuals(self,event,poke2):
        selected_index = event.widget.curselection()
        if selected_index:
            selected_item = event.widget.get(selected_index[0])
            # Chama o método atualizar_dados em PokeView
            self.poke_view_instance.atualizar_dados_Duals(selected_item,poke2)

    def SelectAlternativeForm(self, event):
        # Obtém o nome selecionado no Listbox
        selected_index = event.widget.curselection()
        if selected_index:
            selected_item = event.widget.get(selected_index[0])
            # Chama o método atualizar_dados em PokeView
            self.poke_view_instance.atualizar_dados(selected_item)

    def CreateDualsGroup(self,PokeName1,PokeName2,parent):
        for widget in parent.winfo_children():
            widget.destroy()
        def SwitchOn(PokeInField,Pokename):
            for widget in parent.winfo_children():
                widget.destroy()
            if(PokeInField == 1):
                SearchBox(parent).SearchDuals(DefaultValue1="",DefaultValue2=Pokename)       
            elif(PokeInField == 2):
                SearchBox(parent).SearchDuals(DefaultValue1=Pokename,DefaultValue2="")
            
        Pokename1 = PokeName1
        Pokename2 = PokeName2
        DualsPanel1 = self.CreateDualsPanel(parent,Pokename1,Pokename2)
        DualsPanel2 = self.CreateDualsPanel(parent,Pokename2,Pokename1)

        PokeInField1 = DualsPanel1[0]
        PokeInField2 = DualsPanel2[0]
        SwitchInPoke1 = DualsPanel1[1]
        SwitchInPoke2 = DualsPanel2[1]
        SwitchInPoke1.config(command= lambda :SwitchOn(1,Pokename2))
        SwitchInPoke2.config(command= lambda :SwitchOn(2,Pokename1))
        PokeInField1.pack()
        PokeInField2.pack()
        FillDualsInteractions(parent,Pokename1,Pokename2)
    def CreateDualsPanel(self, parent,pokemon_name,Poke2):
        
        panel = tk.Frame(parent, bg="#2E2E2E")
        frame_image = tk.Frame(panel, bg="#2E2E2E")
        frame_image.grid(row=0, column=0, padx=10, sticky="w")
        try:
            
            data = PokeInfoRequests(pokemon_name).DoRequest()
            image_url = data['sprites']['front_default']
            img = Image.open(requests.get(image_url, stream=True).raw)
            img = img.resize((80, 80))
            img_tk = ImageTk.PhotoImage(img)
            label_image = tk.Label(frame_image, image=img_tk, bg="#2E2E2E")
            SwitchInButton = tk.Button(frame_image,text="SWITCH")
            SwitchInButton.grid(row=1,column=0)
            label_image.image = img_tk  # Manter referência da imagem
            label_image.grid(row=0, column=0)  # Usando grid aqui

        except requests.exceptions.RequestException as e:
            label_error = tk.Label(frame_image, text="Erro ao carregar imagem", bg="#2E2E2E", fg="white")
            label_error.grid(row=0, column=0)  # Usando grid também aqui

        # Frame para habilidades
        frame_abilities = tk.Frame(panel, bg="#2E2E2E")
        frame_abilities.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        label_title = tk.Label(frame_abilities, text="Habilidades", font=("Arial", 14), bg="#2E2E2E", fg="white")
        label_title.grid(row=0, column=0, sticky="nw", padx=5)

        # Obter habilidades e descrições
        pokeab = self.GetPokeAbilities(pokemon_name)
        abilities_descriptions = self.get_ability_descriptions(pokemon_name)  # Método que retorna as descrições

        # Configurar Listbox
        listbox = tk.Listbox(frame_abilities, height=len(pokeab), bg="#2E2E2E", fg="white", selectmode=SINGLE)
        AlternativeForms= tk.Listbox(frame_abilities, height=4, bg="#2E2E2E", fg="white", selectmode=SINGLE)
        for ability in pokeab:
            listbox.insert(END, ability)
        self.GetPokeAlternativeForms(AlternativeForms)
        listbox.grid(row=1, column=0, sticky="nsew")
        AlternativeForms.grid(row=1, column=1, sticky="nsew")       
        description_frame = tk.Frame(frame_abilities, bg="#2E2E2E", width=250)  # Largura fixa
        description_frame.grid(row=2, columnspan=2,column=0, padx=10, pady=10, sticky="nsew")
        description_label = tk.Label(description_frame, text="", bg="#2E2E2E", fg="yellow", wraplength=330, justify="left")
       
        description_label.grid(row=0,columnspan=2, column=0)

        # Atualizar descrição ao clicar no item
        def update_description(event):
            # Obtém o índice do item selecionado
            index = listbox.curselection()
            if index:
                description_label.config(text=abilities_descriptions[index[0]])

        listbox.bind("<<ListboxSelect>>", update_description)

        AlternativeForms.bind("<<ListboxSelect>>", lambda x: self.SelectAlternativeFormOnDuals(x,Poke2))
        # Configure o grid para garantir que a coluna da descrição tenha uma largura fixa
        frame_abilities.grid_columnconfigure(0, weight=1)  # A `Listbox` ocupa o restante do espaço
        frame_abilities.grid_columnconfigure(1, minsize=250)  # A coluna de descrição tem largura fixa

        return panel,SwitchInButton
    def create_pokemon_panel(self, pokemon_name,func=None):
        panel = tk.Frame(self.parent, bg="#2E2E2E")
        frame_image = tk.Frame(panel, bg="#2E2E2E")
        frame_image.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        try:
 
            data = PokeInfoRequests(pokemon_name).DoRequest()
            image_url = data['sprites']['front_default']

            img = Image.open(requests.get(image_url, stream=True).raw)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            Stats = tk.Button(frame_image,text="stats",command=func)
            label_image = tk.Label(frame_image, image=img_tk, bg="#2E2E2E")
            label_image.image = img_tk  # Manter referência da imagem
        
            

            Stats.grid(row=1,column=0)
            label_image.grid(row=0, column=0)  # Usando grid aqui
        except requests.exceptions.RequestException as e:
            label_error = tk.Label(frame_image, text="Erro ao carregar imagem", bg="#2E2E2E", fg="white")
            label_error.grid(row=0, column=0)  # Usando grid também aqui

        # Frame para habilidades
        frame_abilities = tk.Frame(panel, bg="#2E2E2E")
        frame_abilities.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        label_title = tk.Label(frame_abilities, text="Habilidades", font=("Arial", 14), bg="#2E2E2E", fg="white")
        label_title.grid(row=0, column=0, sticky="nw", padx=5)

        # Obter habilidades e descrições
        pokeab = self.GetPokeAbilities(pokemon_name)
        abilities_descriptions = self.get_ability_descriptions(pokemon_name)  # Método que retorna as descrições

        # Configurar Listbox
        listbox = tk.Listbox(frame_abilities, height=len(pokeab), bg="#2E2E2E", fg="white", selectmode=SINGLE)
        AlternativeForms= tk.Listbox(frame_abilities, height=4, bg="#2E2E2E", fg="white", selectmode=SINGLE)

        for ability in pokeab:
            listbox.insert(END, ability)
        
        self.GetPokeAlternativeForms(AlternativeForms)

        
        listbox.grid(row=1, column=0, sticky="nsew")
        AlternativeForms.grid(row=1, column=1, sticky="nsew")

        
        description_frame = tk.Frame(frame_abilities, bg="#2E2E2E", width=250)  # Largura fixa
        description_frame.grid(row=2, columnspan=2,column=0, padx=10, pady=10, sticky="nsew")
        description_label = tk.Label(description_frame, text="", bg="#2E2E2E", fg="yellow", wraplength=330, justify="left")
       
        description_label.grid(row=0,columnspan=2, column=0)


        # Atualizar descrição ao clicar no item
        def update_description(event):
            # Obtém o índice do item selecionado
            index = listbox.curselection()
            if index:
                description_label.config(text=abilities_descriptions[index[0]])

        listbox.bind("<<ListboxSelect>>", update_description)

        AlternativeForms.bind("<<ListboxSelect>>", self.SelectAlternativeForm)
        # Configure o grid para garantir que a coluna da descrição tenha uma largura fixa
        frame_abilities.grid_columnconfigure(0, weight=1)  # A `Listbox` ocupa o restante do espaço
        frame_abilities.grid_columnconfigure(1, minsize=250)  # A coluna de descrição tem largura fixa

        return panel



    def get_ability_descriptions(self, pokemon_name):
        descriptions = []
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for ability in data['abilities']:
                ability_url = ability['ability']['url']
                ability_response = requests.get(ability_url)

                if ability_response.status_code == 200:
                    ability_data = ability_response.json()
                    effect_entries = ability_data['effect_entries']

                    # Filtrar pelo idioma português
                    description_pt = next(
                        (entry['short_effect'] for entry in effect_entries if entry['language']['name'] == 'en'),
                        None
                    )

                    if description_pt:
                        descriptions.append(description_pt)
                    else:
                        descriptions.append("Descrição não disponível")
        else:
            print("Erro ao buscar habilidades do Pokémon.")
        
        return descriptions 

def FillDualsInteractions(parent,Poke1,Poke2):
        TextIconsWeakness = []
        TextIconsImunities = []
        TextIconsResistences = []
        ImunitiesMultipyers = []
        ArrayDosTipos1 = PokeJsonHandle().GetPokeType(PokeInfoRequests(Poke1).DoRequest())
        ArrayDosTipos2 = PokeJsonHandle().GetPokeType(PokeInfoRequests(Poke2).DoRequest())

        if((len(ArrayDosTipos1)>1) and (len(ArrayDosTipos2)>1)):
             GlobalTypeInteractions = TypeInteractions.DualsTypeInteraction(TypeInteractions.StrenghtAndWeakness(ArrayDosTipos1[0],ArrayDosTipos1[1]),TypeInteractions.StrenghtAndWeakness(ArrayDosTipos2[0],ArrayDosTipos2[1]))

        elif (len(ArrayDosTipos1)==1 and len(ArrayDosTipos2)==1):
            GlobalTypeInteractions = TypeInteractions.DualsTypeInteraction(TypeInteractions.StrenghtAndWeakness(ArrayDosTipos1[0],None),TypeInteractions.StrenghtAndWeakness(ArrayDosTipos2[0],None))
            
        elif (len(ArrayDosTipos1)>1 and len(ArrayDosTipos2)==1):
            GlobalTypeInteractions = TypeInteractions.DualsTypeInteraction(TypeInteractions.StrenghtAndWeakness(ArrayDosTipos1[0],ArrayDosTipos1[1]),TypeInteractions.StrenghtAndWeakness(ArrayDosTipos2[0],None))
        elif (len(ArrayDosTipos1) == 1 and len(ArrayDosTipos2)>1):
            GlobalTypeInteractions = TypeInteractions.DualsTypeInteraction(TypeInteractions.StrenghtAndWeakness(ArrayDosTipos1[0],None),TypeInteractions.StrenghtAndWeakness(ArrayDosTipos2[0],ArrayDosTipos2[1]))




            
        Weakness = GlobalTypeInteractions[0]
        Imunities = GlobalTypeInteractions[1]
        Resistences = GlobalTypeInteractions[2]
         
        if(len(Resistences)==0):
            Resistences = ["none 0.5x"]
        
        if(len(Imunities)==0):
            Imunities = ["none 0x"]
        
        if(len(Weakness)==0):
            Weakness = ["none 0x"]
        
        for tipo in Weakness:
            if getattr(sys, 'frozen', False):
                # Estamos rodando a partir de um executável
                caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
            else:
                # Estamos rodando no ambiente de desenvolvimento
                caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
              
            TextIconsWeakness.append((caminho_icone, ""))

        for tipo in Imunities:
            if getattr(sys, 'frozen', False):
                # Estamos rodando a partir de um executável
                caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
                ImunitiesMultipyers.append("0X")
            else:
                # Estamos rodando no ambiente de desenvolvimento
                caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
                ImunitiesMultipyers.append("0X")
            TextIconsImunities.append((caminho_icone, ""))
        
        for tipo in Resistences:
            if getattr(sys, 'frozen', False):
                # Estamos rodando a partir de um executável
                caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
            else:
                # Estamos rodando no ambiente de desenvolvimento
                caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
            TextIconsResistences.append((caminho_icone, ""))


        damageMultiplierText = []






        for tipo in Weakness:
            if len(tipo.split(" ")) == 3:
               damageMultiplierText.append("4x")
            else:
                damageMultiplierText.append("2x")
        ResistencesMultiplierText = []
        for tipo in Resistences:
            if len(tipo.split(" ")) == 2:
               ResistencesMultiplierText.append(tipo.split(" ")[1])
            else:
                ResistencesMultiplierText.append("2x")
        
        tipo_widget = PokemonTypeWidget(parent,TextIconsWeakness,damageMultiplierText)

        tipo_widget2 = PokemonTypeWidget(parent,TextIconsResistences,ResistencesMultiplierText)

        tipo_widget3 = PokemonTypeWidget(parent,TextIconsImunities,ImunitiesMultipyers)

        divisoriaFraquezas = tk.Label(parent,fg="#00FFFF",bg="#2E2E2E" ,text="----- Fraquezas -----", font=("Arial", 10, "bold"))
        divisoriaImunidades= tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="----- Imunidades -----", font=("Arial", 10, "bold"))
        divisoriaResistencias = tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="----- Resistencias -----", font=("Arial", 10, "bold"))
        
        divisoriaFraquezas.pack()
        tipo_widget.pack()
        divisoriaResistencias.pack()

        tipo_widget2.pack()
        divisoriaImunidades.pack()
        tipo_widget3.pack()


def FillPokeInteractions(parent,pokename):
        
        TextIconsWeakness = []
        TextIconsImunities = []
        TextIconsResistences = []
        ImunitiesMultipyers = []
        ArrayDosTipos = PokeJsonHandle().GetPokeType(PokeInfoRequests(pokename).DoRequest())

        if(len(ArrayDosTipos)>1):
             Weakness = TypeInteractions.StrenghtAndWeakness(ArrayDosTipos[0],ArrayDosTipos[1])[0]  
             Resistences = TypeInteractions.StrenghtAndWeakness(ArrayDosTipos[0],ArrayDosTipos[1])[2]
             Imunities = TypeInteractions.StrenghtAndWeakness(ArrayDosTipos[0],ArrayDosTipos[1])[1]
        else:
            Weakness = TypeInteractions.StrenghtAndWeakness(ArrayDosTipos[0],None)[0]
            Resistences = TypeInteractions.StrenghtAndWeakness(ArrayDosTipos[0],None)[2]
            Imunities = TypeInteractions.StrenghtAndWeakness(ArrayDosTipos[0],None)[1]

         
        if(len(Resistences)==0):
            Resistences = ["none 0.5x"]
        
        if(len(Imunities)==0):
            Imunities = ["none 0x"]
        
        for tipo in Weakness:
            if getattr(sys, 'frozen', False):
                # Estamos rodando a partir de um executável
                caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
            else:
                # Estamos rodando no ambiente de desenvolvimento
                caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
              
            TextIconsWeakness.append((caminho_icone, ""))

        for tipo in Imunities:
            if getattr(sys, 'frozen', False):
                # Estamos rodando a partir de um executável
                caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
                ImunitiesMultipyers.append("0X")
            else:
                # Estamos rodando no ambiente de desenvolvimento
                caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
                ImunitiesMultipyers.append("0X")
            TextIconsImunities.append((caminho_icone, ""))
        
        for tipo in Resistences:
            if getattr(sys, 'frozen', False):
                # Estamos rodando a partir de um executável
                caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
            else:
                # Estamos rodando no ambiente de desenvolvimento
                caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
            TextIconsResistences.append((caminho_icone, ""))


        damageMultiplierText = []






        for tipo in Weakness:
            if len(tipo.split(" ")) == 3:
               damageMultiplierText.append("4x")
            else:
                damageMultiplierText.append("2x")
        ResistencesMultiplierText = []
        for tipo in Resistences:
            if len(tipo.split(" ")) == 2:
               ResistencesMultiplierText.append(tipo.split(" ")[1])
            else:
                ResistencesMultiplierText.append("2x")
        
        tipo_widget = PokemonTypeWidget(parent,TextIconsWeakness,damageMultiplierText)

        tipo_widget2 = PokemonTypeWidget(parent,TextIconsResistences,ResistencesMultiplierText)

        tipo_widget3 = PokemonTypeWidget(parent,TextIconsImunities,ImunitiesMultipyers)

        divisoriaFraquezas = tk.Label(parent,fg="#00FFFF",bg="#2E2E2E" ,text="----- Fraquezas -----", font=("Arial", 10, "bold"))
        divisoriaImunidades= tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="----- Imunidades -----", font=("Arial", 10, "bold"))
        divisoriaResistencias = tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="----- Resistencias -----", font=("Arial", 10, "bold"))
        
        divisoriaFraquezas.pack()
        tipo_widget.pack()
        divisoriaResistencias.pack()

        tipo_widget2.pack()
        divisoriaImunidades.pack()
        tipo_widget3.pack()

class PokeView:
    def __init__(self, root,pokename,pokename2=None,SideBar=None):

        self.root = root
        self.sideBar = SideBar
        
        self.pokename1 = pokename
        self.pokename2 = pokename2
        
        self.SidebarInst = None
        pokemon_name = pokename     
        
        panel = GetPokeInfo(self.root,self).create_pokemon_panel(pokemon_name,func=self.ShowPokeStatsSingles)
        
        panel.pack()

    def ShowPokeStatsSingles(self,pokename=None):
        if pokename ==None:
            pokename = self.pokename1
        
        if(self.SidebarInst == None):
            
            self.SidebarInst = self.create_singles_bars(self.SearchPokeStats(pokename)[0])
            return
        state = self.SidebarInst.wm_state()
        
        if state == "withdrawn":
            self.SidebarInst.deiconify()
        elif state == "normal":
            self.SidebarInst.withdraw()
    def SearchPokeStats(self,name):
        Data = PokeInfoRequests(name).DoRequest()
  
        ArrayVals = []
        evs = {
            "HP": 252,  # Exemplo
            "Attack": 252,
            "Defense": 252,
            "Special Attack": 252,
            "Special Defense": 252,
            "Speed": 252
        }   
        level = 100

        if Data == None:
            return
        for Pokestats in Data['stats']:
            
            ArrayVals.append(Pokestats["base_stat"])
        
        def calculate_stats(base_stats, evs, level):
            IV = 31
            def calculate_hp(base, ev, level):
                return ((2 * base + IV + (ev // 4)) * level // 100) + level + 10
            
            # Função para calcular os outros stats
            def calculate_other_stat(base, ev, level):
                return ((2 * base + IV + (ev // 4)) * level // 100) + 5
            
            # Calcula os stats
            final_stats = {}
            for stat, base in base_stats.items():
                ev = evs.get(stat, 0)
                if stat == "HP":
                    final_stats[stat] = calculate_hp(base, ev, level)
                else:
                    final_stats[stat] = calculate_other_stat(base, ev, level)
            
            return final_stats
        def GenBaseStats(ev_array):
            stats = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"] 
            baseStats = {stat: ev for stat, ev in zip(stats, ev_array)}
            return baseStats
        BaseStats = GenBaseStats(ArrayVals)
        MaxStats = calculate_stats(BaseStats,evs,level)
        return BaseStats,MaxStats

    def create_singles_bars(self,val):
        parent = self.sideBar()
        values = [v for v in val.values() if isinstance(v, (int, float))]
           
        labels = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"] 
        # Verificar se o número de valores coincide com o número de rótulos
        if len(values) != len(labels):
            print("Erro: O número de valores deve ser igual ao número de rótulos.")
            return

        # Determinar largura máxima
        max_value = max(values)
        canvas_width = 200  # Largura máxima para as barras
        bar_height = 15     # Altura de cada barra
        spacing = 10        # Espaço entre as barras

        # Criar um canvas para as barras
        canvas_height = len(values) * (bar_height + spacing) + spacing
        canvas = tk.Canvas(parent, width=canvas_width + 200, height=canvas_height)
        canvas.config(bg="#2e2e2e")
        canvas.pack()

        for i, (value, label) in enumerate(zip(values, labels)):
            # Calcular comprimento proporcional
            bar_length = (value / max_value) * canvas_width
            x0 = 0  # Início colado na margem esquerda
            y0 = i * (bar_height + spacing) + spacing
            x1 = x0 + bar_length
            y1 = y0 + bar_height

            # Desenhar barra
            canvas.create_rectangle(x0, y0, x1, y1, fill="blue")

            # Adicionar o valor da barra (à direita da barra)
            canvas.create_text(x1 + 10, (y0 + y1) / 2,fill="white",text=str(value), font=("Arial", 10), anchor="w")

            # Adicionar o nome da barra (depois do valor)
            canvas.create_text(x1 + 50, (y0 + y1) / 2, text=label, font=("Arial", 10), anchor="w",fill="white")
        return parent
    def Fill(self):
        FillPokeInteractions(self.root,self.pokename1)

    def FillDuals(self,parent):
    

        for widget in parent.winfo_children():
            widget.destroy()  # deleting widget
        GetPokeInfo(self.root,self).CreateDualsGroup(self.pokename1,self.pokename2,parent)
    def atualizar_dados_Duals(self,pokename1,pokename2):
        for widget in self.root.winfo_children():
            widget.destroy()  # deleting widget

        self.Pokemon_image = GetPokeInfo(self.root,self) 
        panel = self.Pokemon_image.CreateDualsGroup(pokename1,pokename2,self.root)
        panel[0].pack()
        FillDualsInteractions(self.root,pokename1,pokename2)


    def atualizar_dados(self, pokename = "zacian-crowned"):
        
        for widget in self.root.winfo_children():
            widget.destroy()  # deleting widget

        self.Pokemon_image = GetPokeInfo(self.root,self)  # Instância única de GetPokeInfo
        panel = self.Pokemon_image.create_pokemon_panel(pokename,func=lambda:self.ShowPokeStatsSingles(pokename))
        panel.pack()
        FillPokeInteractions(self.root,pokename)




def SimpleTypeSelection(parent,Tipo1,Tipo2=None):

    if(Tipo1 == Tipo2):
        Tipo2 = None
    
    if(Tipo1 == "Nenhum"):
        Tipo1 = None
        
    if(Tipo2 == "Nenhum"):
        Tipo2 = None
    if((Tipo1 == None) and(Tipo2 != None)):
        Tipo1 = Tipo2
        Tipo2 = None
    
    if(Tipo2 == None and Tipo1 == None):
        return False
    TextIconsWeakness = []
    TextIconsImunities = []
    TextIconsResistences = []
    ImunitiesMultipyers = []
    
    
    if(Tipo2 != None and Tipo2 != None):
            Weakness = TypeInteractions.StrenghtAndWeakness(Tipo1,Tipo2)[0]  
            Resistences = TypeInteractions.StrenghtAndWeakness(Tipo1,Tipo2)[2]
            Imunities = TypeInteractions.StrenghtAndWeakness(Tipo1,Tipo2)[1]
    else:
        if(Tipo1 == None):
            Weakness = TypeInteractions.StrenghtAndWeakness(Tipo2,None)[0]
            Resistences = TypeInteractions.StrenghtAndWeakness(Tipo2,None)[2]
            Imunities = TypeInteractions.StrenghtAndWeakness(Tipo2,None)[1]
        elif(Tipo2 == None):
            Weakness = TypeInteractions.StrenghtAndWeakness(Tipo1,None)[0]
            Resistences = TypeInteractions.StrenghtAndWeakness(Tipo1,None)[2]
            Imunities = TypeInteractions.StrenghtAndWeakness(Tipo1,None)[1]

        
    if(len(Resistences)==0):
        Resistences = ["none 0.5x"]
    
    if(len(Imunities)==0):
        Imunities = ["none 0x"]
    
    for tipo in Weakness:
        if getattr(sys, 'frozen', False):
            # Estamos rodando a partir de um executável
            caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
        else:
            # Estamos rodando no ambiente de desenvolvimento
            caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
        TextIconsWeakness.append((caminho_icone, ""))

    for tipo in Imunities:
        if getattr(sys, 'frozen', False):
            # Estamos rodando a partir de um executável
            caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
            ImunitiesMultipyers.append("0X")
        else:
            # Estamos rodando no ambiente de desenvolvimento
            caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
            ImunitiesMultipyers.append("0X")
        TextIconsImunities.append((caminho_icone, ""))
    
    for tipo in Resistences:
        if getattr(sys, 'frozen', False):
            # Estamos rodando a partir de um executável
            caminho_icone = os.path.join(sys._MEIPASS, 'icons', f"{tipo.split(' ')[0]}.png")
        else:
            # Estamos rodando no ambiente de desenvolvimento
            caminho_icone = os.path.join('icons', f"{tipo.split(' ')[0]}.png")
        TextIconsResistences.append((caminho_icone, ""))
    damageMultiplierText = []
    for tipo in Weakness:
        if len(tipo.split(" ")) == 3:
            damageMultiplierText.append("4x")
        else:
            damageMultiplierText.append("2x")
    ResistencesMultiplierText = []
    for tipo in Resistences:
        if len(tipo.split(" ")) == 2:
            ResistencesMultiplierText.append(tipo.split(" ")[1])
        else:
            ResistencesMultiplierText.append("2x")
    tipo_widget = PokemonTypeWidget(parent,TextIconsWeakness,damageMultiplierText,40)
    tipo_widget2 = PokemonTypeWidget(parent,TextIconsResistences,ResistencesMultiplierText,40)
    tipo_widget3 = PokemonTypeWidget(parent,TextIconsImunities,ImunitiesMultipyers,40)
    divisoriaFraquezas = tk.Label(parent,fg="#00FFFF",bg="#2E2E2E" ,text="FRAQUEZAS", font=("Arial", 12, "bold"))
    divisoriaImunidades= tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="IMUNIDADES", font=("Arial", 12, "bold"))
    divisoriaResistencias = tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="RESISTÊNCIAS", font=("Arial", 12, "bold"))   
    divisoriaFraquezas.pack()
    tipo_widget.pack()
    divisoriaResistencias.pack()
    tipo_widget2.pack()
    divisoriaImunidades.pack()
    tipo_widget3.pack()

# ----------------------------------------------------------------------------------------------------------------------------------

class IconCombobox:
    def __init__(self, parent, values, icons, default_value):
        self.parent = parent
        self.values = values
        self.icons = icons

        # Frame para conter o dropdown
        self.frame = tk.Frame(self.parent)
        
        # Botão para exibir a seleção
        self.selected_value = tk.StringVar(value=default_value)
        self.dropdown_button = tk.Menubutton(
            self.frame, textvariable=self.selected_value, relief="raised", width=15
        )
        self.dropdown_button.pack(fill="x")

        # Menu que mostra os valores com ícones
        self.menu = tk.Menu(self.dropdown_button, tearoff=0)
        self.dropdown_button["menu"] = self.menu

        # Lista para armazenar as referências das imagens
        self.images = []

        for value, icon_path in zip(self.values, self.icons):
            image = Image.open(icon_path).resize((30, 30))
            icon = ImageTk.PhotoImage(image)
            self.images.append(icon)  # Armazena as imagens para evitar o garbage collector
            self.menu.add_command(
                label=value, image=icon, compound="left", command=lambda v=value: self.set_value(v)
            )
    def get_Value(self):
        return self.selected_value.get()
    def set_value(self, value):
        self.selected_value.set(value)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

class SearchBox(tk.Frame):
    def __init__(self, root,RenomearAba=None,*args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        
        self.lista_pokemon = ["Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash","Nidoran♀","Nidorina","Nidoqueen","Nidoran♂","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetch'd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr-Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew","Chikorita","Bayleef","Meganium","Cyndaquil","Quilava","Typhlosion","Totodile","Croconaw","Feraligatr","Sentret","Furret","Hoothoot","Noctowl","Ledyba","Ledian","Spinarak","Ariados","Crobat","Chinchou","Lanturn","Pichu","Cleffa","Igglybuff","Togepi","Togetic","Natu","Xatu","Mareep","Flaaffy","Ampharos","Bellossom","Marill","Azumarill","Sudowoodo","Politoed","Hoppip","Skiploom","Jumpluff","Aipom","Sunkern","Sunflora","Yanma","Wooper","Quagsire","Espeon","Umbreon","Murkrow","Slowking","Misdreavus","Unown","Wobbuffet","Girafarig","Pineco","Forretress","Dunsparce","Gligar","Steelix","Snubbull","Granbull","Qwilfish","Scizor","Shuckle","Heracross","Sneasel","Teddiursa","Ursaring","Slugma","Magcargo","Swinub","Piloswine","Corsola","Remoraid","Octillery","Delibird","Mantine","Skarmory","Houndour","Houndoom","Kingdra","Phanpy","Donphan","Porygon2","Stantler","Smeargle","Tyrogue","Hitmontop","Smoochum","Elekid","Magby","Miltank","Blissey","Raikou","Entei","Suicune","Larvitar","Pupitar","Tyranitar","Lugia","Ho-Oh","Celebi","Treecko","Grovyle","Sceptile","Torchic","Combusken","Blaziken","Mudkip","Marshtomp","Swampert","Poochyena","Mightyena","Zigzagoon","Linoone","Wurmple","Silcoon","Beautifly","Cascoon","Dustox","Lotad","Lombre","Ludicolo","Seedot","Nuzleaf","Shiftry","Taillow","Swellow","Wingull","Pelipper","Ralts","Kirlia","Gardevoir","Surskit","Masquerain","Shroomish","Breloom","Slakoth","Vigoroth","Slaking","Nincada","Ninjask","Shedinja","Whismur","Loudred","Exploud","Makuhita","Hariyama","Azurill","Nosepass","Skitty","Delcatty","Sableye","Mawile","Aron","Lairon","Aggron","Meditite","Medicham","Electrike","Manectric","Plusle","Minun","Volbeat","Illumise","Roselia","Gulpin","Swalot","Carvanha","Sharpedo","Wailmer","Wailord","Numel","Camerupt","Torkoal","Spoink","Grumpig","Spinda","Trapinch","Vibrava","Flygon","Cacnea","Cacturne","Swablu","Altaria","Zangoose","Seviper","Lunatone","Solrock","Barboach","Whiscash","Corphish","Crawdaunt","Baltoy","Claydol","Lileep","Cradily","Anorith","Armaldo","Feebas","Milotic","Castform","Kecleon","Shuppet","Banette","Duskull","Dusclops","Tropius","Chimecho","Absol","Wynaut","Snorunt","Glalie","Spheal","Sealeo","Walrein","Clamperl","Huntail","Gorebyss","Relicanth","Luvdisc","Bagon","Shelgon","Salamence","Beldum","Metang","Metagross","Regirock","Regice","Registeel","Latias","Latios","Kyogre","Groudon","Rayquaza","Jirachi","Deoxys","Turtwig","Grotle","Torterra","Chimchar","Monferno","Infernape","Piplup","Prinplup","Empoleon","Starly","Staravia","Staraptor","Bidoof","Bibarel","Kricketot","Kricketune","Shinx","Luxio","Luxray","Budew","Roserade","Cranidos","Rampardos","Shieldon","Bastiodon","Burmy","Wormadam","Mothim","Combee","Vespiquen","Pachirisu","Buizel","Floatzel","Cherubi","Cherrim","Shellos","Gastrodon","Ambipom","Drifloon","Drifblim","Buneary","Lopunny","Mismagius","Honchkrow","Glameow","Purugly","Chingling","Stunky","Skuntank","Bronzor","Bronzong","Bonsly","Mime-Jr","Happiny","Chatot","Spiritomb","Gible","Gabite","Garchomp","Munchlax","Riolu","Lucario","Hippopotas","Hippowdon","Skorupi","Drapion","Croagunk","Toxicroak","Carnivine","Finneon","Lumineon","Mantyke","Snover","Abomasnow","Weavile","Magnezone","Lickilicky","Rhyperior","Tangrowth","Electivire","Magmortar","Togekiss","Yanmega","Leafeon","Glaceon","Gliscor","Mamoswine","Porygon-Z","Gallade","Probopass","Dusknoir","Froslass","Rotom","Uxie","Mesprit","Azelf","Dialga","Palkia","Heatran","Regigigas","Giratina","Cresselia","Phione","Manaphy","Darkrai","Shaymin","Arceus","Victini","Snivy","Servine","Serperior","Tepig","Pignite","Emboar","Oshawott","Dewott","Samurott","Patrat","Watchog","Lillipup","Herdier","Stoutland","Purrloin","Liepard","Pansage","Simisage","Pansear","Simisear","Panpour","Simipour","Munna","Musharna","Pidove","Tranquill","Unfezant","Blitzle","Zebstrika","Roggenrola","Boldore","Gigalith","Woobat","Swoobat","Drilbur","Excadrill","Audino","Timburr","Gurdurr","Conkeldurr","Tympole","Palpitoad","Seismitoad","Throh","Sawk","Sewaddle","Swadloon","Leavanny","Venipede","Whirlipede","Scolipede","Cottonee","Whimsicott","Petilil","Lilligant","Basculin","Sandile","Krokorok","Krookodile","Darumaka","Darmanitan","Maractus","Dwebble","Crustle","Scraggy","Scrafty","Sigilyph","Yamask","Cofagrigus","Tirtouga","Carracosta","Archen","Archeops","Trubbish","Garbodor","Zorua","Zoroark","Minccino","Cinccino","Gothita","Gothorita","Gothitelle","Solosis","Duosion","Reuniclus","Ducklett","Swanna","Vanillite","Vanillish","Vanilluxe","Deerling","Sawsbuck","Emolga","Karrablast","Escavalier","Foongus","Amoonguss","Frillish","Jellicent","Alomomola","Joltik","Galvantula","Ferroseed","Ferrothorn","Klink","Klang","Klinklang","Tynamo","Eelektrik","Eelektross","Elgyem","Beheeyem","Litwick","Lampent","Chandelure","Axew","Fraxure","Haxorus","Cubchoo","Beartic","Cryogonal","Shelmet","Accelgor","Stunfisk","Mienfoo","Mienshao","Druddigon","Golett","Golurk","Pawniard","Bisharp","Bouffalant","Rufflet","Braviary","Vullaby","Mandibuzz","Heatmor","Durant","Deino","Zweilous","Hydreigon","Larvesta","Volcarona","Cobalion","Terrakion","Virizion","Tornadus","Thundurus","Reshiram","Zekrom","Landorus","Kyurem","Keldeo","Meloetta","Genesect","Chespin","Quilladin","Chesnaught","Fennekin","Braixen","Delphox","Froakie","Frogadier","Greninja","Bunnelby","Diggersby","Fletchling","Fletchinder","Talonflame","Scatterbug","Spewpa","Vivillon","Litleo","Pyroar","Flabébé","Floette","Florges","Skiddo","Gogoat","Pancham","Pangoro","Furfrou","Espurr","Meowstic","Honedge","Doublade","Aegislash","Spritzee","Aromatisse","Swirlix","Slurpuff","Inkay","Malamar","Binacle","Barbaracle","Skrelp","Dragalge","Clauncher","Clawitzer","Helioptile","Heliolisk","Tyrunt","Tyrantrum","Amaura","Aurorus","Sylveon","Hawlucha","Dedenne","Carbink","Goomy","Sliggoo","Goodra","Klefki","Phantump","Trevenant","Pumpkaboo","Gourgeist","Bergmite","Avalugg","Noibat","Noivern","Xerneas","Yveltal","Zygarde","Diancie","Hoopa","Volcanion","Rowlet","Dartrix","Decidueye","Litten","Torracat","Incineroar","Popplio","Brionne","Primarina","Pikipek","Trumbeak","Toucannon","Yungoos","Gumshoos","Grubbin","Charjabug","Vikavolt","Crabrawler","Crabominable","Oricorio","Cutiefly","Ribombee","Rockruff","Lycanroc","Wishiwashi","Mareanie","Toxapex","Mudbray","Mudsdale","Dewpider","Araquanid","Fomantis","Lurantis","Morelull","Shiinotic","Salandit","Salazzle","Stufful","Bewear","Bounsweet","Steenee","Tsareena","Comfey","Oranguru","Passimian","Wimpod","Golisopod","Sandygast","Palossand","Pyukumuku","Type:-Null","Silvally","Minior","Komala","Turtonator","Togedemaru","Mimikyu","Bruxish","Drampa","Dhelmise","Jangmo-o","Hakamo-o","Kommo-o","Tapu-Koko","Tapu-Lele","Tapu-Bulu","Tapu-Fini","Cosmog","Cosmoem","Solgaleo","Lunala","Nihilego","Buzzwole","Pheromosa","Xurkitree","Celesteela","Kartana","Guzzlord","Necrozma","Magearna","Marshadow","Poipole","Naganadel","Stakataka","Blacephalon","Zeraora","Meltan","Melmetal","Grookey","Thwackey","Rillaboom","Scorbunny","Raboot","Cinderace","Sobble","Drizzile","Inteleon","Skwovet","Greedent","Rookidee","Corvisquire","Corviknight","Blipbug","Dottler","Orbeetle","Nickit","Thievul","Gossifleur","Eldegoss","Wooloo","Dubwool","Chewtle","Drednaw","Yamper","Boltund","Rolycoly","Carkol","Coalossal","Applin","Flapple","Appletun","Silicobra","Sandaconda","Cramorant","Arrokuda","Barraskewda","Toxel","Toxtricity","Sizzlipede","Centiskorch","Clobbopus","Grapploct","Sinistea","Polteageist","Hatenna","Hattrem","Hatterene","Impidimp","Morgrem","Grimmsnarl","Obstagoon","Perrserker","Cursola","Sirfetch'd","Mr-Rime","Runerigus","Milcery","Alcremie","Falinks","Pincurchin","Snom","Frosmoth","Stonjourner","Eiscue","Indeedee","Morpeko","Cufant","Copperajah","Dracozolt","Arctozolt","Dracovish","Arctovish","Duraludon","Dreepy","Drakloak","Dragapult","Zacian","Zamazenta","Eternatus","Kubfu","Urshifu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Wyrdeer","Kleavor","Ursaluna","Basculegion","Sneasler","Overqwil","Enamorus","Sprigatito","Floragato","Meowscarada","Fuecoco","Crocalor","Skeledirge","Quaxly","Quaxwell","Quaquaval","Lechonk","Oinkologne","Tarountula","Spidops","Nymble","Lokix","Pawmi","Pawmo","Pawmot","Tandemaus","Maushold","Fidough","Dachsbun","Smoliv","Dolliv","Arboliva","Squawkabilly","Nacli","Naclstack","Garganacl","Charcadet","Armarouge","Ceruledge","Tadbulb","Bellibolt","Wattrel","Kilowattrel","Maschiff","Mabosstiff","Shroodle","Grafaiai","Bramblin","Brambleghast","Toedscool","Toedscruel","Klawf","Capsakid","Scovillain","Rellor","Rabsca","Flittle","Espathra","Tinkatink","Tinkatuff","Tinkaton","Wiglett","Wugtrio","Bombirdier","Finizen","Palafin","Varoom","Revavroom","Cyclizar","Orthworm","Glimmet","Glimmora","Greavard","Houndstone","Flamigo","Cetoddle","Cetitan","Veluza","Dondozo","Tatsugiri","Annihilape","Clodsire","Farigiraf","Dudunsparce","Kingambit","Great-Tusk","Scream-Tail","Brute-Bonnet","Flutter-Mane","Slither-Wing","Sandy-Shocks","Iron-Treads","Iron-Bundle","Iron-Hands","Iron-Jugulis","Iron-Moth","Iron-Thorns","Frigibax","Arctibax","Baxcalibur","Gimmighoul","Gholdengo","Wo-Chien","Chien-Pao","Ting-Lu","Chi-Yu","Roaring-Moon","Iron-Valiant","Koraidon","Miraidon","Walking-Wake","Iron-Leaves","Dipplin","Poltchageist","Sinistcha","Okidogi","Munkidori","Fezandipiti","Ogerpon","Archaludon","Hydrapple","Gouging-Fire","Raging-Bolt","Iron-Boulder","Iron-Crown","Terapagos","Pecharunt"]
        self.BarraDeComandos = BarraDeComandos
    def SearchDuals(self,DefaultValue1="",DefaultValue2="",Zerado=False):
           
        self.entrada_pokemon = StringVar()
        self.SearchAndComplete = tk.Frame(self.root, relief="sunken", borderwidth=1)
        self.lista_sugestoes = Listbox(self.SearchAndComplete, bg="#444444",fg="#fff",font=("Arial", 12), width=30, height=10, bd=2,selectmode=tk.SINGLE)
        self.EntryLabel = Label(self.SearchAndComplete,text="Pesquisa por nome")
        self.entry_pokemon = tk.Entry(self.SearchAndComplete,bg="#444444",insertbackground="red",fg="#fff" ,textvariable=self.entrada_pokemon, font=("Arial", 12), width=30, bd=2)
        self.entrada_pokemon.trace_add("write", lambda x,y,z:self.atualizar_lista(self.entrada_pokemon,self.entrada_pokemon,self.lista_sugestoes))

        self.entrada_pokemon2 = StringVar()
        if(Zerado == False):
            self.entrada_pokemon.set(DefaultValue1)
            self.entrada_pokemon2.set(DefaultValue2)
        
        self.SearchAndComplete2 = tk.Frame(self.root, relief="sunken", borderwidth=1)
        self.lista_sugestoes2 = Listbox(self.SearchAndComplete2, bg="#444444",fg="#fff",font=("Arial", 12), width=30, height=10, bd=2,selectmode=tk.SINGLE)
        self.EntryLabel2 = Label(self.SearchAndComplete2,text="Pesquisa por nome")
        self.entrada_pokemon2.trace_add("write", lambda x,y,z:self.atualizar_lista(self.entrada_pokemon2,self.entrada_pokemon2,self.lista_sugestoes2))
        self.entry_pokemon2 = tk.Entry(self.SearchAndComplete2,bg="#444444",insertbackground="red",fg="#fff" ,textvariable=self.entrada_pokemon2, font=("Arial", 12), width=30, bd=2)
        self.entry_pokemon.pack(fill="x")  # Posiciona a Entry na janela
        self.entry_pokemon.pack(fill="x")  # Posiciona a Entry na janela
        self.entry_pokemon.focus()
        self.lista_sugestoes.pack(fill="x")
        self.SearchAndComplete.pack(fill="x")
                
        
        self.entry_pokemon2.pack(fill="x")  # Posiciona a Entry na janela
        self.entry_pokemon2.pack(fill="x")  # Posiciona a Entry na janela
        self.entry_pokemon2.focus()
        self.lista_sugestoes2.pack(fill="x")
        self.SearchAndComplete2.pack(fill="x")
        
        
        self.lista_sugestoes.bind("<<ListboxSelect>>", lambda x: self.DualsSelectItem(self.lista_sugestoes,self.SearchAndComplete,self.entrada_pokemon))
        self.lista_sugestoes2.bind("<<ListboxSelect>>", lambda x: self.DualsSelectItem(self.lista_sugestoes2,self.SearchAndComplete2,self.entrada_pokemon2))
        

        self.DualsSearch_BTN = tk.Button(self.root,text="SEARCH",command=lambda:PokeView(self.root,self.entry_pokemon.get().lower(),self.entry_pokemon2.get().lower()).FillDuals(self.root))
        self.DualsSearch_BTN.pack()
    def DualsSelectItem(self,Lista,Panel_SearchAndComplete,Entrada):
        if not hasattr(self, "_handling_event") or not self._handling_event:
            self._handling_event = True  # Indica que estamos lidando com o evento

            selected_index = Lista.curselection()
            if selected_index:
                selected_item = Lista.get(selected_index[0])
                Entrada.set(selected_item)
                #Panel_SearchAndComplete.pack_forget()

            else:
                print("Erro: Nenhum item selecionado")
            
            # Reativar o evento após uma pequena pausa
            self.root.after(100, lambda: setattr(self, "_handling_event", False))

    def SearchByTypes(self):
        self.values2 = self.values1 =  ['Nenhum','Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy']
        self.ValTESTE=  ['Nenhum','Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy']
        self.IconsPath = []
        
        for i in self.ValTESTE:
            if getattr(sys, 'frozen', False):
                self.IcoLoc = os.path.join(sys._MEIPASS, 'icons_cortados', f"{i}.png")
    
            else:
                self.IcoLoc = "icons_cortados/"+i+".png"
            self.IconsPath.append(self.IcoLoc)

        self.DropdownFrame = tk.Frame(self.root, relief="sunken", borderwidth=1)
        self.DropdownFrame.config(bg="#444444")

        self.TiposDoPokemon = Label(self.root,text="Selecione os tipos do pokemon")
        self.TiposDoPokemon.pack(fill="x")
        self.TiposDoPokemon.config(bg="#2E2E2E",fg="#fff",font=15)
        self.PokemonCombobox1 = IconCombobox(self.root, values=self.ValTESTE, icons=self.IconsPath, default_value="Nenhum")
        self.PokemonCombobox1.pack(fill="x",pady=(10, 0),padx=10)
        
        self.PokemonCombobox2 = IconCombobox(self.root, values=self.ValTESTE, icons=self.IconsPath, default_value="Nenhum")
        self.PokemonCombobox2.pack(fill="x",pady=(10, 0),padx=10)

        update_button = tk.Button(self.DropdownFrame, text="Pesquisar", command=self.UpdateTypeSelection)
        update_button.pack(fill="x")

        self.panel_frame = tk.Frame(self.root, relief="sunken", borderwidth=7)
        self.panel_frame.config(bg="#2E2E2E")
        self.DropdownFrame.pack(fill="x",pady=(10, 0),padx=10)
        self.panel_frame.pack(fill="x")

    def SearchPokeStats(self,name):
        Data = PokeInfoRequests(name).DoRequest()
  
        ArrayVals = []
        evs = {
            "HP": 252,  # Exemplo
            "Attack": 252,
            "Defense": 252,
            "Special Attack": 252,
            "Special Defense": 252,
            "Speed": 252
        }   
        level = 100

        if Data == None:
            return
        for Pokestats in Data['stats']:
            
            ArrayVals.append(Pokestats["base_stat"])
        
        def calculate_stats(base_stats, evs, level):
            IV = 31
            def calculate_hp(base, ev, level):
                return ((2 * base + IV + (ev // 4)) * level // 100) + level + 10
            
            # Função para calcular os outros stats
            def calculate_other_stat(base, ev, level):
                return ((2 * base + IV + (ev // 4)) * level // 100) + 5
            
            # Calcula os stats
            final_stats = {}
            for stat, base in base_stats.items():
                ev = evs.get(stat, 0)
                if stat == "HP":
                    final_stats[stat] = calculate_hp(base, ev, level)
                else:
                    final_stats[stat] = calculate_other_stat(base, ev, level)
            
            return final_stats
        def GenBaseStats(ev_array):
            stats = ["HP", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"] 
            baseStats = {stat: ev for stat, ev in zip(stats, ev_array)}
            return baseStats
        BaseStats = GenBaseStats(ArrayVals)
        MaxStats = calculate_stats(BaseStats,evs,level)
        return BaseStats,MaxStats

    def SearchByPokeName(self,rootlistener,Janela_btn,SideBar=None):
       
        self.sidebar = SideBar
    
        self.inst_pokename = None
        self.entrada_pokemon = StringVar()
        self.SearchAndComplete = tk.Frame(self.root, relief="sunken", borderwidth=1)
        self.entrada_pokemon.trace_add("write", lambda x,y,z: self.atualizar_lista(self.entrada_pokemon,self.entrada_pokemon,self.lista_sugestoes))
        self.lista_sugestoes = Listbox(self.SearchAndComplete, bg="#444444",fg="#fff",font=("Arial", 12), width=30, height=10, bd=2,selectmode=tk.SINGLE)
        self.EntryLabel = Label(self.SearchAndComplete,text="Pesquisa por nome")
        self.entry_pokemon = tk.Entry(self.SearchAndComplete,bg="#444444",insertbackground="red",fg="#fff" ,textvariable=self.entrada_pokemon, font=("Arial", 12), width=30, bd=2)
        self.entry_pokemon.pack(fill="x")  # Posiciona a Entry na janela
        self.entry_pokemon.pack(fill="x")  # Posiciona a Entry na janela
        self.entry_pokemon.focus()
        self.lista_sugestoes.pack(fill="x")
        self.SearchAndComplete.pack(fill="x")
        self.lista_sugestoes.bind("<<ListboxSelect>>", lambda x: self.select_mouse_item(Janela_btn,SideBar=SideBar))
        rootlistener.bind("<Return>", lambda x: self.selecionar_item(Janela_btn,SideBar=SideBar))
        
    def UpdateTypeSelection(self):
        # Remove labels antigos
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

        # Obter valores selecionados nas lis
        option1 = self.PokemonCombobox1.get_Value()
        option2 = self.PokemonCombobox2.get_Value()
        SimpleTypeSelection(self.panel_frame,option1,option2)


    def atualizar_lista(self,entrada_pokemon, entradapokemon,listaSugestoes,*args):
        valor_digitado = entrada_pokemon.get()
        
        if valor_digitado == '':
            listaSugestoes.place_forget()
            listaSugestoes.delete(0, END)
        else:
            listaSugestoes.delete(0, END)
         

            for item in self.lista_pokemon:
                if re.search(valor_digitado, item, re.IGNORECASE):
                    listaSugestoes.insert(END, item)
    def CreateLoadingWindow():
        # Cria a janela principal
        LoadingWindow = tk.Tk()
        LoadingWindow.title("LOADING")
        LoadingWindow.geometry("400x400")
        LoadingWindow.overrideredirect(True)
        # Torna a janela totalmente transparente
    
        LoadingWindow.config(bg="#2e2e2e")  # Define o fundo da janela como branco
        # Cria um label para ver o conteúdo na janela
        label = tk.Label(LoadingWindow, text="CARREGANDO", font=("Arial", 20), fg="white", bg="#2e2e2e")
        label.pack(expand=True)

        # Mantém a janela aberta
        LoadingWindow.mainloop()
    def start_asyncio_loop(self):
        global RootMain
        # Cria um novo loop de eventos se não houver um ativo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)  # Define o novo loop como o loop atual
        loop.create_task(self.abrir_instancia())  # Cria a tarefa assíncrona
        RootMain.after(100, self.check_asyncio_loop)

    def check_asyncio_loop(self):
        global RootMain
        loop = asyncio.get_event_loop()  # Obtém o loop de eventos atual
        if loop.is_running():
            RootMain.after(100, self.check_asyncio_loop)
        else:
            print("Asyncio loop terminado!")

    def select_mouse_item(self, Janela_btn,SideBar):

        if not hasattr(self, "_handling_event") or not self._handling_event:
            self._handling_event = True  # Indica que estamos lidando com o evento

            selected_index = self.lista_sugestoes.curselection()
            if selected_index:
                selected_item = self.lista_sugestoes.get(selected_index[0])
                self.entrada_pokemon.set(selected_item)
                self.SearchAndComplete.pack_forget()

                # Chamando a nova instância apenas uma vez
                Janela_btn.config(text=selected_item.lower())
                
                self.abrir_nova_instancia(selected_item.lower(),sideBar=SideBar)
         
                
            else:
                print("Erro: Nenhum item selecionado")
            
            # Reativar o evento após uma pequena pausa
            

    def selecionar_item(self, Janela_btn,SideBar):

        if self.lista_sugestoes.winfo_ismapped() and self.lista_sugestoes.size() > 0:
            if not hasattr(self, "_handling_event") or not self._handling_event:
                self._handling_event = True  # Indica que estamos lidando com o evento
                
                selected_item = self.lista_sugestoes.get(0)
                self.entrada_pokemon.set(selected_item)
                self.SearchAndComplete.pack_forget()

                    # Chamando a nova instância apenas uma vez
                Janela_btn.config(text=selected_item.lower())
                self.abrir_nova_instancia(selected_item.lower(),sideBar=SideBar)
            else:
                print("Erro: Nenhum item selecionado")
                
                # Reativar o evento após uma pequena pausa
                self.root.after(100, lambda: setattr(self, "_handling_event", False))







    def carregar_dados_pokemon(self, nome_pokemon):
        self.RenomearAba("Pokemon 1",nome_pokemon)
        for widget in self.root.winfo_children():
            widget.destroy()
            


    def abrir_instancia(self,sidebar):
        
        app = PokeView(self.root,self.inst_pokename,SideBar=sidebar)
        app.Fill()
    def abrir_nova_instancia(self,nome_pokemon,sideBar):
       
        self.sidebar = sideBar
        self.inst_pokename = nome_pokemon
        RootMain.after(100, lambda: self.abrir_instancia(sideBar)) 


aba_lateral = None





def main():

    global RootMain
    root = tk.Tk()



    
    root.title("Poke Search")
    root.config(bg="#2E2E2E")
    root.call('wm', 'attributes', '.', '-topmost', True)

    RootMain  = root
    root.geometry('560x600')  # Largura x Altura
    BarraDeComandos_instancia =  BarraDeComandos(root)
    BarraDeComandos_instancia.criar_tipo_de_aba("Pokemon")
    # Chamar a função para posicionar a janela
    center_window(root)
   # app = SearchBox(root)
    # Exibir a janela
    root.overrideredirect(True)
    
    root.mainloop()



if __name__ == "__main__":
    main()
    