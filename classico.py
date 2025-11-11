from dataclasses import dataclass
import random as rd

#Simular meio quantico atraves do meio classico
P_ERRO = 2/4
QTD_BITS = 5

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

def gereVectorAlice():
    vectorAlice = []
    for _ in range(QTD_BITS):
        baseSort = rd.choice([escolhaBases.Base_X, escolhaBases.Base_Z])
        if baseSort == escolhaBases.Base_Z:
            bitChoice = rd.choice([escolhaQubit.QubitOne, escolhaQubit.QubitZero])
        else:
            bitChoice = rd.choice([escolhaQubit.QubitMinus, escolhaQubit.QubitMore])
        vectorAlice.append(VectorQubit(Qubit=bitChoice, Base=baseSort))
    return vectorAlice;


def escolhaBaseBob():
    vectorBaseBob = []
    for _ in range(QTD_BITS):
        vectorBaseBob.append(rd.choice([escolhaBases.Base_X, escolhaBases.Base_Z]))
    return vectorBaseBob

def interferenciaEve(vectorAlice):
    for _ in range(QTD_BITS):
        baseSort = rd.choice([escolhaBases.Base_X, escolhaBases.Base_Z])
        

