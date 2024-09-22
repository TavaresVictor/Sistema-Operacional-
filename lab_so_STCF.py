import numpy as np
import random

class Processo(object):
    def __init__(self,pnome,pio,ptam,prioridade,tempoChegada):
        self.nome = pnome
        self.io = pio # Probabilidade de fazer E/S, inicialmente zero
        self.tam = ptam # Quantos Timeslices sao necessarios para terminar
        self.prio = prioridade # Prioridade, eh desnecessaria aora 
        self.chegada = None
        self.inicio_processo = None
        #self.tempoInicioProcesso = None

    def roda(self,quantum=None): # se rodar sem quantum, o processor roda ate o fim
        if(random.randint(1,100)<self.io): #Verifica se fez E/S
            self.tam-=1
            print(self.nome," fez e/s, falta ",self.tam)
            return 1, True #True que fez E/S
            
            
        if(quantum is None or self.tam<quantum):
            quantum = self.tam
        self.tam -=quantum
        print(self.nome," rodou por ",quantum," timeslice, faltam ",self.tam)
        return quantum, False # False se nao fez E/S
    

class escalonadorSTCF(object): # Protótipo de escalonador de exemplo
    def __init__(self,vprontos=[]):
        self.prontos = vprontos #processos que cheam ao tempo zero

    def pronto(self,Processo):
        # implemente aqui o que escalonador faz quando surge um novo processo pronto
        self.prontos.append(Processo)

        
    def proximo(self):
        # implemente aqui a politica de escalonamento para definir um processo a ser executado
        if self.prontos is None:
            return None

        menorProcesso = self.prontos[0]

        for processo in self.prontos:
            if processo.tam < menorProcesso.tam:
                menorProcesso = processo
                
        self.prontos.remove(menorProcesso)
        return menorProcesso

nprocs = 5
nomes = ['A','B','C','D','E']
chanceio = [0,0,0,0,0] #Valor de zero a cem, chance de ser entrada e saida por enquanto deixem em zero
tamanho = np.array([20,20,20,20,20])


total = tamanho.sum()

procs = []
for i in range(nprocs):
    procs.append(Processo(nomes[i],chanceio[i],tamanho[i],0,0)) #cria uma lista procs de Processos


quantum = 2
tempoBloq = 1

escalonador = escalonadorSTCF(procs) #troque escalonador pelo seu escalonador
bloqueados = []

tempo = 0
tempo_execucao = 0
tempo_resposta = 0

random.seed(0)

while total>0:
    p = escalonador.proximo()
    if(p is not None):
        print("TEMPO ATUAL:",tempo,end=' ')
        if p.inicio_processo is None:
            
            p.inicio_processo = tempo
            tempo_resposta += tempo
        
        rodou, _ = p.roda(quantum) #adicione quantum como parâmetro, por enquanto nao temos E/S
        total-=rodou
        tempo+=rodou
        
        if(p.tam>0):
            escalonador.pronto(p)
        else:
            p.chegada = tempo
            tempo_execucao += p.chegada
        
    else:
        #Reduz o tempo de todos os bloqueados em uma unidade se nao havia ninguem pronto
        tempo+=1

print("\nTEMPO TOTAL:",tempo)
print("TEMPO MEDIO DE RESPOSTA:", (tempo_resposta / nprocs))
print("TEMPO MEDIO DE EXECUCAO:", (tempo_execucao / nprocs))