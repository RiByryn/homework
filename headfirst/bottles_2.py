# _*_ coding: cp1251 _*_
word = "�������"
for beer_num in range(99, 0, -1):
    print(beer_num, word, "���� �� �����.")
    print(beer_num, word, "����.")
    print("������ ����.")
    print("����� �� �����.")
    if beer_num == 1:
        print("��� ������� ���� �� �����!")
    else:
        new_num = beer_num - 1
        if new_num >= 11 and new_num <= 19:
            word = "�������"
        else:
            if new_num % 10 == 1:
                word = "�������"
            elif new_num % 10 in (2, 3, 4):
                word = "�������"
            else:
                word = "�������"
        print(new_num, word, "���� �� �����.")
    print()