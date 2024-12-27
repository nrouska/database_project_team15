import numpy as np
import sqlite3
conn = sqlite3.connect('camping_v2.db')
cursor=conn.cursor()
selectquery="select strftime('%Y',hmer_afixhs),count(*) from KRATHSH GROUP BY strftime('%Y',hmer_afixhs)"
cursor.execute(selectquery)
records=cursor.fetchall()
selectquery1="SELECT strftime('%Y',hmer_afixhs),K.kwd_krathshs,((arithmos_paidiwn*7)+(arithmos_enhlikwn*10)+XK.kostos)*(julianday(hmer_anaxwrhshs)-julianday(hmer_afixhs))FROM XWROS_KATASKHNWSHS as XK NATURAL JOIN KATALYMA NATURAL JOIN KRAT_PERILAMB_KATALYM NATURAL JOIN KRATHSH as K JOIN YPHRESIA as Y JOIN KRAT_EPILE_YPHR GROUP BY strftime('%Y',hmer_afixhs),K.kwd_krathshs"
cursor.execute(selectquery1)
records1=cursor.fetchall()
selectquery2="SELECT strftime('%Y',hmer_afixhs),K.kwd_krathshs,((arithmos_paidiwn*7)+(arithmos_enhlikwn*10)+XK.kostos)*(julianday(hmer_anaxwrhshs)-julianday(hmer_afixhs))FROM DWMATIO as XK NATURAL JOIN KATALYMA NATURAL JOIN KRAT_PERILAMB_KATALYM NATURAL JOIN KRATHSH as K JOIN YPHRESIA as Y JOIN KRAT_EPILE_YPHR GROUP BY strftime('%Y',hmer_afixhs),K.kwd_krathshs"
cursor.execute(selectquery2)
records2=cursor.fetchall()
selectquery3="SELECT strftime('%Y',hmer_afixhs),K.kwd_krathshs,((arithmos_paidiwn*7)+(arithmos_enhlikwn*10)+XK.kostos)*(julianday(hmer_anaxwrhshs)-julianday(hmer_afixhs))FROM RV as XK NATURAL JOIN KATALYMA NATURAL JOIN KRAT_PERILAMB_KATALYM NATURAL JOIN KRATHSH as K JOIN YPHRESIA as Y JOIN KRAT_EPILE_YPHR GROUP BY strftime('%Y',hmer_afixhs),K.kwd_krathshs"
cursor.execute(selectquery3)
records3=cursor.fetchall()
selectquery4="SELECT strftime('%Y',hmer_afixhs),avg(vathmologia) FROM KRATHSH natural JOIN AXIOLOGHSH GROUP BY strftime('%Y',hmer_afixhs)"
cursor.execute(selectquery4)
records4=cursor.fetchall()

conn.close()