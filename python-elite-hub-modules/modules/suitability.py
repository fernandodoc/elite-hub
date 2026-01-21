class SuitabilityEngine:
    @staticmethod
    def calcular_perfil(respostas):
        """
        Calcula o perfil do investidor com base em pontuação técnica.
        """
        score = sum(respostas)
        
        if score <= 10:
            return {
                "perfil": "CONSERVADOR 🛡️",
                "alocacao": "Prioridade em Liquidez e Renda Fixa Pós-Fixada (Tesouro Selic/CDBs).",
                "cor": "#58a6ff"
            }
        elif score <= 18:
            return {
                "perfil": "MODERADO ⚖️",
                "alocacao": "Equilíbrio entre Renda Fixa e ativos de valor (Fundos Imobiliários e Multimercados).",
                "cor": "#f1e05a"
            }
        else:
            return {
                "perfil": "ARROJADO 🚀",
                "alocacao": "Foco em ganho de capital. Alocação em Ações, Small Caps e Investimentos Internacionais.",
                "cor": "#00ff41"
            }