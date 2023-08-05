def data_trans(datajson,col,datavaltran):
    try:
      datajson[col] = datavaltran.get(str(datajson[col]))
    except KeyError:
        datajson
    return datajson