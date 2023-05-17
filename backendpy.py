
import json
import mysql.connector
from flask import request, redirect

from flask import Flask, render_template

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Samaya#9421",
    database="swarnesh"
)

class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}




class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")
    
    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        
        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1
        
    def dfs(self, node, prefix):
        """Depth-first traversal of the trie
        
        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))
        
        for child in node.children.values():
            self.dfs(child, prefix + node.char)
        
    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of 
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root
        
        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            '''else:
                # cannot found the prefix, return empty list
                return []'''
        
        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)



mycursor=mydb.cursor()
app = Flask(__name__)
loggedUser='User'

@app.route('/')
def index():
    return render_template('homePage.html')

@app.route('/test', methods=['POST'])
def test():
    output=request.get_json()
    result=json.loads(output)
    print(result)
    sql1= "SELECT userid FROM users"
    mycursor.execute(sql1)
    rel1= mycursor.fetchall()
    print(rel1)
    check="false"
    for i in range(0, len(rel1)):
        if (result["user"] == rel1[i][0]):
            check="true"
            break
        else:
            check="false"
    if(check=="false"):
        sql ="INSERT INTO users (name, gender, dob, phone, mail, userid, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (result["name"], result["gender"], result["dob"], result["telp"], result["mail"], result["user"], result["pass"])
        mycursor.execute(sql, val)
        mydb.commit()
        print("inserted")
        return check
    else:
        print("error")
        return check

@app.route('/testAdv', methods=['POST'])
def testAdv():
    output=request.get_json()
    result=json.loads(output)
    print(result)
    sql1= "SELECT userid FROM websiteUser"
    mycursor.execute(sql1)
    rel1= mycursor.fetchall()
    print(rel1)
    check="false"
    for i in range(0, len(rel1)):
        if (result["user"] == rel1[i][0]):
            check="true"
            break
        else:
            check="false"
    if(check=="false"):
        sql ="INSERT INTO websiteUser (name, compName, contact, telNum, mail, userid, password, walletBalance) VALUES (%s, %s, %s, %s, %s, %s, %s,0)"
        val = (result["name"], result["compname"], result["telp"], result["telph"], result["mail"], result["user"], result["pass"])
        mycursor.execute(sql, val)
        mydb.commit()
        print("inserted")
        return check
    else:
        print("error")
        return check

@app.route('/signin')
def signin():
    return render_template('index.html')

@app.route('/signinadv')
def signinadv():
    return render_template('advSignin.html')

@app.route('/signinweb')
def signinweb():
    return render_template('webSignin.html')

@app.route('/signUp')
def signup():
    return render_template('index1.html')

@app.route('/signUpAdv')
def signupadv():
    return render_template('advSignup.html')

t=Trie()
@app.route('/search')
def home():
    sql2="SELECT tag FROM websiteTag"
    mycursor.execute(sql2)
    rel2= mycursor.fetchall()
    print(rel2)
    for i in rel2:
        t.insert(i[0])
    sql="SELECT name FROM users WHERE userid = %s"
    val=(loggedUser,)
    print(val)
    mycursor.execute(sql, val)
    rel=mycursor.fetchall()
    print(rel[0][0])
    sql="SELECT mail FROM users WHERE userid = %s"
    val=(loggedUser,)
    print(val)
    mycursor.execute(sql, val)
    rel1=mycursor.fetchall()
    print(rel1[0][0])
    print(rel[0][0])

    return render_template('searchEngine.html', name=rel[0][0], mail=rel1[0][0])

@app.route('/advDash')
def advDash():
    sql="SELECT * FROM advUser WHERE userid = %s"
    print("start")
    print(loggedUser)
    val=(loggedUser,)

    print(val)
    mycursor.execute(sql, val)
    rel=mycursor.fetchall()
    print(rel)
    print(rel[0][0])
    return render_template('advDash.html', name=rel[0][0],wbalance=rel[0][7])

@app.route('/check', methods=['POST'])
def check():
    output1 =request.get_json()
    result1=json.loads(output1)
    check=0
    print(result1)
    sql="SELECT password FROM users WHERE userid = %s"
    val=(result1["user"],)
    print(val[0])
    mycursor.execute(sql, val)
    rel= mycursor.fetchall()
    print(rel)
    
    print(result1["pass"])
    global loggedUser
    loggedUser=val[0]
    return json.dumps({'user':val[0], 'passent':result1["pass"], 'passcrct':rel[0][0]})
  
@app.route('/checkAdv',methods=['POST'])
def checkAdv():
    output1 =request.get_json()
    result1=json.loads(output1)
    check=0
    print(result1)
    sql="SELECT password FROM advUser WHERE userid = %s"
    val=(result1["user"],)
    print(val[0])
    mycursor.execute(sql, val)
    rel= mycursor.fetchall()
    print(rel)
    print(rel[0][0])
    print(result1["pass"])
    global loggedUser
    loggedUser=val[0]
    return json.dumps({'user':val[0], 'passent':result1["pass"], 'passcrct':rel[0][0]})

@app.route('/checkWeb',methods=['POST'])
def checkWeb():
    output1 =request.get_json()
    result1=json.loads(output1)
    check=0
    print(result1)
    sql="SELECT password FROM websiteUser WHERE userid = %s"
    val=(result1["user"],)
    print(val[0])
    mycursor.execute(sql, val)
    rel= mycursor.fetchall()
    print(rel)
    print(rel[0][0])
    print(result1["pass"])
    global loggedUser
    loggedUser=val[0]
    return json.dumps({'user':val[0], 'passent':result1["pass"], 'passcrct':rel[0][0]})


@app.route('/trie', methods=['POST'])
def trie():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    str1=r['inp']
    print(str1)
    a=t.query(str1)
    print(a)
    b=[]
    for i in a:
        b.append(i[0])
    print(b)
    return json.dumps(b)
    
keyword1='sample'  
@app.route('/webList', methods=['POST'])
def webList():
    get=request.get_json()
    r=json.loads(get)
    print('error')
    print(r)
    keyword=r['tag1']
    global keyword1
    keyword1=keyword
    print(keyword)
    return keyword

@app.route('/displayWebList')
def displayWebList():

    '''sql="SELECT distinct(websiteId) FROM websiteTag WHERE tag = %s"
    val=(keyword1,)
    mycursor.execute(sql, val)
    rel=mycursor.fetchall()
    print(rel)
    list1=[]
    for i in rel:
        list1.append()'''
    return render_template('webList.html',tag1=keyword1)

@app.route('/getWebsiteList', methods=['POST'])
def getWebsiteList():
    sql="SELECT distinct(websiteId) FROM websiteTag WHERE tag = %s"
    val=(keyword1,)
    mycursor.execute(sql, val)
    rel=mycursor.fetchall()
    print(rel)
    list1=[]
    for i in rel:
        sql1="SELECT websiteName, websiteLink, userid, websiteId from webDetails where websiteId = %s"
        val1=(i[0],)
        mycursor.execute(sql1, val1)
        rel1=mycursor.fetchall()
        print(rel1)
        list1.append(rel1[0])
    print(list1)
    return list1
@app.route('/insertWebDetail', methods=['POST'])
def insertWebDetail():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    sql1= "SELECT websiteName FROM webDetails"
    mycursor.execute(sql1)
    rel1= mycursor.fetchall()
    print(rel1)
    check="false"
    for i in range(0, len(rel1)):
        if (r["name"] == rel1[i][0]):
            check="true"
            break
        else:
            check="false"
    if(check=="false"):
        sql="insert into webDetails (userid, websiteLink, websiteName, views)  values(%s,%s,%s,0)"
        val = (loggedUser,r['link'], r['name'])
        mycursor.execute(sql, val)
        mydb.commit()

    return check
@app.route('/insertWebTag', methods=['POST'])
def insertWebTag():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    print(r['tag'])
    val1=[]
    val1.append(r['tag'])
    print(val1)
    val=(r['tag'],)
    mycursor.callproc('insertTag', val)
    mydb.commit()
    return 'true'
@app.route('/withdrawpage')
def withdrawpage():
    return 'amount withdrawn'
@app.route('/webDash')
def webDash():
    sql="SELECT * FROM websiteUser WHERE userid = %s"
    print("start")
    print(loggedUser)
    val=(loggedUser,)

    print(val)
    mycursor.execute(sql, val)
    rel=mycursor.fetchall()
    print(rel)
    print(rel[0][0])
    sql1="SELECT websiteId, websiteLink, websiteName FROM webDetails WHERE userid = %s"
    val1=(loggedUser,)
    mycursor.execute(sql1, val1)
    rel1=mycursor.fetchall()
    print(rel1)
    print(rel1[0][0])
    sql2="SELECT increaseAmt, tranDate from webTransaction  where userid=%s order by tranDate desc";
    val2=(loggedUser,)
    mycursor.execute(sql2, val2)
    rel2=mycursor.fetchall()
    sql3="SELECT websiteId, websiteName, views from webDetails where userid=%s"
    val3=(loggedUser,)
    mycursor.execute(sql3, val3)
    rel3=mycursor.fetchall()
    sql4="SELECT sum(views) from webDetails where userid=%s"
    val4=(loggedUser,)
    mycursor.execute(sql4, val4)
    rel4=mycursor.fetchall()
    print('rel4')
    print(rel4[0][0])
    return render_template('webOwnDash.html', name=rel[0][0],wbalance=rel[0][7], table=rel1, table1=rel2, table2=rel3, total=rel4[0][0])


webOwner='user'
webId=0000
@app.route('/getWebName', methods=['POST'])
def getWebName():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    sql1="SELECT userid FROM webDetails WHERE websiteId = %s"
    val1=(r['ele1'],)
    mycursor.execute(sql1, val1)
    rel1=mycursor.fetchall()
    print("inside rel")
    print(rel1)
    webOwn=rel1[0][0]
    wid=r['ele1']
    global webId
    webId=wid
    global webOwner
    webOwner=webOwn
    print(webOwner)
    return 'true'

@app.route('/openWebsite')
def openWebsite():
    sql ="update webdetails set views=views+1 where websiteId=%s"
    val = (webId,)
    mycursor.execute(sql, val)
    mydb.commit()
    return render_template('dummyWeb.html')

@app.route('/withdraw', methods=['POST'])
def withdrawn():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    val=(r['amt'], loggedUser)
    mycursor.callproc('withdraw', val)
    mydb.commit()
    return 'true'
@app.route('/updateWebDetail', methods=['POST'])
def updateWeb():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    sql ="update webDetails set websiteName =%s, websiteLink=%s where websiteId=%s"
    val = (r['name'], r['link'], r['id'])
    mycursor.execute(sql, val)
    mydb.commit()
    return 'true'

@app.route('/upWallet')
def upWallet():
    sql ="update websiteUser set walletBalance=walletBalance+200 where userid=%s"
    val = (webOwner,)
    mycursor.execute(sql, val)
    mydb.commit()
    return 'Advertisement'

@app.route('/removeWeb', methods=['POST'])
def removeWeb():
    get=request.get_json()
    r=json.loads(get)
    print(r)
    print(r['id'])
    val=(r['id'],)
    mycursor.callproc('deleteWeb', val)
    mydb.commit()
    return 'true'
app.run(debug=True)