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
