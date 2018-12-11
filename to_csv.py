import json
import sys
import os
import xmltodict
import csv
from os.path import join
from utils import *
import shutil

PATH = sys.argv[1]
DIR = PATH.replace('extracted/', '')

print("importing", DIR)

file = join(PATH, 'Posts.xml')


def clean(x):
    # neo4j-import doesn't support: multiline (coming soon), quotes next to each other and escape quotes with '\""'
    return x.replace('\n', '').replace('\r', '').replace('\\', '').replace('"', '')


def open_csv(name):
    return csv.writer(open('csvs/{}.csv'.format(name), 'w', encoding='utf-8'), doublequote=False, escapechar='\\')


try:
    shutil.rmtree('csvs/')
except:
    pass
os.mkdir('csvs')

posts = open_csv('posts')
posts_rel = open_csv('posts_rel')

users = open_csv('users')
users_posts_rel = open_csv('users_posts_rel')

votes = open_csv('votes')
votes_users_rel = open_csv('votes_users_rel')
votes_posts_rel = open_csv('votes_posts_rel')

comments = open_csv('comments')
comments_users_rel = open_csv('comments_users_rel')
comments_posts_rel = open_csv('comments_posts_rel')

posts_things = ['posttypeid', 'acceptedanswerid', 'creationdate', 'deletiondate', 'score', 'viewcount', 'body',
                'ownerdisplayname', 'lasteditoruserid', 'lasteditordisplayname', 'lasteditdate', 'lastactivitydate',
                'title', 'answercount', 'commentcount', 'favoritecount', 'closeddate', 'communityowneddate']
posts.writerow(['postId:ID(Post)'] + posts_things)
posts_rel.writerow([':START_ID(Post)', ':END_ID(Post)'])

users_things = ['reputation', 'creationdate', 'displayname', 'lastaccessdate', 'websiteurl', 'location', 'profileimageurl', 'aboutme',
                'views', 'upvotes', 'downvotes', 'age', 'accountid', 'emailhash']
users.writerow(['userId:ID(User)'] + users_things)
users_posts_rel.writerow([':START_ID(User)', ':END_ID(Post)'])

votes_things = ['votetypeid', 'creationdate', 'bountyamount']
votes.writerow(['voteId:ID(Vote)'] + votes_things)
votes_users_rel.writerow([':START_ID(User)', ':END_ID(Vote)'])
votes_posts_rel.writerow([':START_ID(Post)', ':END_ID(Vote)'])

comments_things = ['score', 'text', 'creationdate', 'userdisplayname']
comments.writerow(['commentId:ID(Comment)'] + comments_things)
comments_users_rel.writerow([':START_ID(User)', ':END_ID(Comment)'])
comments_posts_rel.writerow([':START_ID(Post)', ':END_ID(Comment)'])

for i, line in enumerate(open(file, encoding='utf8')):
    line = line.strip()
    try:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            row = [el['id'], ]
            for k in posts_things:
                row.append(clean(el.get(k, '')))
            posts.writerow(row)
            if el.get('parentid'):
                posts_rel.writerow([el['parentid'], el['id']])
            if el.get('owneruserid'):
                users_posts_rel.writerow([el['owneruserid'], el['id']])
            if el.get('tags'):
                eltags = [x.replace('<', '') for x in el.get('tags').split('>')]
                # for tag in [x for x in eltags if x]:
                #     tags_posts_rel.writerow([el['id'], tag])
    except Exception as e:
        print('x', e)
    if i and i % 100000 == 0:
        print('.', end='')
    if i and i % 1000000 == 0:
        print(i)

print(i, 'posts ok')

file = join(PATH, 'Users.xml')

for i, line in enumerate(open(file, encoding='utf-8')):
    line = line.strip()
    try:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            row = [el['id'], ]
            for k in users_things:
                row.append(clean(el.get(k, '')))
            users.writerow(row)
    except Exception as e:
        print('x', e)
    if i % 100000 == 0:
        print('.', end='')

print(i, 'users ok')

file = join(PATH, 'Votes.xml')

for i, line in enumerate(open(file, encoding='utf-8')):
    line = line.strip()
    try:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            row = [el['id'], ]
            for k in votes_things:
                row.append(clean(el.get(k, '')))
            votes.writerow(row)
            if el.get('postid'):
                votes_posts_rel.writerow([el['postid'], el['id']])
            if el.get('userid'):
                votes_users_rel.writerow([el['userid'], el['id']])
    except Exception as e:
        print('x', e)
    if i % 100000 == 0:
        print('.', end='')

print(i, 'votes ok')

file = join(PATH, 'Comments.xml')

for i, line in enumerate(open(file, encoding='utf-8')):
    line = line.strip()
    try:
        if line.startswith("<row"):
            el = xmltodict.parse(line)['row']
            el = replace_keys(el)
            row = [el['id'], ]
            for k in comments_things:
                row.append(clean(el.get(k, '')))
            comments.writerow(row)
            if el.get('postid'):
                comments_posts_rel.writerow([el['postid'], el['id']])
            if el.get('userid'):
                comments_users_rel.writerow([el['userid'], el['id']])
    except Exception as e:
        print('x', e)
    if i % 100000 == 0:
        print('.', end='')

print(i, 'comments ok')
