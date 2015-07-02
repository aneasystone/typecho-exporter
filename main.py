# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 16:45:03 2015

@author: aneasystone
"""

# https://pypi.python.org/pypi/MySQL-python/1.2.5
import MySQLdb

import os
import codecs

class Post(object):
    pass

class Config():
    
    host = 'localhost'
    user = 'root'
    pwd = ''
    port = 3306
    db = 'typecho_db'

    def __init__(self):
        
        ini = open('config.ini', 'r')
        lines = ini.readlines()
        ini.close()
        for line in lines:
            if not line:
                continue
            self.parse_line(line)
        
    def parse_line(self, line):

        parts = line.split('=')
        if 2 != len(parts):
            return
            
        #print line
        key = parts[0].strip()
        value = parts[1].strip()
        if key == 'host':
            self.host = value
        elif key == 'user':
            self.user = value
        elif key == 'pwd':
            self.pwd = value
        elif key == 'port':
            if value:
                self.port = int(3306)
        elif key == 'db':
            self.db = value
    

def get_all_posts():
    
    posts = []    
    try:
        configs = Config()
        conn = MySQLdb.connect(host=configs.host,user=configs.user,passwd=configs.pwd,port=configs.port,charset='utf8')
        cur = conn.cursor()
        conn.select_db(configs.db)
 
        count = cur.execute('select * from typecho_contents')
        print 'there has %s posts' % count
    
        print '==' * 10
    
        results = cur.fetchall()
        for r in results:
            p = Post()
            p.id = r[0]
            p.title = r[1]
            p.content = r[5]
            posts.append(p)
            
        conn.commit()
        cur.close()
        conn.close()
            
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return posts
                

def save_posts(posts):
    
    for p in posts:
        if p.content:
            save_post(p)
            
    return

def save_post(post):
    
    # save to html file
    name = 'files/' + post.title
    if post.content.startswith('<!--markdown-->'):
        name += '.md'
    else:
        name += '.html'
        
    t = codecs.open(name, 'wb', 'utf-8');
    t.write(post.content)
    t.close()

    return
    
def main():
    
    if not os.path.exists('files'):
        os.makedirs('files')    
    
    posts = get_all_posts()
    save_posts(posts)

    return
    
if __name__ == '__main__':
    main()