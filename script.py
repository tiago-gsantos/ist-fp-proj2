# Fundamentos da Programação - Segundo Projeto - 2022-23 #




# Funções auxiliares
def int_entre(min, max, num):
  """
  Devolve True se o argumento num for inteiro e estiver entre os argumentos min
  e max.

  Args / Returns: int, int, universal --> bool
  """
  return isinstance(num, int) and min <= num <= max

def ord_1a26(c):
  """
  Devolve um número de 1 a 26 correspondente à posição do caracter de entrada
  no alfabeto.

  Args / Returns: str --> int
  """
  return ord(c) - ord('A') + 1

def formata_num(n):
  """
  Converte o número de entrada numa string de tamanho 2.

  Args / Returns: int --> str
  """
  if n < 10:
    return f"0{n}"
  return str(n)

def bits_e_seed_validos(num_bits, seed):
  """
  Verifica se os argumentos são válidos

  Args / Returns: universal, universal --> bool
  """
  return (isinstance(num_bits, int) and
         (num_bits == 32 and int_entre(1, 2**32 -1, seed) or 
          num_bits == 64 and int_entre(1, 2**64 -1, seed)))

def col_e_lin_validos(col, lin):
  """
  Verifica se os argumentos são válidos

  Args / Returns: universal, universal --> bool
  """
  return (isinstance(col, str) and len(col) == 1 and 
          int_entre(1, 26, ord_1a26(col)) and int_entre(1, 99, lin))

def coor_vizinhas_do_campo(campo, coor):
  """
  Devolve a lista das coordenadas vizinhas da coordenada de entrada que
  pertencem ao campo dado.

  Args / Returns: campo, coordenada --> list
  """
  return [c for c in obtem_coordenadas_vizinhas(coor)
            if eh_coordenada_do_campo(campo, c)]

def coor_escolhida(campo):
  """
  Pede ao utilizador uma coordenada até este introduzir uma coordenada válida e
  devolve a string correspondente.

  Args / Returns: campo --> str
  """
  coor = input('Escolha uma coordenada:')
  while not (len(coor) == 3 and 
             coor[1].isnumeric() and
             col_e_lin_validos(coor[0], int(coor[1:])) and 
             eh_coordenada_do_campo(campo, str_para_coordenada(coor))):
    coor = input('Escolha uma coordenada:')
  return coor




# TAD - gerador


# Construtores
def cria_gerador(num_bits, seed):
  """
  Devolve um gerador que contém um número de bits (que pode ser 32 ou 64) e o
  estado inicial ou a seed.

  Args / Returns: int, int --> gerador
  """
  if not bits_e_seed_validos(num_bits, seed):
    raise ValueError('cria_gerador: argumentos invalidos')
  return {'num_bits': num_bits, 'seed': seed}

def cria_copia_gerador(gerador):
  """
  Devolve uma cópia do gerador de entrada.

  Args / Returns: gerador --> gerador
  """
  return gerador.copy()


# Seletores
def obtem_bits(gerador):
  """
  Devolve o número de bits do gerador de entrada.

  Args / Returns: gerador --> int
  """
  return gerador['num_bits']

def obtem_estado(gerador):
  """
  Devolve o estado atual do gerador de entrada.

  Args / Returns: gerador --> int
  """
  return gerador['seed']


# Modificadores
def define_estado(gerador, seed):
  """
  Altera o valor do estado do gerador de entrada para o argumento seed e
  devolve o novo estado.

  Args / Returns: gerador, int --> int
  """
  gerador['seed'] = seed
  return obtem_estado(gerador)

def atualiza_estado(gerador):
  """
  Atualiza o estado do gerador de entrada de acordo com o algoritmo xorshift de
  geração de números pseudoaleatórios, e devolve-o.

  Args / Returns: gerador --> int
  """
  if obtem_bits(gerador) == 32:
    gerador['seed'] ^= (obtem_estado(gerador) << 13) & 0xFFFFFFFF
    gerador['seed'] ^= (obtem_estado(gerador) >> 17) & 0xFFFFFFFF
    gerador['seed'] ^= (obtem_estado(gerador) << 5) & 0xFFFFFFFF
  elif obtem_bits(gerador) == 64:
    gerador['seed'] ^= (obtem_estado(gerador) << 13) & 0xFFFFFFFFFFFFFFFF
    gerador['seed'] ^= (obtem_estado(gerador) >> 7) & 0xFFFFFFFFFFFFFFFF
    gerador['seed'] ^= (obtem_estado(gerador) << 17) & 0xFFFFFFFFFFFFFFFF
  return obtem_estado(gerador)


# Reconhecedor
def eh_gerador(arg):
  """
  Devolve True caso o argumento seja um TAD gerador e False caso contrário.

  Args / Returns: universal --> bool
  """
  return isinstance(arg, dict) and len(arg) == 2 and \
         'num_bits' in arg and 'seed' in arg and \
         bits_e_seed_validos(obtem_bits(arg), obtem_estado(arg))


# Teste
def geradores_iguais(gerador1, gerador2):
  """
  Devolve True se os argumentos de entrada são geradores e são iguais.

  Args / Returns: gerador, gerador --> bool
  """
  return eh_gerador(gerador1) and eh_gerador(gerador2) and gerador1 == gerador2


# Transformador
def gerador_para_str(gerador):
  """
  Devolve a string que representa o gerador de entrada.

  Args / Returns: gerador --> str
  """
  return f'xorshift{obtem_bits(gerador)}(s={obtem_estado(gerador)})'


# Funções de alto nível
def gera_numero_aleatorio(gerador, n):
  """
  Atualiza o estado do gerador de entrada e devolve um número aleatório no
  intervalo [1, n], utilizando o novo estado do gerador.

  Args / Returns: gerador, int --> int
  """
  return 1 + atualiza_estado(gerador) % n

def gera_carater_aleatorio(gerador, c):
  """
  Atualiza o estado do gerador de entrada e devolve um carater aleatório no
  intervalo entre 'A' e o carater maiúsculo c, utilizando o novo estado do
  gerador.

  Args / Returns: gerador, int --> int
  """
  return chr(65 + atualiza_estado(gerador) % ord_1a26(c))




# TAD coordenada


# Construtor
def cria_coordenada(col, lin):
  """
  Devolve uma coordenada com a coluna (de 'A' a 'Z') e linha (de 1 a 99)
  correspondentes.

  Args / Returns: str, int --> coordenada
  """
  if not col_e_lin_validos(col, lin):
    raise ValueError('cria_coordenada: argumentos invalidos')
  return (col, lin)


# Seletores
def obtem_coluna(coor):
  """
  Devolve a coluna da coordenada de entrada.

  Args / Returns: coordenada --> str
  """
  return coor[0]

def obtem_linha(coor):
  """
  Devolve a linha da coordenada de entrada.

  Args / Returns: coordenada --> int
  """
  return coor[1]


# Reconhecedor
def eh_coordenada(arg):
  """
  Devolve True caso o argumento seja um TAD coordenada e False caso contrário.

  Args / Returns: universal --> bool
  """
  return (isinstance(arg, tuple) and len(arg) == 2 and
          col_e_lin_validos(obtem_coluna(arg), obtem_linha(arg)))


# Teste
def coordenadas_iguais(coor1, coor2):
  """
  Devolve True se os argumentos de entrada são coordenadas e são iguais.

  Args / Returns: coordenada, coordenada --> bool
  """
  return eh_coordenada(coor1) and eh_coordenada(coor2) and coor1 == coor2


# Transformadores
def coordenada_para_str(coor):
  """
  Devolve a string que representa a coordenada de entrada.

  Args / Returns: coordenada --> str
  """
  return f'{obtem_coluna(coor)}{formata_num(obtem_linha(coor))}'

def str_para_coordenada(string):
  """
  Devolve a coordenada representada pela string de entrada.

  Args / Returns: str --> coordenada
  """
  if string[1] == '0':
    return cria_coordenada(string[0], int(string[2:]))
  return cria_coordenada(string[0], int(string[1:]))


# Funções de alto nível
def obtem_coordenadas_vizinhas(coor):
  """
  Devolve um tuplo com as coordenadas vizinhas da coordenada de entrada,
  começando na de cima à esquerda e seguindo o sentido horário.

  Args / Returns: coordenada --> tuple
  """
  col_c, lin_c = ord(obtem_coluna(coor)), obtem_linha(coor)

  template = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
  vizinhas = []

  for c, n in template:
    if col_e_lin_validos(chr(col_c + c), lin_c + n):
      vizinhas.append(cria_coordenada(chr(col_c + c), lin_c + n))

  return tuple(vizinhas)

def obtem_coordenada_aleatoria(coor, gerador):
  """
  Devolve coordenada gerada aleatoriamente utilizando o gerador de entrada e em
  que a coordenada de entrada define a maior coluna e maior linha possíveis.

  Args / Returns: coordenada, gerador --> coordenada
  """
  col = gera_carater_aleatorio(gerador, obtem_coluna(coor))
  lin = gera_numero_aleatorio(gerador, obtem_linha(coor))
  return cria_coordenada(col, lin)




# TAD parcela


# Construtores
def cria_parcela():
  """
  Devolve uma parcela tapada sem mina escondida.

  Args / Returns: {} --> tuple
  """
  return {'estado': 'tapada', 'mina': False}

def cria_copia_parcela(parc):
  """
  Devolve uma cópia da parcela de entrada.

  Args / Returns: parcela --> parcela
  """
  return parc.copy()


# Modificadores
def limpa_parcela(parc):
  """
  Modifica o estado da parcela de entrada para limpa e devolve a própria parcela.

  Args / Returns: parcela --> parcela
  """
  parc['estado'] = 'limpa'
  return parc

def marca_parcela(parc):
  """
  Modifica o estado da parcela de entrada para marcada e devolve a própria.
  parcela.

  Args / Returns: parcela --> parcela
  """
  parc['estado'] = 'marcada'
  return parc

def desmarca_parcela(parc):
  """
  Modifica o estado da parcela de entrada para tapada e devolve a própria.
  parcela.

  Args / Returns: parcela --> parcela
  """
  parc['estado'] = 'tapada'
  return parc

def esconde_mina(parc):
  """
  Esconde uma mina na parcela de entrada e devolve a própria parcela.

  Args / Returns: parcela --> parcela
  """
  parc['mina'] = True
  return parc


# Reconhecedor
def eh_parcela(arg):
  """
  Devolve True caso o argumento seja um TAD parcela e False caso contrário.

  Args / Returns: universal --> bool
  """
  return (isinstance(arg, dict) and len(arg) == 2 and
          'estado' in arg and 'mina' in arg and
          arg['estado'] in ['tapada', 'limpa', 'marcada'] and
          isinstance(arg['mina'], bool))

def eh_parcela_tapada(parc):
  """
  Devolve True caso a parcela de entrada se encontre tapada e False caso
  contrário.

  Args / Returns: parcela --> bool
  """
  return parc['estado'] == 'tapada'

def eh_parcela_marcada(parc):
  """
  Devolve True caso a parcela de entrada se encontre marcada e False caso
  contrário.

  Args / Returns: parcela --> bool
  """
  return parc['estado'] == 'marcada'

def eh_parcela_limpa(parc):
  """
  Devolve True caso a parcela de entrada se encontre limpa e False caso
  contrário.

  Args / Returns: parcela --> bool
  """
  return parc['estado'] == 'limpa'

def eh_parcela_minada(parc):
  """
  Devolve True caso a parcela de entrada esconda uma mina e False caso
  contrário.

  Args / Returns: parcela --> bool
  """
  return parc['mina'] == True


# Teste
def parcelas_iguais(parc1, parc2):
  """
  Devolve True se os argumentos de entrada são parcelas e são iguais.

  Args / Returns: parcela, parcela --> bool
  """
  return eh_parcela(parc1) and eh_parcela(parc2) and parc1 == parc2


# Transformador
def parcela_para_str(parc):
  """
  Devolve a string que representa a parcela de entraa em função do seu estado.

  Args / Returns: parcela --> str
  """
  if parc['estado'] == 'tapada':
    return '#'
  elif parc['estado'] == 'marcada':
    return '@'
  elif parc['mina']:
    return 'X'
  return '?'


# Funções de alto nível
def alterna_bandeira(parc):
  """
  Desmarca a parcela de entrada se estiver marcada e marca se estiver tapada,
  devolvendo True. Se não houver nenhuma modificação devolve False.

  Args / Returns: parcela --> bool
  """
  if eh_parcela_marcada(parc):
    desmarca_parcela(parc)
    return True
  elif eh_parcela_tapada(parc):
    marca_parcela(parc)
    return True
  return False




# TAD campo


# Construtores
def cria_campo(col_max, lin_max):
  """
  Devolve o campo com número de colunas e linhas iguais aos argumentos formado
  por parcelas tapadas sem minas.

  Args / Returns:  str, int --> campo
  """
  if not col_e_lin_validos(col_max, lin_max):
    raise ValueError('cria_campo: argumentos invalidos')

  campo = []
  for lin in range(1, lin_max + 1):
    for col in range(65, ord(col_max) + 1):    
      campo.append([cria_coordenada(chr(col), lin), cria_parcela()])
  return campo

def cria_copia_campo(campo):
  """
  Devolve uma cópia do campo de entrada.

  Args / Returns: campo --> campo
  """
  copia_campo = []
  for coord, parc in campo:
    copia_campo.append([coord, cria_copia_parcela(parc)])
  return copia_campo


# Seletores
def obtem_ultima_coluna(campo):
  """
  Devolve a string que corresponde à última coluna do campo.

  Args / Returns: campo --> str
  """
  return campo[-1][0][0]

def obtem_ultima_linha(campo):
  """
  Devolve o valor que corresponde à última linha do campo.

  Args / Returns: campo --> int
  """
  return campo[-1][0][1]

def obtem_parcela(campo, coor):
  """
  Devolve a parcela do campo de entrada que se encontra na coordenada dada.

  Args / Returns: campo, coordenada --> parcela
  """
  i = 0
  for el in campo:
    if coordenadas_iguais(el[0], coor):
      break
    i += 1
  return campo[i][1]

def obtem_coordenadas(campo, string):
  """
  Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente da
  esquerda para a direita e de cima para baixo das parcelas de acordo com a
  string de entrada ('limpas', 'tapadas', 'marcadas' ou 'minadas').

  Args / Returns: campo, str --> tuple
  """
  coordenadas = []
  for i in campo:
    if (string == 'limpas' and eh_parcela_limpa(i[1]) or
          string == 'tapadas' and eh_parcela_tapada(i[1]) or
          string == 'marcadas' and eh_parcela_marcada(i[1]) or
          string == 'minadas' and eh_parcela_minada(i[1])):
      coordenadas.append(i[0])

  return tuple(coordenadas)

def obtem_numero_minas_vizinhas(campo, coor):
  """
  Devolve o número de parcelas vizinhas da parcela na coordenada de entrada que
  escondem mina.

  Args / Returns: campo, coordenada --> int
  """
  return len([c for c in obtem_coordenadas(campo, 'minadas') 
                if c in obtem_coordenadas_vizinhas(coor)])


# Reconhecedores
def eh_campo(arg):
  """
  Devolve True caso o argumento seja um TAD campo e False caso contrário.

  campo --> [[coor, parc], [coor, parc], ...]

  Args / Returns: universal --> bool
  """
  if not (isinstance(arg, list) and len(arg) > 0):
    return False
  for el in arg:
    if not (isinstance(el, list) and len(el) == 2 and
            eh_coordenada(el[0]) and eh_parcela(el[1])):
      return False
  return True

def eh_coordenada_do_campo(campo, coor):
  """
  Devolve True se a coordenada de entrada é uma coordenada válida do campo dado
  e False caso contrário.

  Args / Returns: campo, coordenada --> bool
  """
  for i in campo:
    if coordenadas_iguais(i[0], coor):
      return True
  return False


# Teste
def campos_iguais(campo1, campo2):
  """
  Devolve True se os argumentos são campos e são iguais.

  Args / Returns: campo, campo --> bool
  """
  if (eh_campo(campo1) and eh_campo(campo2) and
      obtem_ultima_coluna(campo1) == obtem_ultima_coluna(campo2) and
      obtem_ultima_linha(campo1) == obtem_ultima_linha(campo2)):
    for i in range(len(campo1)):
      if not (coordenadas_iguais(campo1[i][0], campo2[i][0]) and
              parcelas_iguais(campo1[i][1], campo2[i][1])):
        return False
    return True
  return False


# Tranformador
def campo_para_str(campo):
  """
  Devolve uma cadeia de caracteres que representa o campo de minas.

  Args / Returns: campo --> str
  """
  # Função auxiliar
  def parcela_para_carater(campo, coor):
    parc = obtem_parcela(campo, coor)
    if eh_parcela_limpa(parc) and not eh_parcela_minada(parc):
      if obtem_numero_minas_vizinhas(campo, coor) == 0:
        return " "
      return str(obtem_numero_minas_vizinhas(campo, coor))
    return parcela_para_str(parc)

  letras = "".join([chr(l) for l in range(65, ord(obtem_ultima_coluna(campo)) + 1)])
  
  str_campo = f"   {letras}\n  +{'-' * len(letras)}+\n"

  for l in range(obtem_ultima_linha(campo)):
    str_linha = ""
    for c in letras:
      coor = cria_coordenada(c, l + 1)
      str_linha += parcela_para_carater(campo, coor)
    str_campo += f"{formata_num(l+1)}|{str_linha}|\n"
  return str_campo + f"  +{'-' * len(letras)}+"


# Funções de alto nível
def coloca_minas(campo, coor_inicial, gerador, num_minas):
  """
  Esconde um certo número de minas em parcelas do campo dado. As coordenadas
  destas parcelas são geradas aleatoriamente e não podem coincidir nem com a
  coordenada de entrada, nem com nenhuma das suas coordenadas vizinhas, nem com
  minas colocadas anteriormente. É devolvido o campo alterado.

  Args / Returns: campo, coordenada, gerador, int --> campo
  """
  coor_proibidas = [coor_inicial] + coor_vizinhas_do_campo(campo, coor_inicial)
  minas_colocadas = 0

  ul_c, ul_l = obtem_ultima_coluna(campo), obtem_ultima_linha(campo)
  
  while minas_colocadas < num_minas:
    c, l = gera_carater_aleatorio(gerador, ul_c), gera_numero_aleatorio(gerador, ul_l)
    coor = cria_coordenada(c, l)
    if coor not in coor_proibidas:
      esconde_mina(obtem_parcela(campo, coor))
      coor_proibidas += [coor]
      minas_colocadas += 1
  return campo

def limpa_campo(campo, coor):
  """
  Limpa o campo de entrada começando pela parcela na coordenada dada. Se não
  houver nenhuma mina vizinha escondida, limpa iterativamente todas as parcelas
  vizinhas tapadas. Caso a parcela já se encontre limpa, a operação não tem
  efeito. É devolvido o campo alterado.

  Args / Returns: campo, coordenada --> campo
  """
  parc = obtem_parcela(campo, coor)
  if not eh_parcela_limpa(parc) and not eh_parcela_marcada(parc):
    limpa_parcela(parc)
    if eh_parcela_minada(parc):
      return campo
    elif obtem_numero_minas_vizinhas(campo, coor) == 0:
      for coord in coor_vizinhas_do_campo(campo, coor):
        limpa_campo(campo, coord)
  return campo




# Funções adicionais
def jogo_ganho(campo):
  """
  Devolve True se todas as parcelas sem minas do campo de entrada se encontram
  limpas e False caso contrário.

  Args / Returns: campo --> bool
  """
  num_parc_totais = ord_1a26(obtem_ultima_coluna(campo)) * obtem_ultima_linha(campo)
  num_parc_limpas = len(obtem_coordenadas(campo, 'limpas'))
  num_parc_minadas = len(obtem_coordenadas(campo, 'minadas'))
  return num_parc_limpas + num_parc_minadas == num_parc_totais

def turno_jogador(campo):
  """
  Oferece ao jogador a opção de escolher uma ação ('L' para limpar e 'M' para
  marcar) e uma coordenada. O campo é alterado de acordo com ação escolhida e é
  devolvido False se o jogador limpou uma parcela que continha uma mina, ou
  True caso contrário.

  Args / Returns: campo --> bool
  """
  acao = input("Escolha uma ação, [L]impar ou [M]arcar:")
  while acao not in ['M', 'L']:
    acao = input("Escolha uma ação, [L]impar ou [M]arcar:")

  coor = coor_escolhida(campo)
  
  parc = obtem_parcela(campo, str_para_coordenada(coor))

  if acao == 'M' or eh_parcela_marcada(parc):
    alterna_bandeira(parc)
  if acao == 'L':
    limpa_campo(campo, str_para_coordenada(coor))
    if eh_parcela_minada(parc):
      return False
  return True

def minas(ul_c, ul_l, num_minas, num_bits, seed):
  """
  Função principal que permite jogar o jogo das minas. 
  A função cria o campo utilizando a última coluna e última linha dadas, coloca
  o número de minas dado em coordenadas aleatórias do campo utilizando um
  gerador com número de bits e seed iguais aos de entrada.
  Devolve True se o jogador conseguir ganhar o jogo, ou False caso contrário.

  Args / Returns: str, int, int, int, int --> bool
  """
  # Função auxiliar
  def jogada(campo, num_minas):
    print(f"   [Bandeiras {len(obtem_coordenadas(campo, 'marcadas'))}/{num_minas}]")
    print(campo_para_str(campo))

  if not (col_e_lin_validos(ul_c, ul_l) and 
         int_entre(1, ord_1a26(ul_c) * ul_l, num_minas) and 
         bits_e_seed_validos(num_bits, seed)):
    raise ValueError("minas: argumentos invalidos")
  
  # Ver se o campo é 1x1, 1x2, 2x1 ou 2x2
  if ((ord_1a26(ul_c) * ul_l) <= 2  or 
     (ul_c == 'B' and ul_l == 2)):
     raise ValueError("minas: argumentos invalidos")

  campo = cria_campo(ul_c, ul_l)
  jogada(campo, num_minas)
  coor = str_para_coordenada(coor_escolhida(campo))

  # Ver se é possível colocar todas as minas no campo
  if num_minas > (ord_1a26(ul_c) * ul_l) - 1 - len(coor_vizinhas_do_campo(campo, coor)):
    raise ValueError("minas: argumentos invalidos")

  coloca_minas(campo, coor, cria_gerador(num_bits, seed), num_minas)
  limpa_campo(campo, coor)

  while True:
    jogada(campo, num_minas)
    if jogo_ganho(campo):
      print("VITORIA!!!")
      return True
    if not turno_jogador(campo):
      jogada(campo, num_minas)
      print("BOOOOOOOM!!!")
      return False

