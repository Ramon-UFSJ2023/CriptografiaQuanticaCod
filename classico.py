from dataclasses import dataclass
import random as rd
import math as mt

#TD_BITS = 5
QTD_BITS_AMOSTRAGEM = 0.2 #20% do vector
PERCA_CANAL = 0.02 #Taxa de erro do canal é inserida antes e depois da interferencia da eve
#taxa de erro vc define

@dataclass
class Bases:
    Base_Z: str
    Base_X: str

@dataclass
class SimuQubit:
    QubitOne: str
    QubitZero: str
    QubitMore: str
    QubitMinus: str

@dataclass
class VectorQubit:
    Qubit: str
    Base: str
    

escolhaBases = Bases(Base_Z='baseZ', Base_X='baseX')
escolhaQubit = SimuQubit(QubitOne = "1", QubitZero = "0", QubitMore="+", QubitMinus="-")

def gereVectorAlice(qtd_bits):
    vectorAlice = []
    for _ in range(qtd_bits):
        baseSort = rd.choice([escolhaBases.Base_X, escolhaBases.Base_Z])
        if baseSort == escolhaBases.Base_Z:
            bitChoice = rd.choice([escolhaQubit.QubitOne, escolhaQubit.QubitZero])
        else:
            bitChoice = rd.choice([escolhaQubit.QubitMinus, escolhaQubit.QubitMore])
        vectorAlice.append(VectorQubit(Qubit=bitChoice, Base=baseSort))
    return vectorAlice;

def VectorInterferenciaEve(vectorAlice, qtd_bits):
    vectorEveEnvBob = []
    vectorObtidoEve = []

    for i in range(qtd_bits):
        vector_ori = vectorAlice[i]
        BaseSortEve = rd.choice([escolhaBases.Base_X, escolhaBases.Base_Z])
        
        if BaseSortEve == vector_ori.Base:
            resultadoEveObteu = vector_ori.Qubit
            bitSendBob = vector_ori.Qubit
        else:
            if BaseSortEve == escolhaBases.Base_X:
                resultadoEveObteu = rd.choice([escolhaQubit.QubitMinus,escolhaQubit.QubitMore])
            else:
                resultadoEveObteu = rd.choice([escolhaQubit.QubitZero,escolhaQubit.QubitOne])
            bitSendBob = resultadoEveObteu

        baseSendBob = BaseSortEve
        #vectorObtidoEve.append(resultadoEveObteu)
        vectorEveEnvBob.append(VectorQubit(Qubit=bitSendBob, Base=baseSendBob))
    return vectorEveEnvBob #vectorObtidoEve

def MedicaoBob(vectorVindoDeEve, qtd_bits):
    vectorBob = []
    for i in range(qtd_bits):
        baseSortBob = (rd.choice([escolhaBases.Base_X, escolhaBases.Base_Z]))
        qubitRecebido = vectorVindoDeEve[i]

        if baseSortBob == qubitRecebido.Base:
            vectorBob.append(qubitRecebido)
        else:
            if baseSortBob == escolhaBases.Base_X:
                vectorBob.append(VectorQubit(Qubit=rd.choice([escolhaQubit.QubitMinus,escolhaQubit.QubitMore]), Base=escolhaBases.Base_X))
            else:
                vectorBob.append(VectorQubit(Qubit=rd.choice([escolhaQubit.QubitZero,escolhaQubit.QubitOne]), Base=escolhaBases.Base_Z))

    return vectorBob

def comparacaoBase(vectorAlice, vectorBob, qtd_bits):
    #vectorPosicoesResultante =[]
    newVectorAlice = []
    newVectorBob = []

    for i in range(qtd_bits):
        if vectorAlice[i].Base == vectorBob[i].Base:
            #vectorPosicoesResultante.append(i)
            newVectorBob.append(VectorQubit(Qubit=vectorBob[i].Qubit, Base=vectorBob[i].Base))
            newVectorAlice.append(VectorQubit(Qubit=vectorAlice[i].Qubit, Base=vectorAlice[i].Base))
    return newVectorAlice, newVectorBob

def amostragem(newVectorAlice, newVectorBob):
    taxa_erro = 0
    numeroBitsCertos= 0
    tamanhoVector = len(newVectorAlice)
    tamanho_amostragem = mt.ceil(tamanhoVector*QTD_BITS_AMOSTRAGEM)
    vector_posi = rd.sample(range(tamanhoVector),k=tamanho_amostragem)

    for i in range(tamanho_amostragem):
        posicao = vector_posi[i]
        if newVectorAlice[posicao].Qubit == newVectorBob[posicao].Qubit:
            numeroBitsCertos = numeroBitsCertos+1
    taxa_erro = (tamanho_amostragem-numeroBitsCertos)/tamanho_amostragem
    return taxa_erro, tamanho_amostragem

def FindQtdBits():
    qtd_bits = 10
    taxaDeErroSemCanal=0
    while(taxaDeErroSemCanal>0.2):
        vectorAlice = gereVectorAlice(qtd_bits);
        vectorEveInterfere=VectorInterferenciaEve(vectorAlice, qtd_bits)
        vectorBob=MedicaoBob(vectorEveInterfere, qtd_bits)
        newVectorAlice,newVectorBob = comparacaoBase(vectorAlice, vectorBob, qtd_bits)
        taxaDeErroSemCanal, tamanhoAmostragem= amostragem(newVectorAlice, newVectorBob)
        qtd_bits= qtd_bits+2
    print(qtd_bits)
    print(tamanhoAmostragem)