import pathlib,re,html
p=pathlib.Path(r'C:\lunwen\research_audit\topic_selection_2026_11_22'); s=(p/'wave_html.txt').read_text('utf-8');s=re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',s,flags=re.S);t=html.unescape(re.sub('<[^>]+>',' ',s));t=re.sub(r'\s+',' ',t);(p/'wave_full_clean.txt').write_text(t,'utf-8')
for word in ['Abstract','Conclusion','Limitations','benign','single-image fusion','indistinguishable','complementary','disjoint','fusion','Texas','Jul','Aug','github']:
 starts=[m.start() for m in re.finditer(re.escape(word),t,re.I)];print('\nTERM',word,'COUNT',len(starts))
 for i in (starts[-2:] if word in ['Conclusion','Limitations'] else starts[:3]):print(t[max(0,i-220):i+1300])
print('SOURCE LINKS',re.findall(r'href=["\']([^"\']*(?:github|zenodo|arxiv)[^"\']*)',s))
