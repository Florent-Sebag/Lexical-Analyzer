import sys

to_read1 = open("ret.txt", "r")
to_read2 = open(sys.argv[1], "r")

line = to_read1.readline()
i = 0
diff = False
while (line):
    line2 = to_read2.readline()
    if (line != line2):
        diff = True
        # print("line = " + line + "           res = " + line2)
        # print("diff " + sys.argv[1])
    line = to_read1.readline()
    i += 1

if (diff):
    print("diff " + sys.argv[1])
else:
    print (sys.argv[1] + " -- No diff")
