import pandas as pd
values_to_change = {'?':None, pd.NA: None, '':None, ' ':None,
                    "POPLATEK MESICNE":'monthly issuance',
                    'POPLATEK TYDNE':'weekly issuance',
                    'POPLATEK PO OBRATU':'issuance after transaction',

                    'PRIJEM':'credit',
                    'VYDAJ':'withdrawal', 
                    'VKLAD':'credit in cash',

                    'VYBER KARTOU':'withdrawal card',
                    'PREVOD NA UCET':'remittance to another bank',
                    'VYBER':'withdrawal in cash',
                    'PREVOD Z UCTU':'collection from another bank',

                    'SIPO':'household',
                    'UVER':'loan',
                    'LEASING':'leasing',
                    'POJISTNE':'insurance',

                    'A':'contract finished, no problems',
                    'B':' contract finished, loan not payed',
                    'C':' running contract, OK so far',
                    'D':' running contract, client in debt',

                    }