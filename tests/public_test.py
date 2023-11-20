import pytest
import sys
from exemplo import *


class TestPublicGerador:
    def test_1(self):
        g1 = cria_gerador(32, 1)
        assert gerador_para_str(g1) == 'xorshift32(s=1)'

    def test_2(self):
        g1 = cria_gerador(32, 1)
        assert [atualiza_estado(g1) for n in range(3)] == [270369, 67634689, 2647435461]

    def test_3(self):
        g1 = cria_gerador(32, 1)
        for n in range(3): atualiza_estado(g1)
        assert gera_numero_aleatorio(g1, 25) == 21

    def test_4(self):
        g1 = cria_gerador(32, 1)
        for n in range(3): atualiza_estado(g1)
        gera_numero_aleatorio(g1, 25)
        assert  gerador_para_str(g1) == 'xorshift32(s=307599695)'

    def test_5(self):
        g2 = cria_gerador(64, 1)
        assert [atualiza_estado(g2) for n in range(5)] == [1082269761, 1152992998833853505, 11177516664432764457, 17678023832001937445, 9659130143999365733]

    def test_6(self):
        g2 = cria_gerador(64, 1)
        [atualiza_estado(g2) for n in range(5)] 
        assert gerador_para_str(g2) == 'xorshift64(s=9659130143999365733)'

    def test_7(self):
        g2 = cria_gerador(64, 1)
        [atualiza_estado(g2) for n in range(5)] 
        gerador_para_str(g2)
        assert gera_carater_aleatorio(g2, 'Z') == 'L'


class TestPublicCoordenada:
    def test_1(self):
        with pytest.raises(ValueError) as excinfo:
            cria_coordenada('A', 200)
        assert "cria_coordenada: argumentos invalidos" == str(excinfo.value)
        
    def test_2(self):
        c1 = cria_coordenada('B', 1)
        c2 = cria_coordenada('N', 20)
        assert coordenadas_iguais(c1, c2) == False

    def test_3(self):
        c1 = cria_coordenada('B', 1)
        assert coordenada_para_str(c1) == 'B01'

    def test_4(self):
        c1 = cria_coordenada('B', 1)
        t = obtem_coordenadas_vizinhas(c1)
        assert ('C01', 'C02', 'B02', 'A02', 'A01') == tuple(coordenada_para_str(p) for p in t)

    def test_5(self):
        g1 = cria_gerador(32, 1)
        c3 = obtem_coordenada_aleatoria(cria_coordenada('Z', 99), g1)
        assert coordenada_para_str(c3) == 'V68'


class TestPublicParcela:
    def test_1(self):
        p1 = cria_parcela()
        assert parcela_para_str(p1) == '#'
    
    def test_2(self):
        p1 = cria_parcela()
        assert parcela_para_str(limpa_parcela(p1)) == '?'

    def test_3(self):
        p1 = cria_parcela()
        p2 = limpa_parcela(cria_copia_parcela(p1))
        assert not parcelas_iguais(p1, p2)

    def test_4(self):
        p1 = cria_parcela()
        p2 = cria_copia_parcela(p1)
        assert parcela_para_str(esconde_mina(p2)) == '#'

    def test_5(self):
        p1 = cria_parcela()
        p2 = cria_copia_parcela(p1)
        assert alterna_bandeira(esconde_mina(p2))

    def test_6(self):
        p1 = cria_parcela()
        p2 = cria_copia_parcela(p1) 
        alterna_bandeira(esconde_mina(p2))
        assert parcela_para_str(p2) == '@'

    def test_7(self):
        assert not alterna_bandeira(limpa_parcela(cria_parcela()))

    def test_8(self):
        p1 = cria_parcela()
        p2 = cria_copia_parcela(p1) 
        alterna_bandeira(esconde_mina(p2))
        assert eh_parcela_minada(p2)


class TestPublicCampo:
    def test_1(self):
        m = cria_campo('E',5)
        assert obtem_ultima_coluna(m), obtem_ultima_linha(m) == ('E', 5)

    def test_2(self):
        m = cria_campo('E',5)
        assert campo_para_str(m) == '   ABCDE\n  +-----+\n01|#####|\n02|#####|\n03|#####|\n04|#####|\n05|#####|\n  +-----+'

    def test_3(self):
        m = cria_campo('E',5)

        for l in 'ABC':esconde_mina(obtem_parcela(m, cria_coordenada(l,1)))
        for l in 'BC':esconde_mina(obtem_parcela(m, cria_coordenada(l,2)))
        for l in 'DE':limpa_parcela(obtem_parcela(m, cria_coordenada(l,1)))
        for l in 'AD':limpa_parcela(obtem_parcela(m, cria_coordenada(l,2)))
        for l in 'ABCDE':limpa_parcela(obtem_parcela(m, cria_coordenada(l,3)))

        assert alterna_bandeira(obtem_parcela(m, cria_coordenada('D',4)))

    def test_4(self):
        m = cria_campo('E',5)

        for l in 'ABC':esconde_mina(obtem_parcela(m, cria_coordenada(l,1)))
        for l in 'BC':esconde_mina(obtem_parcela(m, cria_coordenada(l,2)))
        for l in 'DE':limpa_parcela(obtem_parcela(m, cria_coordenada(l,1)))
        for l in 'AD':limpa_parcela(obtem_parcela(m, cria_coordenada(l,2)))
        for l in 'ABCDE':limpa_parcela(obtem_parcela(m, cria_coordenada(l,3)))

        alterna_bandeira(obtem_parcela(m, cria_coordenada('D',4)))

        assert campo_para_str(m) == '   ABCDE\n  +-----+\n01|###2 |\n02|3##2#|\n03|1221 |\n04|###@#|\n05|#####|\n  +-----+'

    def test_5(self):
        m = cria_campo('E',5)

        for l in 'ABC':esconde_mina(obtem_parcela(m, cria_coordenada(l,1)))
        for l in 'BC':esconde_mina(obtem_parcela(m, cria_coordenada(l,2)))
        for l in 'DE':limpa_parcela(obtem_parcela(m, cria_coordenada(l,1)))
        for l in 'AD':limpa_parcela(obtem_parcela(m, cria_coordenada(l,2)))
        for l in 'ABCDE':limpa_parcela(obtem_parcela(m, cria_coordenada(l,3)))

        alterna_bandeira(obtem_parcela(m, cria_coordenada('D',4)))

        assert campo_para_str(limpa_campo(m, cria_coordenada('A', 5))) == '   ABCDE\n  +-----+\n01|###2 |\n02|3##2#|\n03|1221 |\n04|   @ |\n05|     |\n  +-----+'

    def test_6(self):
        m = cria_campo('E',5)
        g = cria_gerador(32, 1)
        c = cria_coordenada('D', 4)
        m = coloca_minas(m, c, g, 2)
        assert tuple(coordenada_para_str(p) for p in obtem_coordenadas(m, 'minadas')) == ('B01', 'C01')

    def test_7(self):
        m = cria_campo('E',5)
        g = cria_gerador(32, 1)
        c = cria_coordenada('D', 4)
        m = coloca_minas(m, c, g, 2)
        assert campo_para_str(limpa_campo(m, c)) == '   ABCDE\n  +-----+\n01|###1 |\n02|1221 |\n03|     |\n04|     |\n05|     |\n  +-----+'


class TestPublicFunAux:
    def test_1(self):
        m = cria_campo('F',6)
        assert not jogo_ganho(m)

    def test_2(self):
        m = cria_campo('F',6)
        g = cria_gerador(32, 2)
        c = cria_coordenada('D', 4)
        m = coloca_minas(m, c, g, 1)
        limpa_campo(m, c)
        assert jogo_ganho(m)

    def test_3(self):
        m = cria_campo('M',5)
        g = cria_gerador(32, 2)
        c = cria_coordenada('G', 3)
        m = coloca_minas(m, c, g, 5)
        assert turno_jogador_mooshak(m, 'L\nG03\n')  == (True, 'Escolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:')

    def test_4(self):
        m = cria_campo('M',5)
        g = cria_gerador(32, 2)
        c = cria_coordenada('G', 3)
        m = coloca_minas(m, c, g, 5)
        turno_jogador_mooshak(m, 'L\nG03\n')
        ref = '   ABCDEFGHIJKLM\n  +-------------+\n01|####1  1###1 |\n02|11111  113#2 |\n03|         2#2 |\n04|         111 |\n05|             |\n  +-------------+'
        assert campo_para_str(m) == ref 

    def test_5(self):
        ref = (True,
 '   [Bandeiras 0/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|##########################|\n02|##########################|\n03|##########################|\n04|##########################|\n05|##########################|\n  +--------------------------+\nEscolha uma coordenada:   [Bandeiras 0/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|#1       1#1   1#1  1#####|\n02|11       2#2   111  111###|\n03|         2#2          1###|\n04|         111          1###|\n05|                      1###|\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|#1       1#1   1#1  1@####|\n02|11       2#2   111  111###|\n03|         2#2          1###|\n04|         111          1###|\n05|                      1###|\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|#1       1#1   1#1  1@1###|\n02|11       2#2   111  111###|\n03|         2#2          1###|\n04|         111          1###|\n05|                      1###|\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|#1       1#1   1#1  1@1   |\n02|11       2#2   111  111   |\n03|         2#2          111 |\n04|         111          1#1 |\n05|                      1#1 |\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|#1       1#1   1#1  1@1   |\n02|11       2#2   111  111   |\n03|         2#2          111 |\n04|         111          1#1 |\n05|                      111 |\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/6]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|#1       111   1#1  1@1   |\n02|11       2#2   111  111   |\n03|         2#2          111 |\n04|         111          1#1 |\n05|                      111 |\n  +--------------------------+\nVITORIA!!!\n')
        assert minas_mooshak('Z', 5, 6, 32, 2, 'M03\nM\nV01\nL\nW01\nL\nX01\nL\nX05\nL\nK01\n') == ref
    
    def test_6(self):
        ref = (False,
 '   [Bandeiras 0/10]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|##########################|\n02|##########################|\n03|##########################|\n04|##########################|\n05|##########################|\n  +--------------------------+\nEscolha uma coordenada:Escolha uma coordenada:   [Bandeiras 0/10]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|        1#1     1#########|\n02| 111    1#1   112#########|\n03| 1#21   111  12###########|\n04| 12#1        1############|\n05|  1#1        1############|\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/10]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|        1#1     1#########|\n02| 111    1#1   112#########|\n03| 1@21   111  12###########|\n04| 12#1        1############|\n05|  1#1        1############|\n  +--------------------------+\nEscolha uma ação, [L]impar ou [M]arcar:Escolha uma coordenada:   [Bandeiras 1/10]\n   ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  +--------------------------+\n01|        1#1     1#########|\n02| 111    1#1   112#########|\n03| 1@21   111  12###########|\n04| 12X1        1############|\n05|  1#1        1############|\n  +--------------------------+\nBOOOOOOOM!!!\n')
        assert minas_mooshak('Z', 5, 10, 32, 15, 'M3\nM03\nM\nC03\nL\nD04\n') == ref

### AUXILIAR CODE NECESSARY TO REPLACE STANDARD INPUT 
class ReplaceStdIn:
    def __init__(self, input_handle):
        self.input = input_handle.split('\n')
        self.line = 0

    def readline(self):
        if len(self.input) == self.line:
            return ''
        result = self.input[self.line]
        self.line += 1
        return result

class ReplaceStdOut:
    def __init__(self):
        self.output = ''

    def write(self, s):
        self.output += s
        return len(s)

    def flush(self):
        return 


def turno_jogador_mooshak(mapa, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = turno_jogador(mapa)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout

def minas_mooshak(ncols, nlins, nminas, dim, seed, input_jogo):
    oldstdin = sys.stdin
    sys.stdin = ReplaceStdIn(input_handle=input_jogo)
    
    oldstdout, newstdout = sys.stdout,  ReplaceStdOut()
    sys.stdout = newstdout

    try:
        res = minas(ncols, nlins, nminas, dim, seed)
        text = newstdout.output
        return res, text
    except ValueError as e:
        raise e
    finally:
        sys.stdin = oldstdin
        sys.stdout = oldstdout

