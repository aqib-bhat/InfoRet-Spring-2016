from html.parser import HTMLParser
import os
import xml.etree.ElementTree as xtree
import xml.etree.cElementTree as ET
import lxml



tree_all = xtree.parse('enwiki-20160204-pages-articles1.xml-p000000010p000030302')

print(tree_all.getroot())

out = tree_all.findall('{http://www.mediawiki.org/xml/export-0.10/}page')
print(len(out))

#print(((out[0].find('{http://www.mediawiki.org/xml/export-0.10/}revision')).find('{http://www.mediawiki.org/xml/export-0.10/}text')).text)

def find_next_marker(s, section_marker, possible_char):
    index = s.find(section_marker)
    while (index + len(section_marker) < len(s) and s[index+len(section_marker)] == possible_char) or (index - len(section_marker) > -len(s) and s[index-len(section_marker):index] == section_marker):
        if index == -1: return -1
        index = s[index+len(section_marker):].find(section_marker) + index+len(section_marker)
    return index

def add_marker(s, section_marker, spl_char, possible_char):
	#print(section_marker)

	if section_marker == "======":return s
	cur_first_index = s.find(section_marker)
	while cur_first_index + len(section_marker)< len(s) and cur_first_index > -1:
		
		if s[cur_first_index+len(section_marker)] != possible_char and s[cur_first_index-len(section_marker):cur_first_index] != section_marker and \
						'\n' not in s[cur_first_index+len(section_marker):cur_first_index+len(section_marker)+2] \
				and s[cur_first_index:cur_first_index+len(section_marker)] == section_marker and s[cur_first_index+len(section_marker): cur_first_index+len(section_marker)+len(spl_char)]!= spl_char:

			
			cur_last_index = s[cur_first_index+len(section_marker):].find(section_marker)+cur_first_index+len(section_marker)
			s= s[:cur_first_index+len(section_marker)]+spl_char+s[cur_first_index+len(section_marker):]
			cur_last_index += len(spl_char)


			cur_first_index = find_next_marker(s[cur_last_index+len(section_marker):], section_marker, possible_char) + cur_last_index + len(section_marker)

			if cur_first_index != -1:
				new_text = add_marker(s[cur_last_index+len(section_marker):cur_first_index], section_marker+possible_char, spl_char, possible_char)
				s = s[:cur_last_index+len(section_marker)] + new_text + s[cur_first_index:]

		else:
			cur_first_index = cur_first_index + len(section_marker)
			cur_first_index += s[cur_first_index:].find(section_marker)
	return s

count=0
i = 0
while i < len(out):
	if len(out[i].findall('{http://www.mediawiki.org/xml/export-0.10/}redirect')) == 0:
	"""
		page1 = os.path.join('./target_folder'+str(count)+"doc"+"wiki_00.xml")
		old_text = ((out[i].find('{http://www.mediawiki.org/xml/export-0.10/}revision')).find('{http://www.mediawiki.org/xml/export-0.10/}text')).text
		text = add_marker(old_text, "==", "@@@@@", '=')
		((out[i].find('{http://www.mediawiki.org/xml/export-0.10/}revision')).find('{http://www.mediawiki.org/xml/export-0.10/}text')).text = text
		#tree = xtree.ElementTree(out[i])		
		#tree.write(page1)
		count += 1
		#break
	"""
	
	if i%1000 == 0: print(i)
	i += 1

tree_all.write('dump2.xml')



tree_all.write('dump2.xml', xml_declaration=True)
with open("dump2.xml", "r") as infile, open("output.xml", "w") as outfile:
    data = infile.read()
    data = data.replace("ns0:", "")
    outfile.write(data)
    infile.close()
    outfile.close()
    

