import asyncio, re, pathlib, edge_tts
html=pathlib.Path('index.html').read_text()
async def main():
 for grade, rows in re.findall(r"(\d):\{title:'[^']+',rows:\[(.*?)\]\}",html):
  folder=pathlib.Path('audio')/grade
  folder.mkdir(parents=True,exist_ok=True)
  for i,row in enumerate(re.findall(r"'([^']+)'",rows)):
   words=row.replace('-','').split()
   for name,phrase in [(str(i),' '.join(words))]+[(f'{i}-{j}',w.rstrip(',.!?')) for j,w in enumerate(words)]:
    path=folder/(name+'.mp3')
    if path.exists() and path.stat().st_size>0: continue
    for attempt in range(4):
     try:
      await edge_tts.Communicate(phrase,'ms-MY-YasminNeural').save(str(path))
      break
     except Exception:
      if path.exists(): path.unlink()
      if attempt==3: raise
      await asyncio.sleep(3*(attempt+1))
asyncio.run(main())

import json
async def unit_audio():
 match=re.search(r'const unitVocabulary6=(\[.*?\]);',html,re.S)
 if not match: return
 groups=json.loads(match.group(1))
 folder=pathlib.Path('audio/6/units')
 folder.mkdir(parents=True,exist_ok=True)
 sem=asyncio.Semaphore(3)
 async def one(i,j,word):
  path=folder/f'{i}-{j}.mp3'
  if path.exists() and path.stat().st_size>0: return
  async with sem:
   for attempt in range(4):
    try:
     await edge_tts.Communicate(word,'ms-MY-YasminNeural').save(str(path))
     return
    except Exception:
     if path.exists(): path.unlink()
     if attempt==3: raise
     await asyncio.sleep(3*(attempt+1))
 await asyncio.gather(*(one(i,j,row[0]) for i,g in enumerate(groups) for j,row in enumerate(g['rows'])))
asyncio.run(unit_audio())

async def imlak_announcements():
 folder=pathlib.Path('audio/imlak-complete')
 folder.mkdir(parents=True,exist_ok=True)
 for n in list(range(1,31))+[621]:
  path=folder/f'{n}.mp3'
  if path.exists() and path.stat().st_size>0: continue
  for attempt in range(4):
   try:
    await edge_tts.Communicate(f'Tahniah! Murid telah menyelesaikan {n} daripada {n} soalan imlak.','ms-MY-YasminNeural',volume='+20%').save(str(path))
    break
   except Exception:
    if path.exists(): path.unlink()
    if attempt==3: raise
    await asyncio.sleep(3*(attempt+1))
asyncio.run(imlak_announcements())
