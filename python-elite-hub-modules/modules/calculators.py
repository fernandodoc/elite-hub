import pandas as pd
import numpy as np

class WealthCalculator:
    @staticmethod
    def juros_compostos_avancado(principal, aporte_mensal, taxa_anual, anos, inflacao_anual):
        """
        Calcula a projeção de crescimento patrimonial com inflação e juros compostos.
        """
        meses = anos * 12
        taxa_mensal = (1 + taxa_anual)**(1/12) - 1
        taxa_inflacao_mensal = (1 + inflacao_anual)**(1/12) - 1
        
        dados = []
        saldo_nominal = principal
        
        for mes in range(1, meses + 1):
            # Cálculo do saldo com aportes e juros
            saldo_nominal = (saldo_nominal + aporte_mensal) * (1 + taxa_mensal)
            
            # Valor Real (Poder de compra descontado pela inflação)
            poder_compra_real = saldo_nominal / ((1 + taxa_inflacao_mensal) ** mes)
            
            total_aportado = principal + (aporte_mensal * mes)
            juros_acumulados = saldo_nominal - total_aportado
            
            dados.append({
                "Mês": mes,
                "Saldo Nominal (R$)": round(saldo_nominal, 2),
                "Poder de Compra (R$)": round(poder_compra_real, 2),
                "Total Aportado (R$)": round(total_aportado, 2),
                "Juros Acumulados (R$)": round(juros_acumulados, 2)
            })
            
        return pd.DataFrame(dados)