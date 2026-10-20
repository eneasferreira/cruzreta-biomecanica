"""CRUZRETA — reconstrução tridimensional conforme a planilha.
Execução em Python com: python cruzreta_entrega.py
Para testar outros dados, alterar apenas C1, P1, C2, P2 e REAL abaixo.
"""

# Coordenadas (X, Y, Z) dos dados da planilha.
C1 = (365.8, 211.0, 107.0)
P1 = (0.0, 133.9, 50.9)
C2 = (131.4, 384.8, 151.8)
P2 = (179.4, 0.0, 17.1)
REAL = (159.3, 168.2, 74.9)


def cruzamento(a, b, c, d):
    """Interseção das retas AB e CD em um plano 2D."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    vx, vy = d[0] - c[0], d[1] - c[1]
    determinante = ux * vy - uy * vx
    if abs(determinante) < 1e-10:
        raise ValueError('As retas são paralelas ou coincidentes neste plano.')
    t = ((c[0] - a[0]) * vy - (c[1] - a[1]) * vx) / determinante
    return a[0] + t * ux, a[1] + t * uy


def plano(ponto, indices):
    return tuple(ponto[i] for i in indices)


def main():
    xy = cruzamento(*(plano(p, (0, 1)) for p in (C1, P1, C2, P2)))
    xz = cruzamento(*(plano(p, (0, 2)) for p in (C1, P1, C2, P2)))
    zy = cruzamento(*(plano(p, (2, 1)) for p in (C1, P1, C2, P2)))

    # Mesmo critério da planilha: média das duas estimativas de cada eixo.
    reconstruido = ((xy[0] + xz[0]) / 2,
                    (xy[1] + zy[1]) / 2,
                    (xz[1] + zy[0]) / 2)
    erros = [abs(real - calculado) for real, calculado in zip(REAL, reconstruido)]

    print('CRUZRETA — RECONSTRUÇÃO TRIDIMENSIONAL')
    print('-' * 46)
    print(f'Interseção XY: {xy}')
    print(f'Interseção XZ: {xz}')
    print(f'Interseção ZY: {zy}\n')
    print('Eixo | Reconstruído | Referência | Erro absoluto')
    for eixo, valor, real, erro in zip('XYZ', reconstruido, REAL, erros):
        print(f' {eixo}   | {valor:12.6f} | {real:10.3f} | {erro:12.6f}')
    print(f'\nErro médio absoluto: {sum(erros) / 3:.6f}')
    print('Unidades: as mesmas dos dados de entrada da planilha.')


if __name__ == '__main__':
    try:
        main()
    except ValueError as erro:
        print(f'Não foi possível calcular: {erro}')
