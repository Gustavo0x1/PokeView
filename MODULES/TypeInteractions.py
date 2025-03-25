
from collections import Counter

#Relações : Tipo -> Causa x dano em Y ( Dragão -> Causa 0x de dano em Fata)
#Tipo interações -> Tipo -> Dano que o tipo causa em outro

def CapitalizeFirstLetter(A):
    if(A != None):
        Capitalized = ""
        Capitalized += A[0].upper()
        Capitalized += A[1:]
        return Capitalized
    return A
tipo_interacoes = {
    'Normal': {
        'Normal': 1, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 0.5,  
        'Ghost': 0,  
        'Dragon': 1,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 1
    },
    'Fire': {
        'Normal': 1, 
        'Fire': 0.5,   
        'Water': 0.5, 
        'Grass': 2,
        'Electric': 1,  
        'Ice': 2,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 2,  
        'Rock': 0.5,  
        'Ghost': 1,  
        'Dragon': 0.5,  
        'Dark': 1,  
        'Steel': 2,  
        'Fairy': 1
    },
    'Water': {
        'Normal': 1, 
        'Fire': 2,   
        'Water': 0.5, 
        'Grass': 0.5,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 2,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 2,  
        'Ghost': 1,  
        'Dragon': 0.5,  
        'Dark': 1,  
        'Steel': 1,  
        'Fairy': 1
    },
    'Grass': {
         'Normal': 1, 
        'Fire': 0.5,   
        'Water': 2, 
        'Grass': 0.5,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 0.5,  
        'Ground': 2,  
        'Flying': 0.5,  
        'Psychic': 1,  
        'Bug': 0.5,  
        'Rock': 2,  
        'Ghost': 1,  
        'Dragon': 0.5,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 1
    },
    'Electric': {
      'Normal': 1, 
        'Fire': 1,   
        'Water': 2, 
        'Grass': 0.5,
        'Electric': 0.5,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 0,  
        'Flying': 2,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 1,  
        'Dragon': 0.5,  
        'Dark': 1,  
        'Steel': 1,  
        'Fairy': 1
    },
    'Ice': {
      'Normal': 1, 
        'Fire': 0.5,   
        'Water': 0.5, 
        'Grass': 2,
        'Electric': 1,  
        'Ice': 0.5,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 2,  
        'Flying': 2,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 1,  
        'Dragon': 2,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 1
    },
    'Fighting': {
      'Normal': 2, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 2,  
        'Fighting': 1,  
        'Poison': 0.5,  
        'Ground': 1,  
        'Flying': 0.5,  
        'Psychic': 0.5,  
        'Bug': 0.5,  
        'Rock': 2,  
        'Ghost': 0,  
        'Dragon': 1,  
        'Dark': 2,  
        'Steel': 2,  
        'Fairy': 0.5
    },
    'Poison': {
        'Normal': 1, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 2,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 0.5,  
        'Ground': 0.5,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 0.5,  
        'Ghost': 0.5,  
        'Dragon': 1,  
        'Dark': 1,  
        'Steel': 0,  
        'Fairy': 2
    },
    'Ground': {
        'Normal': 1, 
        'Fire': 2,   
        'Water': 1, 
        'Grass': 0.5,
        'Electric': 2,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 2,  
        'Ground': 1,  
        'Flying': 0,  
        'Psychic': 1,  
        'Bug': 0.5,  
        'Rock': 2,  
        'Ghost': 1,  
        'Dragon': 1,  
        'Dark': 1,  
        'Steel': 2,  
        'Fairy': 1
    },
    'Flying': {
        'Normal': 1, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 2,
        'Electric': 0.5,  
        'Ice': 1,  
        'Fighting':2,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 2,  
        'Rock': 0.5,  
        'Ghost': 1,  
        'Dragon': 1,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 1
    },
    'Psychic': {
        'Normal': 1, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 2,  
        'Poison': 2,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 0.5,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 1,  
        'Dragon': 1,  
        'Dark': 0,  
        'Steel': 0.5,  
        'Fairy': 1
    },
    'Bug': {
        'Normal': 1, 
        'Fire': 0.5,   
        'Water': 1, 
        'Grass': 2,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 0.5,  
        'Poison': 0.5,  
        'Ground': 1,  
        'Flying': 0.5,  
        'Psychic': 2,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 0.5,  
        'Dragon': 1,  
        'Dark': 2,  
        'Steel': 0.5,  
        'Fairy': 0.5
    },
    'Rock': {
        'Normal': 1, 
        'Fire': 2,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 2,  
        'Fighting': 0.5,  
        'Poison': 1,  
        'Ground': 0.5,  
        'Flying': 2,  
        'Psychic': 1,  
        'Bug': 2,  
        'Rock': 1,  
        'Ghost': 1,  
        'Dragon': 1,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 1
    },
    'Ghost': {
        'Normal': 0, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 2,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 2,  
        'Dragon': 1,  
        'Dark': 0.5,  
        'Steel': 1,  
        'Fairy': 1
    },
    'Dragon': {
        'Normal': 1, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 1,  
        'Dragon': 2,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 0
    },
    'Dark': {
        'Normal': 1, 
        'Fire': 1,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 0.5,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 2,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 2,  
        'Dragon': 1,  
        'Dark': 0.5,  
        'Steel': 1,  
        'Fairy': 0.5
    },
    'Steel': {
        'Normal': 1, 
        'Fire': 0.5,   
        'Water': 0.5, 
        'Grass': 1,
        'Electric': 0.5,  
        'Ice': 2,  
        'Fighting': 1,  
        'Poison': 1,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic': 1,  
        'Bug': 1,  
        'Rock': 2,  
        'Ghost': 1,  
        'Dragon': 1,  
        'Dark': 1,  
        'Steel': 0.5,  
        'Fairy': 2
    },
    'Fairy': {
        'Normal': 1, 
        'Fire': 0.5,   
        'Water': 1, 
        'Grass': 1,
        'Electric': 1,  
        'Ice': 1,  
        'Fighting': 2,  
        'Poison': 0.5,  
        'Ground': 1,  
        'Flying': 1,  
        'Psychic':1,  
        'Bug': 1,  
        'Rock': 1,  
        'Ghost': 1,  
        'Dragon': 2,  
        'Dark': 2,  
        'Steel': 0.5,  
        'Fairy': 1
    },

}

#Função que obtem o pokechart ( Diz que tipo toma dano de que)
def GetPokeInteractions(Poketypes):
    Strengths= {}
    Weaknesses= {}
    tipo1 = Poketypes[0]
    Val = 0
    if(len(poketypes)==1):
        for target_type in tipo_interacoes[tipo1]:
            Val = tipo_interacoes[tipo1].get(target_type, 1)
            if(Val == 1):
                continue
            if(Val == 2):
                Strengths[target_type] = tipo_interacoes[tipo1].get(target_type, 1)
                continue
            Weaknesses[target_type] = tipo_interacoes[tipo1].get(target_type, 1)
        return [Strengths,Weaknesses]
    tipo2 = Poketypes[1]
    for target_type in tipo_interacoes[tipo1]:
        Val = tipo_interacoes[tipo1].get(target_type, 1) * tipo_interacoes[tipo2].get(target_type, 1)
        if(Val == 1):
            continue
        if(Val == 2):
            Strengths[target_type] = tipo_interacoes[tipo1].get(target_type, 1) * tipo_interacoes[tipo2].get(target_type, 1)
            continue
        Weaknesses[target_type] = tipo_interacoes[tipo1].get(target_type, 1) * tipo_interacoes[tipo2].get(target_type, 1)
    return [Strengths,Weaknesses]
poketypes = ['Fairy'] 
#print(GetPokeInteractions(poketypes)[0])



def DualsTypeInteraction(ArrayInteracoes1,ArrayInteracoes2):
    
    Weaknes1 = ArrayInteracoes1[0]
    Weaknes2 = ArrayInteracoes2[0]
     
    Imunidades1 = ArrayInteracoes1[1]
    Imunidades2 = ArrayInteracoes2[1]

    Resistences1 = ArrayInteracoes1[2]
    Resistences2 = ArrayInteracoes2[2]

    FinalInteractionsWeakness = []
    FinalInteractionsImunidades = []
    FinalInteractionsResistences = []

    for i in Imunidades1:
     
        J = i.split(" ")[0]
        for K in Imunidades2:
            if(J == K.split(" ")[0]):
                FinalInteractionsImunidades.append(K.split(" ")[0])
   
    for i in Weaknes1:
     
        J = i.split(" ")[0]
        for K in Weaknes2:
            if(J == K.split(" ")[0]):
                FinalInteractionsWeakness.append(K.split(" ")[0])
   

    for i in Resistences1:
     
        J = i.split(" ")[0]
        for K in Resistences2:
            if(J == K.split(" ")[0]):
                FinalInteractionsResistences.append(K.split(" ")[0])
    return (FinalInteractionsWeakness,FinalInteractionsImunidades,FinalInteractionsResistences)

    
def StrenghtAndWeakness(Type1,Type2): 



    tipo1 = CapitalizeFirstLetter(Type1)
    tipo2 = CapitalizeFirstLetter(Type2)
   
   
    TypesNames = ['Normal','Fire','Water','Grass','Electric','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy']
    Weakness = []
    Imunidades =[]
    Resistences =[]
    ReturnFromType1 = []
    ReturnFromType2 = []
    FinalInteractions = []


    global Val
    Val = []
    
    if tipo2==None: #Monotype
        for Type in tipo_interacoes:
            for target_type in tipo_interacoes[Type]:
                if target_type == tipo1:
                    FinalInteractions.append(Type)
                    FinalInteractions.append(tipo_interacoes[Type].get(tipo1, 1))
        
        for i in range(0, len(FinalInteractions), 2):
                nome = FinalInteractions[i] 
                numero = FinalInteractions[i + 1]  
                if numero < 1 and numero != 0:
                    str = f"{nome} {numero}X"
                    Resistences.append(str)
                if numero == 0:
                    Imunidades.append(nome)
                    continue
                elif numero == 1:
                    continue
                elif numero == 2:
                    Weakness.append(nome)
                    continue
                elif numero == 4:
                    Weakness.append(nome+" 4X ")
                    continue
        return(Weakness,Imunidades,Resistences)

    else:





        
        for Type in tipo_interacoes:
            
            for target_type in tipo_interacoes[Type]:
                
                TempVal = 1
             
                      
                if target_type == tipo1:
                  
                    
                    TempVal *= tipo_interacoes[Type].get(tipo1, 1)
                    ReturnFromType1.append(tipo_interacoes[Type].get(tipo1, 1))
                    

                elif target_type == tipo2:
            

                    
                    TempVal *= tipo_interacoes[Type].get(target_type, 1)
                    ReturnFromType2.append(tipo_interacoes[Type].get(tipo2, 1))
                    
                
        
       
  
        for i in range(0,len(ReturnFromType1)):
            NormVal = ReturnFromType1[i]*ReturnFromType2[i]
            FinalInteractions.append(TypesNames[i])
            FinalInteractions.append(NormVal)


       
        for i in range(0, len(FinalInteractions), 2):
                nome = FinalInteractions[i] 
                numero = FinalInteractions[i + 1]  
          
                if numero < 1 and numero != 0:
                    str = f"{nome} {numero}X"
                    Resistences.append(str)
                elif numero == 0:
                    Imunidades.append(nome)
                    continue
                elif numero == 1:
                    continue
                elif numero == 2:
                    Weakness.append(nome)
                    continue
                elif numero == 4:
                    Weakness.append(nome+" 4X ")
                    continue
                


        return (Weakness,Imunidades,Resistences)
