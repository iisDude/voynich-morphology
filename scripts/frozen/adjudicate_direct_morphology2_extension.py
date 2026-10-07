from adjudicate_direct_morphology2_pairs import record
EXTENSION='''1 2 0 1 1 0 0 1 2 2 1 0
1 2 0 1 0 1 1 0 0 2 0 1
0 1 0 1 1 1 0 0 1 0 0 1
0 1 0 1 1 0 1 0 1 1 0 0
1 1 1 1 1 0 0 1 1 0 0 0
0 0 1 1 1 2 0 0 1 1 2 1
0 0 1 1 1 0 2 0 0 0 1 2
0 1 1 0 0 1 0 0 1 2 1 1
1 0 1 1 0 1 0 0 0 0 1 1
1 0 0 0 1 0 0 1 0 0 0 0'''.split()
if __name__=='__main__':
    assert len(EXTENSION)==120
    record(2,EXTENSION,241)
