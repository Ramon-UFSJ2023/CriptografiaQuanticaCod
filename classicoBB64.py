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
                bitSendBob = resultadoEveObteu
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
    VectorAlicePosAmostragem=[]
    VectorBobPosAmostragem = []

    for i in range(tamanho_amostragem):
        posicao = vector_posi[i]
        if newVectorAlice[posicao].Qubit == newVectorBob[posicao].Qubit: 
            numeroBitsCertos = numeroBitsCertos+1
    taxa_erro =(tamanho_amostragem-numeroBitsCertos)/tamanho_amostragem

    for i in range(tamanhoVector):
        if i != posicao:
            VectorAlicePosAmostragem.append(newVectorAlice[i])
            VectorBobPosAmostragem.append(newVectorBob[i])
    return taxa_erro, tamanho_amostragem, numeroBitsCertos, VectorAlicePosAmostragem, VectorBobPosAmostragem

def taxaDeErroGeral(vectorAlicePosAmostragem, vectorBobPosAmostragem):
    bits_certos =0
    tamanho_vector = len(vectorBobPosAmostragem)

    for i in range(tamanho_vector):
        if(vectorAlicePosAmostragem[i].Qubit == vectorBobPosAmostragem[i].Qubit):
            bits_certos+=1
    taxa_acerto_geral = bits_certos/tamanho_vector
    taxa_erro_geral = (tamanho_vector-bits_certos)/tamanho_vector
    return bits_certos, taxa_acerto_geral, taxa_erro_geral, tamanho_vector



def FindQtdBits():
    qtd_bits = 256
    taxaDeErroSemCanal=3
    tamanhoAmostragem =0
    numeroBitCertos =0

    while(taxaDeErroSemCanal>0.2):
        vectorAlice = gereVectorAlice(qtd_bits);
        vectorEveInterfere=VectorInterferenciaEve(vectorAlice, qtd_bits)
        vectorBob=MedicaoBob(vectorEveInterfere, qtd_bits)
        newVectorAlice,newVectorBob = comparacaoBase(vectorAlice, vectorBob, qtd_bits)

        taxaDeErroSemCanal, tamanhoAmostragem, numeroBitCertos, vectorAlicePosAmostragem, vectorBobPosAmostragem = amostragem(newVectorAlice, newVectorBob)
        qtd_bits= qtd_bits+2

    bitsCertosGeral, taxaAcertoGeral, taxaDeErroGera, tamanhoVectorPosAmostragem = taxaDeErroGeral(vectorAlicePosAmostragem, vectorBobPosAmostragem)
    print(f"Tamanho do vector: {qtd_bits}\n")
    print(f"Tamanho Amostragem: {tamanhoAmostragem}")
    print("Bits Certos da Amostra{numeroBitCertos}")
    print("Taxa de acerto da amostragem: {:.4f}".format(numeroBitCertos/tamanhoAmostragem))
    print("Taxa de erro da amostra: {:.4f}\n".format(taxaDeErroSemCanal))

    print(f"Numero de Bits PosAmostragem: {tamanhoVectorPosAmostragem}")
    print(f"Numero de Bits certos PosAmostragem: {bitsCertosGeral}")
    print("Taxa de acerto Geral: {:.4f}".format(taxaAcertoGeral))
    print("Taxa de Erro Geral: {:.4f}".format(taxaDeErroGera))


def  main():
    FindQtdBits()
main()