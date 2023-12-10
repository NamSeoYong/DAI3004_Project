from difflib import SequenceMatcher

# file은 txt파일 넣어야 함
def similar(file_a, file_b):
    with open(file_a, "r", encoding="utf-8") as a:
        A = a.read()
    with open(file_b, "r", encoding="utf-8") as b:
        B = b.read()
        similarity = round(float(SequenceMatcher(None, A, B).ratio()), 2) * 100
        
    with open('text/result.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(str(similarity))    
    
    print(similarity)
    
    return similarity


cc = ''
with open('text/click.txt', "r", encoding="utf-8") as a:
        cc = a.read()
        
        
if (cc == 'A'):
    similar('text/A.txt', 'text/output.txt')
elif (cc == 'B'):
    similar('text/B.txt', 'text/output.txt')
elif (cc == 'C'):
    similar('text/C.txt', 'text/output.txt')


print("Text saved to: re.txt")
