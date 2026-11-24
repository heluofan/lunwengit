import urllib.request,json
h={'Accept':'application/vnd.api+json','User-Agent':'Mozilla/5.0'}
for id in ['5ea8004476188b01cd912015','5ea80066e4f081019c077ab1','5ea8005276188b01c891033e']:
 u=f'https://api.osf.io/v2/nodes/mh9sj/files/osfstorage/{id}/';d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=h),timeout=30).read());print(id,[(x['id'],x['attributes']['name'],x['attributes']['kind']) for x in d['data'][:50]])
