# http://filebox.vt.edu/users/batman/kryptos.html
def decrypt_kryptos1(table, encrypted):
    text = ''
    for i in range(0, len(encrypted)):
        ec = encrypted[i]
        rowi = i % (len(table) - 1)
        eci = table[rowi + 1].find(ec)
        d = table[0][eci]
        text = text + d
    return text    


def prepare_table(key1, key2):
    rows = []
    row = key1
    for n in range(ord('A'), ord('Z') + 1):
        if key1.find(chr(n)) == -1:
            row = row + chr(n)
    rows.append(row)
    #print (row)
    
    for i in range(0, len(key2)):
        c = key2[i]
        ci = rows[0].find(c)
        row = rows[0][ci:]+rows[0][:ci]
        
        rows.append(row)
        #print(row)
    
    return rows  


with open("/home/kali/Projects/Hacking/kryptos/kryptos1.txt", "rt") as file:
    encrypted = file.read()
    print(encrypted)
    

table = prepare_table('KRYPTOS', 'PALIMPSEST')
#print(table)
text = decrypt_kryptos1(table, encrypted)

print (text)            
