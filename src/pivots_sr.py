"""Pivot and support/resistance context."""

def pivot_levels(df):
    r=df.iloc[-1]
    p=(r.high+r.low+r.close)/3
    return {"pivot":p,"r1":2*p-r.low,"s1":2*p-r.high,"r2":p+(r.high-r.low),"s2":p-(r.high-r.low)}


def sr_score(df, tolerance=0.002):
    if len(df)<10: return 0
    price=float(df.close.iloc[-1]); levels=[]
    for i in range(max(0,len(df)-50),len(df)-1):
        levels += [float(df.high.iloc[i]), float(df.low.iloc[i])]
    near=[x for x in levels if abs(x-price)/price<=tolerance]
    if not near: return 0
    return 1 if price>=max(near) else -1
