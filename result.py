
def create() -> list:
    rtrn = []
    for i in range(0, 96):
        
        rtrn.append({
            "left": 0,
            "right": 0,
            "jump": 0,
        })

    return rtrn

def load() -> list:
    f = open("resultado.txt", "r")
    s = f.read()
    f.close()

    rtrn = []
    for line in s.split('\n'):
        split = line.split(' ')
        if len(split) < 3:
            continue
        
        rtrn.append({
            "left": float(split[0]),
            "right": float(split[1]),
            "jump": float(split[2]),
        })
    
    if len(rtrn) != 96:
        print(f"Esperado: (96) estados. Lidos: ({len(rtrn)}) estados.\nArquivo foi carregado com ({len(rtrn)}) estados.")

    return rtrn

def save(result: list) -> None:

    if len(result) != 96:
        print(f"Esperado: (96) estados. Recebido: ({len(result)}) estados.\nArquivo foi salvo com ({len(result)}) estados.")


    s = ""
    for state in result:
        s += "{0} {1} {2}\n".format(
            '{0:.6f}'.format(state['left']),
            '{0:.6f}'.format(state['right']),
            '{0:.6f}'.format(state['jump']))

    f = open("resultado.txt", "w")
    f.write(s)
    f.close()
    return 0