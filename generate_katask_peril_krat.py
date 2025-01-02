import sqlite3
import random
def get_everything(cursor, query):
    cursor.execute(query)

    return [row[0] for row in cursor.fetchall()];

def generate_krathsh_katalyma(cursor,db_path):   
    krathseis = get_everything(cursor, 'SELECT kwd_krathshs FROM KRATHSH')
    rv=get_everything(cursor,'select kwd_katal FROM RV')
    krathsh_katalyma_pairs = set()
    pairs = []
    atoma=get_everything(cursor,'''SELECT arithmos_enhlikwn+arithmos_paidiwn
                                FROM KRATHSH''')
    conn=sqlite3.connect('camping_v1.db')
    cursor=conn.cursor()
    cursor.execute('Select kwd_krathshs FROM KRAT_PERILAMB_KATALYM')
    list1=[row[0] for row in cursor.fetchall()]
    cursor.execute('Select kwd_krathshs FROM KRATHSH')
    list2=[row[0] for row in cursor.fetchall()]
    for i in list2:
        if i not in list1:
            list3.append(i)

    for i,j in zip(krathseis,atoma):
            for k in rv: 
                xwrhtikothta=cursor.execute('Select xwrhtikothta FROM RV WHERE kwd_katal=?',(k,)).fetchone()[0]
                print([row[0] for row in cursor.fetchall()])
                if(j==xwrhtikothta and i in list3):
                    pairs.append((
                        i,
                        k
                    ))
                    rv.remove(k)


                    if (i, k) not in krathsh_katalyma_pairs:
                        krathsh_katalyma_pairs.add((i, k))
                        break;
        
    print(pairs)  
    

    cursor.executemany(
       'INSERT INTO "KRAT_PERILAMB_KATALYM" '
       'VALUES (?, ?)',
        pairs
    )
    conn.commit()

def main():
    db_path = "camping_v1.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    generate_krathsh_katalyma(cursor,db_path)

    connection.commit()
    connection.close()
    

    return;

if __name__ == "__main__":
    main()
