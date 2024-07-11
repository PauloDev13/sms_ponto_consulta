def mask_cpf(cpf: str) -> str:
    part_1 = cpf[0:3]
    part_2 = cpf[3:6]
    part_3 = cpf[6:9]
    part_4 = cpf[9:11]

    return f'{part_1}.{part_2}.{part_3}-{part_4}'
