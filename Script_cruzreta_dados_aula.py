"""Cruzreta: Script com as medidas da aula (metros).
Reproduz o método da planilha: cruzamentos nos planos XY, XZ e ZY,
seguidos da média das duas estimativas de cada coordenada.
Executar: python Script_cruzreta_dados_aula.py
"""

C1 = (5.030, 5.663, 0.904)
C2 = (4.640, 1.860, 1.013)
P1 = (0.000, 1.446, 1.026)
P2 = (2.013, 7.032, 0.805)
REAL = (3.440, 4.330, 0.939)  # Medições com laser, conforme anotações da aula


def cruzamento(a, b, c, d):
    """Interseção das retas AB e CD projetadas em duas dimensões."""
    ux, uy = b[0] - a[0], b[1] - a[1]
    vx, vy = d[0] - c[0], d[1] - c[1]
    det = ux * vy - uy * vx
    if abs(det) < 1e-12:
        raise ValueError("Retas paralelas ou coincidentes neste plano.")
    t = ((c[0] - a[0]) * vy - (c[1] - a[1]) * vx) / det
    return a[0] + t * ux, a[1] + t * uy


def projetar(ponto, eixos):
    return tuple(ponto[i] for i in eixos)


def calcular():
    pontos = (C1, P1, C2, P2)
    xy = cruzamento(*(projetar(p, (0, 1)) for p in pontos))
    xz = cruzamento(*(projetar(p, (0, 2)) for p in pontos))
    zy = cruzamento(*(projetar(p, (2, 1)) for p in pontos))
    reconstruido = ((xy[0] + xz[0]) / 2,
                    (xy[1] + zy[1]) / 2,
                    (xz[1] + zy[0]) / 2)
    erros = [abs(a - b) for a, b in zip(reconstruido, REAL)]

    print("CRUZRETA — DADOS MEDIDOS EM AULA (metros)")
    print("Interseção XY:", tuple(round(v, 6) for v in xy))
    print("Interseção XZ:", tuple(round(v, 6) for v in xz))
    print("Interseção ZY:", tuple(round(v, 6) for v in zy))
    print("\nEixo | Reconstruído (m) | Laser (m) | Erro absoluto (m)")
    for eixo, valor, real, erro in zip("XYZ", reconstruido, REAL, erros):
        print(f" {eixo}   | {valor:16.6f} | {real:9.3f} | {erro:16.6f}")
    print(f"\nErro médio absoluto das coordenadas: {sum(erros)/3:.6f} m")
    print("OBS.: Método de médias da planilha, não triangulação 3D por mínimos quadrados.")
    print("As projeções em diferentes planos podem não coincidir em um único ponto.")


if __name__ == "__main__":
    try:
        calcular()
    except ValueError as exc:
        print("Não foi possível calcular:", exc)
