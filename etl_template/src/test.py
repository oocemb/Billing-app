a = {}
a["key1"] = "value0"


def A(dic):
    dic["key1"] = "VALUE1"


def B(dic):
    dic["key2"] = "VALUE2"


def C(dic):
    dic["key3"] = "VALUE4"


A(a)
B(a)
C(a)

print(a)
