import sys,re; sys.stdout.reconfigure(encoding='utf-8')
kw=re.compile(sys.argv[1],re.I)
for f in sys.argv[2:]:
    t=open(f'build/src/pmc/{f}.txt',encoding='utf-8').read()
    print('#########',f,t.split('\n')[0][:120])
    for blk in t.split('\n=== ')[1:]:
        cap=blk.split('\n')[0]
        if kw.search(cap): print('=== '+'\n'.join(l[:260] for l in blk.split('\n')[:int(sys.argv[0] and 40)]))
