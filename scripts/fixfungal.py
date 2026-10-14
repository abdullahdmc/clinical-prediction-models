import re,os
p=os.environ['TEMP']+'/pm/mine.py'
s=open(p,encoding='utf-8').read()
s=re.sub(r"\('Fungal',r'[^']*'\)", "('Fungal',r'(?<![a-z])candid(a|iasis|emia|aemia)(?![a-z])|fungal|aspergill')", s)
open(p,'w',encoding='utf-8').write(s)
i=s.index("('Fungal'"); print(repr(s[i:i+80]))
