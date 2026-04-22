import generar_sbox as ge
import fitness     as fo
import complementoAG as ga
import random

def main():

    TAMANO_POBLACION = 100
    GENERACIONES     = 100
    PROB_CRUCE       = 0.85
    PROB_MUTACION    = 0.3

    print("\n" + "=" * 95)
    print("   ----------------GA HÍBRIDO — 9 MÉTRICAS----------")
    print("=" * 95)

    poblacion  = ge.crear_poblacion_inicial(TAMANO_POBLACION)
    resultados = [fo.consultar_fitness(ind) for ind in poblacion]

    def extraer(res):
        return {
            "score": res[0], "nl": res[1], "dsac": res[2],
            "du": res[3],    "bn": res[4], "ciclos": res[5],
            "min_ciclo": res[6], "ls": res[7], "lp": res[8],
            "paso": res[9]
        }

    datos = [extraer(r) for r in resultados]

    print(f"\n{'GEN':<5} | {'SCORE':<7} | {'NL':<4} | {'DSAC':<5} | {'DU':<4} | "
          f"{'BN':<3} | {'CICLOS':<6} | {'MINCIC':<6} | {'LS':<3} | {'LP':<9} | {'FILTRO':<6} | {'DIV'}")
    print("-" * 100)

    mejor_global       = None
    mejor_score_global = -float('inf')

    for gen in range(GENERACIONES):

        scores = [d["score"] for d in datos]
        mejor_idx = scores.index(max(scores))

        if scores[mejor_idx] > mejor_score_global:
            mejor_score_global = scores[mejor_idx]
            mejor_global       = poblacion[mejor_idx][:]

        nueva_poblacion = [poblacion[mejor_idx][:]]

        while len(nueva_poblacion) < TAMANO_POBLACION:
            p1 = ga.seleccion_torneo(poblacion, scores, k=3)
            p2 = ga.seleccion_torneo(poblacion, scores, k=3)

            if random.random() < PROB_CRUCE:
                h1, h2 = ga.aplicar_cx(p1, p2)
            else:
                h1, h2 = p1[:], p2[:]

            if random.random() < PROB_MUTACION:
                h1 = ga.aplicar_scramble(h1)
            if random.random() < PROB_MUTACION:
                h2 = ga.aplicar_scramble(h2)

            nueva_poblacion.append(h1)
            if len(nueva_poblacion) < TAMANO_POBLACION:
                nueva_poblacion.append(h2)

        poblacion  = nueva_poblacion
        resultados = [fo.consultar_fitness(ind) for ind in poblacion]
        datos      = [extraer(r) for r in resultados]
        scores     = [d["score"] for d in datos]

        mejor_idx  = scores.index(max(scores))
        m          = datos[mejor_idx]
        diversidad = len(set(tuple(i) for i in poblacion))
        paso_str   = "SI" if m["paso"] else "NO"
        ls_str     = "SI" if m["ls"] else "NO"

        if scores[mejor_idx] > mejor_score_global:
            mejor_score_global = scores[mejor_idx]
            mejor_global       = poblacion[mejor_idx][:]

        print(f"{gen:<5} | {m['score']:<7.1f} | {m['nl']:<4} | {m['dsac']:<5} | "
              f"{m['du']:<4} | {m['bn']:<3} | {m['ciclos']:<6} | {m['min_ciclo']:<6} | "
              f"{ls_str:<3} | {m['lp']:<9.6f} | {paso_str:<6} | {diversidad}/{TAMANO_POBLACION}")

    with open("sbox_para_aco.txt", "w") as f:
        f.write(" ".join(mejor_global))

    print("\n" + "=" * 95)
    print(f"  Mejor S-box guardada en sbox_para_aco.txt (formato hex)")
    print(f"  Score final: {mejor_score_global:.1f}")
    print("=" * 95)

if __name__ == "__main__":
    main()
