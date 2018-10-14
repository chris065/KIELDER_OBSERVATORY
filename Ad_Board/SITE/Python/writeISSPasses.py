import json, requests

def formatJson():
    passesData = ""
    count = 0
    with open("ISSPasses.json", "r") as read_file:
        passes = json.load(read_file)
        for line in (passes["passes"]):
                print(count)
                if count > 2:
                    break
                else:
                    passesData = passesData + "<tr><td>"+str(line["tStart"])+ "</td>" + "<td>"+ str(line["mag"]) +"</td>"+"<td>"+str(line["dStart"])+"</td>"+"<td>"+str(line["desc"])+"</td></tr>"
                count = count + 1
    return passesData

def writeToTextFile():
    file = open("ISSPassesTable.txt", "w+")
    file.write(formatJson())
    file.close()

def main():
    writeToTextFile()

main()
