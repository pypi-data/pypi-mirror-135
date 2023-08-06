"""Timing SCPI Commands Example"""
import timeit
from rssd.instrument        import instr

🤖 = instr().open('192.168.58.109')
🤖.timeout(1)

def timeQuery(SCPI):
    tick = timeit.default_timer()
    rdStr = 🤖.query(SCPI)
    TotTime = timeit.default_timer() - tick
    outStr = f'{TotTime*1000:.3f}mSec,{rdStr}'
    return outStr

print(timeQuery('*IDN?'))
# print(timeQuery(':SENS:FREQ:CENT 24e9;*OPC?'))
# print(timeQuery(':INIT:IMM;*OPC?'))

🤖.close()
