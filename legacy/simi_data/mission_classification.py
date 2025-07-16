def classificar_missao(texto):
    texto = texto.lower()
    if "agro" in texto or "rural" in texto:
        return "Agroindústria Sustentável"
    elif "saúde" in texto or "biotec" in texto:
        return "Saúde"
    elif "urbano" in texto or "cidade" in texto or "mobilidade" in texto:
        return "Cidades Inteligentes"
    elif "ia" in texto or "automação" in texto or "indústria 4.0" in texto:
        return "Transformação Digital"
    elif "energia" in texto or "carbono" in texto:
        return "Bioeconomia e Transição Energética"
    elif "segurança" in texto or "defesa" in texto:
        return "Defesa e Soberania"
    return "Não Classificado"
