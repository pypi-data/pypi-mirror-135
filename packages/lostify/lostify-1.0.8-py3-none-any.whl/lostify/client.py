# -*- coding: utf-8 -*-

import json
import aiohttp
import asyncio

class Spotify(object):
  def __init__(self, client_id, client_secret, aiohttp_session=None, access_token=None, redirect_uri=None):
    self.error_codes = (429, 500, 502, 503, 504)
    self.access_token = access_token
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri
    if isinstance(aiohttp_session, aiohttp.ClientSession):
      self.session = aiohttp_session
    else:
      self.session = aiohttp.ClientSession()
  
  async def close(self):
    await self.session.close()

  def json(self):
    data = {}
    if self.client_id:
      data['client_id'] = self.client_id
    if self.client_secret:
      data['client_secret'] = self.client_secret
    if self.redirect_uri:
      data['redirect_uri'] = self.redirect_uri
    return data
  
  async def send_request(self, method, endpoint, payload=None, **kwargs):
    json_data = self.json()
    authorization = {'Content-Type': 'application/json'}

    if payload:
      for item in payload:
        if payload[item] != None: json_data[item] = payload[item]
    if len(kwargs) != 0:
      for kwarg in kwargs:
        if kwargs[kwarg] != None: json_data[kwarg] = kwargs[kwarg]

    if self.access_token:
      authorization['Authorization'] = 'Bearer %s' % self.access_token

    for item in json_data:
      if '?' in endpoint:
        endpoint += '&%s=%s' % (item, json_data[item])
      else:
        endpoint += '?%s=%s' % (item, json_data[item])

    try: 
      json = kwargs['json']
    except: 
      json = None 
    response = await self.session.request(method, endpoint, headers=authorization, json=json)

    if response.status in self.error_codes:
      return False

    try:
      response_data = await response.json()
    except Exception as error:
      if 'Attempt' in str(error): return None
      else: return False

    return response_data
  

  def get_id(self, type, id):
    if id.startswith('https://open.spotify.com/track/'):
      return id.split('https://open.spotify.com/track/')[1].split('?si=')[0]
    fields = id.split(':')
    if len(fields) >= 3:
      if type != fields[-2]:
        return False
      return fields[-1].split('?')[0]
    fields = id.split('/')
    if len(fields) >= 3:
      itype = fields[-2]
      if type != itype:
        return fields[-1].split('?')[0]
    return id

  def get_uri(self, type, id):
    if self.is_uri(id):
      return id
    if id.startswith('https://open.spotify.com/track/'):
      return 'spotify:' + type + ':' + id.split('https://open.spotify.com/track/')[1].split('?si=')[0]
    else:
      return 'spotify:' + type + ':' + self.get_id(type, id)

  def is_uri(self, uri):
      return uri.startswith('spotify:') and len(uri.split(':')) == 3

  def append_device(self, path, device):
    if device:
      if '?' in path:
        path += '&device_id=%s' % device
      else:
        path += '?device_id=%s' % device

    return path

  async def get_token(self, code):
    payload = {
      'grant_type': 'authorization_code',
      'code': code
    }

    return await self.send_request('POST', 'https://accounts.spotify.com/api/token', payload)
  
  async def pause(self, device=None):
    url = self.append_device('https://api.spotify.com/v1/me/player/pause', device)
    
    return await self.send_request('PUT', url)
  
  async def resume(self, device=None):
    url = self.append_device('https://api.spotify.com/v1/me/player/play', device)
    
    return await self.send_request('PUT', url)

  async def skip(self, device=None):
    url = self.append_device('https://api.spotify.com/v1/me/player/next', device)
    
    return await self.send_request('POST', url)
  
  async def previous(self, device=None):
    url = self.append_device('https://api.spotify.com/v1/me/player/previous', device)
    
    return await self.send_request('POST', url)
  
  async def repeat(self, state, device=None):
    if not state in ('track', 'context', 'off'):
      return False

    url = self.append_device('https://api.spotify.com/v1/me/player/repeat?state=%s' % state, device)
    
    return await self.send_request('PUT', url)
  
  async def volume(self, percent, device=None):
    if not isinstance(percent, int):
      return False
    if percent < 0 or percent > 100:
      return False
    
    url = self.append_device('https://api.spotify.com/v1/me/player/volume?volume_percent=%s' % percent, device)
    
    return await self.send_request('PUT', url)

  async def shuffle(self, state, device=None):
    if not isinstance(state, bool):
      return False

    url = self.append_device('https://api.spotify.com/v1/me/player/shuffle?state=%s' % str(state).lower(), device)
    
    return await self.send_request('PUT', url)

  async def seek(self, position, device=None):
    if not isinstance(position, int):
      return False

    url = self.append_device('https://api.spotify.com/v1/me/player/seek?position_ms=%s' % position, device)
    
    return await self.send_request('PUT', url)

  async def heart(self, ids):
    items = []
    if ids != None:
      items = [self.get_id('track', i) for i in ids]
    return await self.send_request('PUT', 'https://api.spotify.com/v1/me/tracks', ids=','.join(items))

  async def unheart(self, ids):
    items = []
    if ids != None:
      items = [self.get_id('track', i) for i in ids]
    return await self.send_request('DELETE', 'https://api.spotify.com/v1/me/tracks', ids=','.join(items))

  async def hearted(self, ids):
    items = []
    if ids != None:
      items = [self.get_id('track', i) for i in ids]
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/tracks/contains', ids=','.join(items))

  async def search(self, query, limit=10, offset=0, type='track'):
    if not type in ('track', 'artist', 'album', 'playlist'):
      return False
    return await self.send_request('GET', 'https://api.spotify.com/v1/search', q=query, limit=limit, offset=offset, type=type)

  async def related_artists(self, id):
    id = self.get_id('artist', id)
    return await self.send_request('GET', 'https://api.spotify.com/v1/artists/%s/related-artists' % id)

  async def album(self, id):
    id = self.get_id('album', id)
    return await self.send_request('GET', 'https://api.spotify.com/v1/albums/%s' % id)

  async def albums(self, ids):
    items = []
    if ids != None:
      items = [self.get_id('album', i) for i in ids]
    return await self.send_request('GET', 'https://api.spotify.com/v1/albums', ids=','.join(items))

  async def album_tracks(self, id, limit=50, offset=0):
    id = self.get_id('album', id)
    return await self.send_request('GET', 'https://api.spotify.com/v1/albums/%s/tracks' % id, limit=limit, offset=offset)

  async def playlists(self, limit=50, offset=0):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/playlists', limit=limit, offset=offset)
  
  async def playlist(self, id, types=('track')):
    id = self.get_id('playlist', id)
    return await self.send_request('GET', 'https://api.spotify.com/v1/playlists/%s' % id, types=','.join(types))

  async def playlist_add(self, id, items, position=None):
    id = self.get_id('playlist', id)
    items = [self.get_uri('track', i) for i in items]
    return await self.send_request('POST', 'https://api.spotify.com/v1/playlists/%s/tracks' % id, uris=','.join(items), position=position)

  async def playlist_remove(self, id, items):
    id = self.get_id('playlist', id)
    items = [self.get_uri('track', i) for i in items]
    data = dict(tracks=[{'uri': i} for i in items])
    return await self.send_request('DELETE', 'https://api.spotify.com/v1/playlists/%s/tracks' % id, json=data)

  async def queue(self, track, device=None):
    uri = self.get_uri('track', track)

    url = self.append_device('https://api.spotify.com/v1/me/player/queue?uri=%s' % uri, device)
    
    return await self.send_request('POST', url)
    
  async def user(self):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/')
  
  async def playing_track(self):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/player/currently-playing')

  async def current(self):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/player')

  async def followed_artists(self, limit=10, after=None):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/following', type='artist', limit=limit, after=after)


  async def following_artists(self, ids=None):
    items = []
    if ids != None:
      items = [self.get_id('artist', i) for i in ids]
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/following/contains', type='artist', ids=','.join(items))

  async def following_users(self, ids=None):
    items = []
    if ids != None:
      items = [self.get_id('user', i) for i in ids]
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/following/contains', type='user', ids=','.join(items))

  async def recent(self, limit=10):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/player/recently-played', limit=limit)

  async def saved(self, limit=10, offset=0):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/tracks', limit=limit, offset=offset)

  async def devices(self):
    return await self.send_request('GET', 'https://api.spotify.com/v1/me/player/devices')

  async def swap_device(self, device):
    data = dict(device_ids=[device])
    return await self.send_request('PUT', 'https://api.spotify.com/v1/me/player', json=data)
