import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


# Created Dictionary , Which will help in calculating CGPA of individual Student
gradingSystem = {
    'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 5, 'E': 4
}
# College Website Result Login Page  [http://results.jssstuniv.in/]
url = 'http://results.jssstuniv.in/check.php'  # [This Page will be available If you entered valid USN]
n = int(input('Number Of Students : '))  # Taking Number OF Students
usn = ''
totalResult = dict()
for student in range(1, n+1):  # Creating USNs for students It varies from Branch to Branch
    if student < 10:
        usn = '01JST17CS00' + str(student)
        print(usn)
    elif 10 <= student < 100:
        usn = '01JST17CS0' + str(student)
        print(usn)
    elif student >= 100:
        usn = '01JST17CS' + str(student)
        print(usn)
    values = {'USN': usn}
    try:
        data = urllib.parse.urlencode(values)
        data = data.encode('utf-8')  # data should be bytes
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        dataAvailabilty = 1
    except Exception as e:
        print('Failed To Fetch The data')
        dataAvailabilty = 0

    if dataAvailabilty == 1:
        soup = BeautifulSoup(the_page, 'html5lib')  # Using this You can webscrap and get the whatever data you want from webpage.
        # from next , code may not suit to your url
        # print(soup.prettify())  # This will print the obtained HTML page in a readable fashion.
        try:
            res1 = soup.find('div', class_='result1') # Required Data is present in class Result
            name = res1.find('h1').text   # <h1>Sharath Champzz</h1>
            usn = res1.find('h2').text  # <h2>01JST17EC086</h2>
            found = 1
        except Exception as e:
            print('Failed To acess Student name ')
            found  = 0

        # Proceeding Only If No error Occured Above i.e only for condition found = 1
        if found == 1:
            table = res1.find('tbody')
            result = dict()
            for tr in table.findAll('tr'):
                i = 0
                key = ""
                val = ""
                for x in tr.findAll('td'):
                    i += 1
                    if i == 2:
                        key = x.text
                    elif i == 3:
                        val = x.text
                        result[key] = val
            # print(result)
            gradval = []
            permissionForDisplay = 1
            for grade in result.values():
                Grad = grade.lstrip().rstrip()
                x = gradingSystem.get(Grad, 0)
                if x != 0:
                    gradval.append(x)
                else:
                    permissionForDisplay = 0
                    break
            if permissionForDisplay == 1:
                summ = 0
                add = 0
            # Change next lines depending on branches
                noOfSubjects = 6
                for i in range(0, noOfSubjects):
                    if i == 0 or i == 3:
                        add = gradval[i] * 4
                        # print('Mutiplying With 4')
                    else:
                        add = gradval[i] * 5
                        # print('Mutiplying With 5')
                    # print('Adding', add)
                    summ = summ + add
                    # print(summ)
                sgpa = summ / 28
                sgpa = round(sgpa, 2)
                print(name, ' : ', usn, ': ', sgpa)
                totalResult[name] = sgpa

            elif permissionForDisplay == 0:
                print('Sorry Your Result Cant Be displayed')

print(totalResult)

Ranking = sorted(totalResult, key=totalResult.get, reverse=True)
rank = 0
# Saving the Output in .txt file
with open("CSRanking.txt", "a") as myfile:
    for r in Ranking:
        rank += 1
        print(r, totalResult[r])
        displayingAs = str(rank) + ' : ' + r + ' - ' + str(totalResult[r]) + '\n'
        print('Writing : ', displayingAs)
        myfile.write(displayingAs)
