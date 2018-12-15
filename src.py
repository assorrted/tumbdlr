import pytumblr
import requests
import os

keys = open('keys.txt', 'r')
consumer_key = keys.readline()[:-1]
consumer_secret = keys.readline()[:-1]
oauth_token = keys.readline()[:-1]
oauth_secret = keys.readline()[:-1]
client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)

# Make the request
likes = client.likes()
count = likes['liked_count']
print('Found {} liked posts'.format(count))
img_urls = []
video_urls = []
post_urls = []
fimgs = open('image_urls.txt', 'a')
fvids = open('video_urls.txt', 'a')
fpost = open('post_urls.txt', 'a')
offset = 0
i = 0
count = 50
while i < count:
    posts = client.likes(limit=100, offset=offset)
    posts = posts['liked_posts']

    for post in posts:
        post_urls += [post['post_url']]
        fpost.write(str((post_urls[-1]+'\n').encode()))
        i += 1
        if i % 50 == 0:
            print(i)
        if post['type'] == 'video':
            try:
                video_urls += [post['video_url']]
                fvids.write(video_urls[-1]+'\n')
                url = video_urls[-1]
                r = requests.get(url)
                with open('vids/'+url.split('com/')[1], 'wb') as f:
                    f.write(r.content)

            except KeyError:
                print(post)
        elif post['type'] == 'photo':
            post_id = ''
            if len(post['photos']) > 1:
                post_id = str(post['id'])
                if not os.path.exists('pics/'+post_id):
                    os.makedirs('pics/' + post_id)
                post_id += '/'
            for pic in post['photos']:
                try:
                    url = pic['original_size']['url']
                    img_urls += [url]
                    fimgs.write(url+'\n')
                    r = requests.get(url)
                    with open('pics/'+post_id+url.split('/')[-1], 'wb') as f:
                        f.write(r.content)
                except KeyError:
                    print(post)

    offset += len(posts)

print(offset, i)

fvids.close()
fpost.close()
fimgs.close()
