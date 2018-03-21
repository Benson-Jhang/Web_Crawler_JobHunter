import re

# '-' 一定在中括號裡面 (單一字元)
str = 'abc1234'
print(re.search(r'[a-c0-4]', str), '#1')
# '[]' 整個中括號代表一個字元，裡面的內容就是這個字元的所有可能 (單一字元)
print(re.search('a[a-c]c', str), '#2')
# '^' 在中括號[]中表示「相反」或「非」的意  (單一字元)
print(re.search('a[^d-e]c', str), '#3')
print(re.search('a[ayz]c', str), '#4')  # a 或 y 或 z
s = 'a-baaa'
print(re.search('[a\-z]b', s), '#s')     # a 或 \ 或 z

# '.'匹配任何字符  (位置)
str1 = 'abc1234'
print(re.search('a.c', str1), '#5')
# '^'匹配輸入字串的開始位置行首，在中括號外  (位置)
print(re.search('^ab', str1), '#6')

# '$'匹配輸入字串的結束位置，行尾 (位置)
print(re.search('34$', str1), '#7')

# 重複字元不會自己獨立出現前面一定有一個真正被比對的字元
# '*'匹配零次到任何次數 (重複)
str3 = 'ton'
print(re.search('ton.*', str3), '#8')

# '+'匹配至少一次到任何次數 (重複)
str4 = 'abcc1234'
print(re.search('a.c+', str4), '#9')

# '?'匹配零次或一次 (重複)
str5 = 'abc1234'
print(re.search('ab?3', str5), '#10')
print(re.search('b?3', str5), '#11')

# {n}固定次數 {n,m}最少n次，最大m次 {n, } 最少n次，到比n次大的任何次數
str6 = 'abbc1234'
print(re.search('ab{3}c', str6), '#12')
print(re.search('ab{1,3}c', str6), '#13')

# '\'跳說字元
str7 = 'abb+1234'
print(re.search('b\+', str7), '#14')

# '()'小括號裡面是多個字元，包括文字、位置(句點)、中括號(單一字元)  (Group)
str8 = 'abb1234'
print(re.search('(abb|bcc)1234', str8), '#15')
print(re.search('(ab|bcc)1234', str8), '#16')

str9 = 'aa<div>test1</div>bb<div>test2</div>cc'
print(re.search(r'<div>.*</div>', str9), '#17')  # greedy
print(re.search(r'<div>.*?</div>', str9), '#18')  # non-greedy

# 'compile' 編譯成Pattern的物件
pattern = re.compile(r'<div>.*</div>')  # pattern object
print(pattern.search(str9), '#19')
# 'findall' 以列表形式返回全部能匹配的子串，如果没有匹配，则返回一个空列表。
print(pattern.findall(str9), '#20')

# 'Search' 方法用于查找字符串的任何位置，它也是一次匹配，只要找到了一个匹配的结果就返回
# 'Match'  方法用于查找字符串的头部（也可以指定起始位置），它是一次匹配，只要找到了一个匹配的结果就返回
str9 = 'I am Benson Chang'
pattern = re.compile(r'(am+).*(chang+)', re.I)
print(pattern.search(str9), '#21')
print(pattern.match(str9), '#22')

str10 = 'I am Big Engineer Data a scientist'
pattern = re.compile(r'.*(big).*\s*(data|scientist)', re.I)
print(pattern.search(str10), '#23')

str11 = '大數據分析師'
pattern = re.compile(r'(數據|大數據)')
print(pattern.search(str11), '#24')

str12 = ''' 不拘
其他條件：
• Master's/Bachelor's Degree in Electrical/Electronics/Microelectronics/Semiconductor/IC Design/Computing. 
• Good knowledge in programming and statistics. 
 *請事先填畢台灣美光應徵人員資料表(於104＂面試須知＂連結下載檔案)，並於面試當日攜帶紙本應試。

公司福利'''
print(re.search(r"(其他條件.*).*(公司)", str12, re.DOTALL).group(1), '#25')

# 參考資料來源:
# http://blog.roodo.com/greenroad/archives/16434449.html
# http://zwindr.blogspot.tw/2016/01/python-regular-expression.html
# http://wiki.jikexueyuan.com/project/explore-python/Regular-Expressions/re.html
