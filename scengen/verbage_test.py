import verbage as v

test = v.verbage()

testdata= {"ModA":[],"ModB":[],"ModC":["ModG"],"ModD":[],"ModE":["ModA","ModB","ModC"],"ModF":["ModA"],"ModG":["ModF"],"ModH":["ModC","ModD"]}

test.stuff_assoc=testdata

print test.getModelOutputOrder()