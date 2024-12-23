import tkinter as tk
from tkinter import PhotoImage, StringVar, Entry, Listbox, Frame, Label, SINGLE, END, ACTIVE,ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import re
import sys
import os
from MODULES import TypeInteractions



class CreatePokemonAbilitiesWidget(tk.Frame):
    def __init__(self, parent, abilities_names,abilities_descriptions, *args, **kwargs):
     
        super().__init__(parent, *args, **kwargs)
        
        
        
        listbox = tk.Listbox(parent, height=len(abilities_names), bg="#2E2E2E", fg="white", selectmode=SINGLE)
        for i in abilities_names:
            listbox.insert(tk.END, i)
            listbox.pack(fill="both", expand=True)



class GetPokeInfo(tk.Frame):

    
    def __init__(self, parent,poke_view_instance):
        super().__init__(parent)
        self.parent = parent
        self.FramePokeinfo = Frame(parent, bg="#2E2E2E")
        self.img_label = Label(self.FramePokeinfo, bg="#2E2E2E")
        self.AbilitiesList = tk.Listbox(parent)
        self.poke_view_instance = poke_view_instance  
        self.Pokename = ""
        self.img_label.grid()  # Configura o rótulo para a imagem
        self.FramePokeinfo.grid(row=0, column=1, rowspan=2, sticky="w",padx=10,pady=10)  # Organiza o frame no layout
        
   
    def GetPokeAbilities(self,Name):
        self.Pokename = Name
        Poke_Abilities = []
        response = PokeInfoRequests(Name).DoRequest()  
        

        for i in range(0,len(response['abilities'])):
            Poke_Abilities.append(response['abilities'][i]['ability']['name'])

        return Poke_Abilities


    def GetPokeImage(parent,nome):
      
        try:
      
            frame_imagens = Frame(parent, bg="#2E2E2E")
            for widget in frame_imagens.winfo_children():
                widget.destroy()
            data = PokeInfoRequests().DoRequest(nome)
            
            imagem_url = data['sprites']['front_default']
            img = Image.open(requests.get(imagem_url, stream=True).raw)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            img_label = Label(frame_imagens, image=img_tk, bg="#2E2E2E")
            img_label.image = img_tk  
            img_label.grid()
            frame_imagens.grid(padx=10, pady=10)  
            return frame_imagens
        except requests.exceptions.RequestException as e:

                
            print("Err")
    def CreatePokemonGrid(self):
        self.Pokemon_image = Frame(self.parent, bg="#2E2E2E")
        self.img_label = Label(self.Pokemon_image, bg="#2E2E2E")
        self.img_label.grid()

    
   

    def GetPokeAlternativeForms(self, Listbox):
        
        
        
        
        alternative_forms = PokeInfoRequests(self.Pokename).DoRequestPokeForms()
  
        for i in alternative_forms:
            
            Listbox.insert(END, i['pokemon']['name'])
       
        Listbox.delete(0)
       
        # Associa o evento <<ListboxSelect>> ao método de PokeView
        
        Listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def on_listbox_select(self, event):
        # Obtém o nome selecionado no Listbox
        selected_index = event.widget.curselection()
        if selected_index:
            selected_item = event.widget.get(selected_index[0])
            # Chama o método atualizar_dados em PokeView
            self.poke_view_instance.atualizar_dados(selected_item)
    def create_pokemon_panel(self, pokemon_name):
        panel = tk.Frame(self.parent, bg="#2E2E2E")

     
        frame_image = tk.Frame(panel, bg="#2E2E2E")
        frame_image.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        try:
 
            data = PokeInfoRequests(pokemon_name).DoRequest()
            image_url = data['sprites']['front_default']

            img = Image.open(requests.get(image_url, stream=True).raw)
            img = img.resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)

            label_image = tk.Label(frame_image, image=img_tk, bg="#2E2E2E")
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
        description_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        description_label = tk.Label(description_frame, text="", bg="#2E2E2E", fg="yellow", wraplength=90, justify="left")
       
        description_label.grid(row=0, column=0)


        # Atualizar descrição ao clicar no item
        def update_description(event):
            # Obtém o índice do item selecionado
            index = listbox.curselection()
            if index:
                description_label.config(text=abilities_descriptions[index[0]])

        listbox.bind("<<ListboxSelect>>", update_description)

        AlternativeForms.bind("<<ListboxSelect>>", self.on_listbox_select)
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
            response = requests.get(self.UrlPoke+self.pokename)
            response.raise_for_status()
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
        
        

        try:
   
            response = requests.get(self.SpeciesURL + str(Pokedexnumber))
    
            if response.status_code != 200:
                return f"Erro: Não foi possível encontrar o Pokémon '{Pokedexnumber}'."

            pokemon_data = response.json()


            return pokemon_data['varieties']

        except:
            return None


class PokeJsonHandle():
    def GetPokeType(self,json):
        tipos = [t['type']['name'] for t in json['types']]
        
        return tipos


class PokeView:
    def __init__(self, root,pokename,lastWindow):
        self.root = root
        self.lastWindow =lastWindow
        center_window(root)
        self.root.title("Poke View")
        self.Pokemon_image = GetPokeInfo(self.root,self)
        self.FillPokeInteractions(pokename)

        pokemon_name = pokename
        self.criar_barra_comandos()

        get_poke_info = GetPokeInfo(self.root,self)
        panel = get_poke_info.create_pokemon_panel(pokemon_name)

        panel.grid(row=1, column=1, padx=10, pady=10)

    def criar_barra_comandos(self):
        self.root.overrideredirect(True)
        barra_comandos = tk.Frame(self.root, bg="#444444", height=30)
        barra_comandos.grid(row=0, column=0, sticky="ew")
        barra_comandos.grid_columnconfigure(0, weight=1) 
        barra_comandos.grid_rowconfigure(0, weight=1)
        btn_fechar = tk.Button(barra_comandos, text="Fechar", command=self.onClose, bg="#444444", fg="#FF5722")
        btn_fechar.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Alinha à direita
        
    def atualizar_dados(self, pokename = "zacian-crowned"):

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.root.children["!frame"]:  # Preserva barra de comandos
                widget.destroy()
        self.criar_barra_comandos()
        self.FillPokeInteractions(pokename)
        self.Pokemon_image = GetPokeInfo(self.root,self)  # Instância única de GetPokeInfo
        panel = self.Pokemon_image.create_pokemon_panel(pokename)

        panel.grid(row=1, column=1, padx=10, pady=10)

          
    def mover_janela(self,event):
        self.root.geometry(f"+{event.x_root}+{event.y_root}")
    def onClose(self):
        self.lastWindow.deiconify()
        self.root.destroy() 



    def FillPokeInteractions(self,pokename):
        
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
        
        tipo_widget = PokemonTypeWidget(self.root,TextIconsWeakness,damageMultiplierText)

        tipo_widget2 = PokemonTypeWidget(self.root,TextIconsResistences,ResistencesMultiplierText)

        tipo_widget3 = PokemonTypeWidget(self.root,TextIconsImunities,ImunitiesMultipyers)

        divisoriaFraquezas = tk.Label(self.root,fg="#00FFFF",bg="#2E2E2E" ,text="----- Fraquezas -----", font=("Arial", 10, "bold"))
        divisoriaImunidades= tk.Label(self.root, fg="#00FFFF",bg="#2E2E2E",text="----- Imunidades -----", font=("Arial", 10, "bold"))
        divisoriaResistencias = tk.Label(self.root, fg="#00FFFF",bg="#2E2E2E",text="----- Resistencias -----", font=("Arial", 10, "bold"))
        
        divisoriaFraquezas.grid(row=3, column=1, pady=(10, 10),padx=(0,50))
        tipo_widget.grid(row=4, column=1, sticky="n",padx=(0,50))
        divisoriaResistencias.grid(row=5, column=1,padx=(0,50))

        tipo_widget2.grid(row=6, column=1, sticky="n",padx=(0,50))
        divisoriaImunidades.grid(row=7, column=1, pady=(10, 10),padx=(0,50))# Espaçamento acima e abaixo
        tipo_widget3.grid(row=8, column=1, sticky="n",padx=(0,50))
        





def SimpleTypeSelection(parent,Tipo1,Tipo2=None):

    if(Tipo1 == Tipo2):
        Tipo2 = None
    if(Tipo1 == "Nenhum"):
        Tipo1 = None
    if(Tipo2 == "Nenhum"):
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
    
    tipo_widget = PokemonTypeWidget(parent,TextIconsWeakness,damageMultiplierText,30)

    tipo_widget2 = PokemonTypeWidget(parent,TextIconsResistences,ResistencesMultiplierText,30)

    tipo_widget3 = PokemonTypeWidget(parent,TextIconsImunities,ImunitiesMultipyers,30)

    divisoriaFraquezas = tk.Label(parent,fg="#00FFFF",bg="#2E2E2E" ,text="----- Fraquezas -----", font=("Arial", 10, "bold"))
    divisoriaImunidades= tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="----- Imunidades -----", font=("Arial", 10, "bold"))
    divisoriaResistencias = tk.Label(parent, fg="#00FFFF",bg="#2E2E2E",text="----- Resistencias -----", font=("Arial", 10, "bold"))
    
    divisoriaFraquezas.grid(row=3, column=1)
    tipo_widget.grid(row=4, column=1, sticky="n")
    divisoriaResistencias.grid(row=5, column=1)

    tipo_widget2.grid(row=6, column=1, sticky="n")
    divisoriaImunidades.grid(row=7, column=1)# Espaçamento acima e abaixo
    tipo_widget3.grid(row=8, column=1, sticky="n")
    





class SearchBox(tk.Frame):
    def __init__(self, root,*args, **kwargs):
      
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.entrada_pokemon = StringVar()
        self.SearchAndComplete = tk.Frame(root, relief="sunken", borderwidth=1)
        self.entrada_pokemon.trace_add("write", self.atualizar_lista)
        self.values1 =  ['Nenhum','Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy']
        self.values2 =  ['Nenhum','Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy']
        self.lista_sugestoes = Listbox(self.SearchAndComplete, bg="#444444",fg="#fff",font=("Arial", 12), width=30, height=10, bd=2,selectmode=tk.SINGLE)
        self.entry_pokemon = tk.Entry(self.SearchAndComplete,bg="#444444",fg="#fff" ,textvariable=self.entrada_pokemon, font=("Arial", 12), width=30, bd=2)
        self.entry_pokemon.grid(row=0,column=0)  # Posiciona a Entry na janela
        self.lista_sugestoes.grid()
        self.SearchAndComplete.grid(row=0,column=0,padx=(5,5),pady=(5,5))
        self.lista_pokemon = ["Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash","Nidoran♀","Nidorina","Nidoqueen","Nidoran♂","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetch'd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr-Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew","Chikorita","Bayleef","Meganium","Cyndaquil","Quilava","Typhlosion","Totodile","Croconaw","Feraligatr","Sentret","Furret","Hoothoot","Noctowl","Ledyba","Ledian","Spinarak","Ariados","Crobat","Chinchou","Lanturn","Pichu","Cleffa","Igglybuff","Togepi","Togetic","Natu","Xatu","Mareep","Flaaffy","Ampharos","Bellossom","Marill","Azumarill","Sudowoodo","Politoed","Hoppip","Skiploom","Jumpluff","Aipom","Sunkern","Sunflora","Yanma","Wooper","Quagsire","Espeon","Umbreon","Murkrow","Slowking","Misdreavus","Unown","Wobbuffet","Girafarig","Pineco","Forretress","Dunsparce","Gligar","Steelix","Snubbull","Granbull","Qwilfish","Scizor","Shuckle","Heracross","Sneasel","Teddiursa","Ursaring","Slugma","Magcargo","Swinub","Piloswine","Corsola","Remoraid","Octillery","Delibird","Mantine","Skarmory","Houndour","Houndoom","Kingdra","Phanpy","Donphan","Porygon2","Stantler","Smeargle","Tyrogue","Hitmontop","Smoochum","Elekid","Magby","Miltank","Blissey","Raikou","Entei","Suicune","Larvitar","Pupitar","Tyranitar","Lugia","Ho-Oh","Celebi","Treecko","Grovyle","Sceptile","Torchic","Combusken","Blaziken","Mudkip","Marshtomp","Swampert","Poochyena","Mightyena","Zigzagoon","Linoone","Wurmple","Silcoon","Beautifly","Cascoon","Dustox","Lotad","Lombre","Ludicolo","Seedot","Nuzleaf","Shiftry","Taillow","Swellow","Wingull","Pelipper","Ralts","Kirlia","Gardevoir","Surskit","Masquerain","Shroomish","Breloom","Slakoth","Vigoroth","Slaking","Nincada","Ninjask","Shedinja","Whismur","Loudred","Exploud","Makuhita","Hariyama","Azurill","Nosepass","Skitty","Delcatty","Sableye","Mawile","Aron","Lairon","Aggron","Meditite","Medicham","Electrike","Manectric","Plusle","Minun","Volbeat","Illumise","Roselia","Gulpin","Swalot","Carvanha","Sharpedo","Wailmer","Wailord","Numel","Camerupt","Torkoal","Spoink","Grumpig","Spinda","Trapinch","Vibrava","Flygon","Cacnea","Cacturne","Swablu","Altaria","Zangoose","Seviper","Lunatone","Solrock","Barboach","Whiscash","Corphish","Crawdaunt","Baltoy","Claydol","Lileep","Cradily","Anorith","Armaldo","Feebas","Milotic","Castform","Kecleon","Shuppet","Banette","Duskull","Dusclops","Tropius","Chimecho","Absol","Wynaut","Snorunt","Glalie","Spheal","Sealeo","Walrein","Clamperl","Huntail","Gorebyss","Relicanth","Luvdisc","Bagon","Shelgon","Salamence","Beldum","Metang","Metagross","Regirock","Regice","Registeel","Latias","Latios","Kyogre","Groudon","Rayquaza","Jirachi","Deoxys","Turtwig","Grotle","Torterra","Chimchar","Monferno","Infernape","Piplup","Prinplup","Empoleon","Starly","Staravia","Staraptor","Bidoof","Bibarel","Kricketot","Kricketune","Shinx","Luxio","Luxray","Budew","Roserade","Cranidos","Rampardos","Shieldon","Bastiodon","Burmy","Wormadam","Mothim","Combee","Vespiquen","Pachirisu","Buizel","Floatzel","Cherubi","Cherrim","Shellos","Gastrodon","Ambipom","Drifloon","Drifblim","Buneary","Lopunny","Mismagius","Honchkrow","Glameow","Purugly","Chingling","Stunky","Skuntank","Bronzor","Bronzong","Bonsly","Mime-Jr","Happiny","Chatot","Spiritomb","Gible","Gabite","Garchomp","Munchlax","Riolu","Lucario","Hippopotas","Hippowdon","Skorupi","Drapion","Croagunk","Toxicroak","Carnivine","Finneon","Lumineon","Mantyke","Snover","Abomasnow","Weavile","Magnezone","Lickilicky","Rhyperior","Tangrowth","Electivire","Magmortar","Togekiss","Yanmega","Leafeon","Glaceon","Gliscor","Mamoswine","Porygon-Z","Gallade","Probopass","Dusknoir","Froslass","Rotom","Uxie","Mesprit","Azelf","Dialga","Palkia","Heatran","Regigigas","Giratina","Cresselia","Phione","Manaphy","Darkrai","Shaymin","Arceus","Victini","Snivy","Servine","Serperior","Tepig","Pignite","Emboar","Oshawott","Dewott","Samurott","Patrat","Watchog","Lillipup","Herdier","Stoutland","Purrloin","Liepard","Pansage","Simisage","Pansear","Simisear","Panpour","Simipour","Munna","Musharna","Pidove","Tranquill","Unfezant","Blitzle","Zebstrika","Roggenrola","Boldore","Gigalith","Woobat","Swoobat","Drilbur","Excadrill","Audino","Timburr","Gurdurr","Conkeldurr","Tympole","Palpitoad","Seismitoad","Throh","Sawk","Sewaddle","Swadloon","Leavanny","Venipede","Whirlipede","Scolipede","Cottonee","Whimsicott","Petilil","Lilligant","Basculin","Sandile","Krokorok","Krookodile","Darumaka","Darmanitan","Maractus","Dwebble","Crustle","Scraggy","Scrafty","Sigilyph","Yamask","Cofagrigus","Tirtouga","Carracosta","Archen","Archeops","Trubbish","Garbodor","Zorua","Zoroark","Minccino","Cinccino","Gothita","Gothorita","Gothitelle","Solosis","Duosion","Reuniclus","Ducklett","Swanna","Vanillite","Vanillish","Vanilluxe","Deerling","Sawsbuck","Emolga","Karrablast","Escavalier","Foongus","Amoonguss","Frillish","Jellicent","Alomomola","Joltik","Galvantula","Ferroseed","Ferrothorn","Klink","Klang","Klinklang","Tynamo","Eelektrik","Eelektross","Elgyem","Beheeyem","Litwick","Lampent","Chandelure","Axew","Fraxure","Haxorus","Cubchoo","Beartic","Cryogonal","Shelmet","Accelgor","Stunfisk","Mienfoo","Mienshao","Druddigon","Golett","Golurk","Pawniard","Bisharp","Bouffalant","Rufflet","Braviary","Vullaby","Mandibuzz","Heatmor","Durant","Deino","Zweilous","Hydreigon","Larvesta","Volcarona","Cobalion","Terrakion","Virizion","Tornadus","Thundurus","Reshiram","Zekrom","Landorus","Kyurem","Keldeo","Meloetta","Genesect","Chespin","Quilladin","Chesnaught","Fennekin","Braixen","Delphox","Froakie","Frogadier","Greninja","Bunnelby","Diggersby","Fletchling","Fletchinder","Talonflame","Scatterbug","Spewpa","Vivillon","Litleo","Pyroar","Flabébé","Floette","Florges","Skiddo","Gogoat","Pancham","Pangoro","Furfrou","Espurr","Meowstic","Honedge","Doublade","Aegislash","Spritzee","Aromatisse","Swirlix","Slurpuff","Inkay","Malamar","Binacle","Barbaracle","Skrelp","Dragalge","Clauncher","Clawitzer","Helioptile","Heliolisk","Tyrunt","Tyrantrum","Amaura","Aurorus","Sylveon","Hawlucha","Dedenne","Carbink","Goomy","Sliggoo","Goodra","Klefki","Phantump","Trevenant","Pumpkaboo","Gourgeist","Bergmite","Avalugg","Noibat","Noivern","Xerneas","Yveltal","Zygarde","Diancie","Hoopa","Volcanion","Rowlet","Dartrix","Decidueye","Litten","Torracat","Incineroar","Popplio","Brionne","Primarina","Pikipek","Trumbeak","Toucannon","Yungoos","Gumshoos","Grubbin","Charjabug","Vikavolt","Crabrawler","Crabominable","Oricorio","Cutiefly","Ribombee","Rockruff","Lycanroc","Wishiwashi","Mareanie","Toxapex","Mudbray","Mudsdale","Dewpider","Araquanid","Fomantis","Lurantis","Morelull","Shiinotic","Salandit","Salazzle","Stufful","Bewear","Bounsweet","Steenee","Tsareena","Comfey","Oranguru","Passimian","Wimpod","Golisopod","Sandygast","Palossand","Pyukumuku","Type:-Null","Silvally","Minior","Komala","Turtonator","Togedemaru","Mimikyu","Bruxish","Drampa","Dhelmise","Jangmo-o","Hakamo-o","Kommo-o","Tapu-Koko","Tapu-Lele","Tapu-Bulu","Tapu-Fini","Cosmog","Cosmoem","Solgaleo","Lunala","Nihilego","Buzzwole","Pheromosa","Xurkitree","Celesteela","Kartana","Guzzlord","Necrozma","Magearna","Marshadow","Poipole","Naganadel","Stakataka","Blacephalon","Zeraora","Meltan","Melmetal","Grookey","Thwackey","Rillaboom","Scorbunny","Raboot","Cinderace","Sobble","Drizzile","Inteleon","Skwovet","Greedent","Rookidee","Corvisquire","Corviknight","Blipbug","Dottler","Orbeetle","Nickit","Thievul","Gossifleur","Eldegoss","Wooloo","Dubwool","Chewtle","Drednaw","Yamper","Boltund","Rolycoly","Carkol","Coalossal","Applin","Flapple","Appletun","Silicobra","Sandaconda","Cramorant","Arrokuda","Barraskewda","Toxel","Toxtricity","Sizzlipede","Centiskorch","Clobbopus","Grapploct","Sinistea","Polteageist","Hatenna","Hattrem","Hatterene","Impidimp","Morgrem","Grimmsnarl","Obstagoon","Perrserker","Cursola","Sirfetch'd","Mr-Rime","Runerigus","Milcery","Alcremie","Falinks","Pincurchin","Snom","Frosmoth","Stonjourner","Eiscue","Indeedee","Morpeko","Cufant","Copperajah","Dracozolt","Arctozolt","Dracovish","Arctovish","Duraludon","Dreepy","Drakloak","Dragapult","Zacian","Zamazenta","Eternatus","Kubfu","Urshifu","Zarude","Regieleki","Regidrago","Glastrier","Spectrier","Calyrex","Wyrdeer","Kleavor","Ursaluna","Basculegion","Sneasler","Overqwil","Enamorus","Sprigatito","Floragato","Meowscarada","Fuecoco","Crocalor","Skeledirge","Quaxly","Quaxwell","Quaquaval","Lechonk","Oinkologne","Tarountula","Spidops","Nymble","Lokix","Pawmi","Pawmo","Pawmot","Tandemaus","Maushold","Fidough","Dachsbun","Smoliv","Dolliv","Arboliva","Squawkabilly","Nacli","Naclstack","Garganacl","Charcadet","Armarouge","Ceruledge","Tadbulb","Bellibolt","Wattrel","Kilowattrel","Maschiff","Mabosstiff","Shroodle","Grafaiai","Bramblin","Brambleghast","Toedscool","Toedscruel","Klawf","Capsakid","Scovillain","Rellor","Rabsca","Flittle","Espathra","Tinkatink","Tinkatuff","Tinkaton","Wiglett","Wugtrio","Bombirdier","Finizen","Palafin","Varoom","Revavroom","Cyclizar","Orthworm","Glimmet","Glimmora","Greavard","Houndstone","Flamigo","Cetoddle","Cetitan","Veluza","Dondozo","Tatsugiri","Annihilape","Clodsire","Farigiraf","Dudunsparce","Kingambit","Great-Tusk","Scream-Tail","Brute-Bonnet","Flutter-Mane","Slither-Wing","Sandy-Shocks","Iron-Treads","Iron-Bundle","Iron-Hands","Iron-Jugulis","Iron-Moth","Iron-Thorns","Frigibax","Arctibax","Baxcalibur","Gimmighoul","Gholdengo","Wo-Chien","Chien-Pao","Ting-Lu","Chi-Yu","Roaring-Moon","Iron-Valiant","Koraidon","Miraidon","Walking-Wake","Iron-Leaves","Dipplin","Poltchageist","Sinistcha","Okidogi","Munkidori","Fezandipiti","Ogerpon","Archaludon","Hydrapple","Gouging-Fire","Raging-Bolt","Iron-Boulder","Iron-Crown","Terapagos","Pecharunt"]



        self.DropdownFrame = tk.Frame(root, relief="sunken", borderwidth=1)
        self.DropdownFrame.config(bg="#444444")


        style = ttk.Style()
        style.theme_use("clam") 

        # Configuração do estilo do Combobox
        style.configure(
            "TCombobox",
            
            background="#2E2E2E",       # Cor de fundo do botão do Combobox

        )
    # Usar tema que permite customização
        self.dropdown1 = ttk.Combobox(self.DropdownFrame,values=self.values1, state="readonly", style="TCombobox")
        self.dropdown1.set("Nenhum")


        self.dropdown1.grid(row=0,column=1)

        self.dropdown2 = ttk.Combobox(self.DropdownFrame, values=self.values2, state="readonly", style="TCombobox")
        self.dropdown2.set("Nenhum")
        self.dropdown2.grid(row=1,column=1)


        # Botão para atualizar o painel
        update_button = tk.Button(self.DropdownFrame, text="Atualizar", command=self.UpdateTypeSelection)
        update_button.grid(row=2,column=1)


        # Painel para exibir labels
        self.panel_frame = tk.Frame(root, relief="sunken", borderwidth=7)
        self.panel_frame.grid(row=0,column=3)
        self.panel_frame.config(bg="#2E2E2E")

        self.DropdownFrame.grid(row=0,column=1,padx=(5,5),pady=(5,5))

        self.lista_sugestoes.bind("<<ListboxSelect>>", self.select_mouse_item)
        self.root.bind("<Return>", self.selecionar_item)

    def UpdateTypeSelection(self):
        # Remove labels antigos
        for widget in self.panel_frame.winfo_children():
            widget.destroy()

        # Obter valores selecionados nas lis
        option1 = self.dropdown1.get()
        option2 = self.dropdown2.get()
        SimpleTypeSelection(self.panel_frame,option1,option2)


    def atualizar_lista(self, *args):
        valor_digitado = self.entrada_pokemon.get()
        
        if valor_digitado == '':
            self.lista_sugestoes.place_forget()
            self.lista_sugestoes.delete(0, END)
        else:
            self.lista_sugestoes.delete(0, END)
         

            for item in self.lista_pokemon:
                if re.search(valor_digitado, item, re.IGNORECASE):
                    self.lista_sugestoes.insert(END, item)
                    

    def select_mouse_item(self,event):


                # Captura o índice do item selecionado
        selected_index = self.lista_sugestoes.curselection()
        
        if selected_index:
          
            selected_item = self.lista_sugestoes.get(selected_index[0])
            self.entrada_pokemon.set(selected_item)
            self.lista_sugestoes.place_forget()
            self.carregar_dados_pokemon(selected_item.lower())
        else:
            print("Err")

    def selecionar_item(self, event):
        if self.lista_sugestoes.winfo_ismapped() and self.lista_sugestoes.size() > 0:
            # Seleciona o primeiro item da lista
            item_selecionado = self.lista_sugestoes.get(0)
            self.entrada_pokemon.set(item_selecionado)
            self.lista_sugestoes.place_forget()
            self.carregar_dados_pokemon(item_selecionado.lower())

    def carregar_dados_pokemon(self, nome_pokemon):
        # Função fictícia para carregar dados do Pokémon, adapte conforme sua necessidade
        self.root.iconify()
        self.abrir_nova_instancia(nome_pokemon)
    def abrir_nova_instancia(self,nome_pokemon):
        # Cria uma nova janela para a nova instância de SearchBox

        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Nova Instância - SearchBox")
        nova_janela.geometry("600x600+1350+550")  # Largura 600, altura 400, posição X=300, Y=100
        nova_janela.config(bg="#2E2E2E")
        # Cria a nova instância de SearchBox na nova janela
        app = PokeView(nova_janela,nome_pokemon,self.root)

        center_window(nova_janela)
        
        # Fica no topo da nova janela
        nova_janela.wm_attributes('-topmost', 1)


class ConfigPanel(tk.Frame):
    def __init__(self, root, janela_para_configurar):
        self.root = root
        self.janela_para_configurar = janela_para_configurar  # A janela que será configurada

        # Variáveis de configuração para X e Y
        self.x_var = StringVar()
        self.y_var = StringVar()

        # Criando o painel de configuração
        self.frame = tk.Frame(root, bg="#2E2E2E", bd=2, relief="solid")
        self.frame.place(x=10, y=10)  # Posição inicial do painel

        # Rótulo e caixa de entrada para X
        self.label_x = tk.Label(self.frame, text="Posição X", fg="white", bg="#2E2E2E", font=("Arial", 12))
        self.label_x.grid(row=0, column=0, padx=5, pady=5)
        self.entry_x = tk.Entry(self.frame, textvariable=self.x_var, font=("Arial", 12), width=10)
        self.entry_x.grid(row=0, column=1, padx=5, pady=5)

        # Rótulo e caixa de entrada para Y
        self.label_y = tk.Label(self.frame, text="Posição Y", fg="white", bg="#2E2E2E", font=("Arial", 12))
        self.label_y.grid(row=1, column=0, padx=5, pady=5)
        self.entry_y = tk.Entry(self.frame, textvariable=self.y_var, font=("Arial", 12), width=10)
        self.entry_y.grid(row=1, column=1, padx=5, pady=5)

        # Botão para aplicar as alterações
        self.apply_button = tk.Button(self.frame, text="Aplicar", command=self.aplicar_configuracoes, font=("Arial", 12))
        self.apply_button.grid(row=2, columnspan=2, pady=10)

        # Atualizar automaticamente as coordenadas X e Y com a posição inicial do painel
        self.atualizar_coordenadas()


    def aplicar_configuracoes(self):
        # Obter as novas posições X e Y
        try:
            novo_x = int(self.x_var.get())
            novo_y = int(self.y_var.get())
            
            # Atualizar a posição da janela com as novas coordenadas
            nova_posicao = f"{novo_x}+{novo_y}"
            self.janela_para_configurar.geometry(f"1700x450+{novo_x}+{novo_y}")  # Ajuste o tamanho e a posição da janela
        except ValueError:
            print("Por favor, insira valores válidos para X e Y.")

    def atualizar_coordenadas(self):
        # Atualiza as variáveis X e Y com a posição atual do painel
        current_x = self.frame.winfo_x()
        current_y = self.frame.winfo_y()
        
        self.x_var.set(str(current_x))
        self.y_var.set(str(current_y))

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

def main():
    root = tk.Tk()
    root.title("Poke Search")
    root.config(bg="#2E2E2E")
    # Definir o tamanho da janela (ajuste conforme necessário)
    root.geometry('800x280')  # Largura x Altura

    # Chamar a função para posicionar a janela
    center_window(root)
    app = SearchBox(root)
    # Exibir a janela
    root.mainloop()

if __name__ == "__main__":
    main()
    
    
