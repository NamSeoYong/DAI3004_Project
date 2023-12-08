from difflib import SequenceMatcher

# file은 txt파일 넣어야 함
def similar(file_a, file_b):
    with open(file_a, "r", encoding="utf-8") as a:
        A = a.read()
    with open(file_b, "r", encoding="utf-8") as b:
        B = b.read()
        similarity = round(float(SequenceMatcher(None, A, B).ratio()), 2) * 100
    return similarity
