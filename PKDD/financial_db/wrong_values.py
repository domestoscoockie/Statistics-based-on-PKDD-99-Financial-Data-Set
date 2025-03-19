# Zdefiniuj mapowania specyficzne dla kolumn i tabel
column_specific_replacements = {
    # Tabela Trans
    'Trans': {
        'operation': {
            'PRIJEM': 'credit',
            'VYDAJ': 'withdrawal',
            'VKLAD': 'credit in cash',
            'VYBER KARTOU': 'withdrawal card',
            'PREVOD NA UCET': 'remittance to another bank',
            'VYBER': 'withdrawal in cash',
            'PREVOD Z UCTU': 'collection from another bank'
        },
        'k_symbol': {
            'SIPO': 'household',
            'UVER': 'loan',
            'LEASING': 'leasing',
            'POJISTNE': 'insurance'
        }
    },
    
    # Tabela Loan
    'Loan': {
        'status': {
            'A': 'contract finished, no problems',
            'B': 'contract finished, loan not payed',
            'C': 'running contract, OK so far',
            'D': 'running contract, client in debt'
        }
    },
    
    # Tabela Account
    'Account': {
        'frequency': {
            'POPLATEK MESICNE': 'monthly issuance',
            'POPLATEK TYDNE': 'weekly issuance',
            'POPLATEK PO OBRATU': 'issuance after transaction'
        }
    },
    
    # Tabela Card
    'Card': {
        'type': {
            'classic': 'Classic',
            'junior': 'Junior',
            'gold': 'Gold'
        }
    }
}

# Ogólne wartości do zastąpienia dla wszystkich kolumn
global_replacements = {'?': None, '': None, ' ': None}