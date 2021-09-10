import xml.etree.ElementTree as ET
import argparse
import os
import json


def latex_header():
  return f'''\\documentclass[10pt,a4paper,oneside]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}
\\usepackage{{longtable}}
\\usepackage[
  left=1.5cm,
  right=1.5cm,
  top=2cm,
  bottom=2cm,
  %includeheadfoot
]{{geometry}}
\\renewcommand{{\\familydefault}}{{\\sfdefault}}

\\usepackage{{titling}}
\\pretitle{{\\begin{{center}}\\Huge\\bfseries}}
\\posttitle{{\\par\end{{center}}\\vskip 0.5em}}
\\preauthor{{\\begin{{center}}\\Large}}
\\postauthor{{\\end{{center}}}}
\\setlength{{\\droptitle}}{{-8em}}

\\title{{Nennliste}}
\\author{{{TITLE}}}


\\begin{{document}}

\\maketitle
\n'''

class Category:
  def __init__(self, id, name, gender, year_min, year_max):
    self.id = id
    self.name = name
    self.gender = gender
    self.year_min = year_min
    self.year_max = year_max
  
  def __str__(self) -> str:
    return f'Category {self.id}, {self.name}'
    
class Athlete:
  def __init__(self, code, firstname, lastname, gender, birthdate, club, division, category, nc) -> None:
      self.code = code
      self.firstname = firstname
      self.lastname = lastname
      self.gender = gender
      self.birthyear = birthdate[0:4]
      self.club = club
      self.division = division
      self.category = category
      self.nc = nc
      self.comment = ""
  
  def __str__(self) -> str:
    return f'{self.code}, {self.firstname} {self.lastname}, {self.birthyear}'
  
  def to_row(self):
    if self.nc == "true":
      nc = "x"
    else:
      nc = "-"
    return f'{self.code} & {self.lastname} {self.firstname} & {self.birthyear} & {self.club} & {nc} & {self.comment} \\\\ \\hline \n'
def main():
  print("python main function")
  entries_tree = ET.parse(opt.xml)
  entries_root = entries_tree.getroot()
  print(entries_root)
  global TITLE
  TITLE = entries_root.find("RaceInfo").find("Title").text
  CATEGORIES = []
  for category in entries_root.find("Categories").findall("Category"):
    #print(category.find("Category").text)
    temp = Category(int(category.find("CategoryID").text),
      category.find("Category").text,
      category.find("Gender").text,
      int(category.find("BirthyearMin").text),
      int(category.find("BirthyearMax").text))
    CATEGORIES.append(temp)
  
  FORMS = []
  
  for entry_form in entries_root.find("EntryForms").findall("EntryForm"):
    athletes = []
    for athlete in entry_form.find("Entries").findall("Entry"):
      temp = Athlete(int(athlete.find("NSACode").text),
        athlete.find("Firstname").text,
        athlete.find("Lastname").text,
        athlete.find("Gender").text,
        athlete.find("Birthdate").text,
        athlete.find("Club").text,
        athlete.find("Division").text,
        athlete.find("CategoryID").text,
        athlete.find("IsNC").text        
      )
      if athlete.find("Comment") is not None:
        temp.comment = athlete.find("Comment").text
      athletes.append(temp)
    #for athlete in athletes:
    #  print(athlete)
    FORMS.append(athletes)
  
  
  with open(opt.out, "w+") as f:
    f.write(latex_header())
    f.write
    f.write('\\begin{longtable}{| c | p{4cm} | c | p{4cm} | c | p{5cm} |}\n\\hline\n')
    f.write('\\textbf{ÖSV Nr.} & \\textbf{Name} & \\textbf{Jahr} & \\textbf{Verein} & \\textbf{NK} & \\textbf{Kommentar} \\\\ \\hline\n \\endhead')
    for form in FORMS:
      for athlete in form:
        f.write(athlete.to_row())
    f.write('\\end{longtable}\n\\end{document}')

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--xml', type=str, default="nennung.xml", help="Path to entries.xml")
  parser.add_argument('--out', type=str, default="./out.tex", help="Where to save data")
  opt = parser.parse_args()
  if not os.access(os.path.dirname(opt.out), os.W_OK):
    print("ERROR: Output directory not writable")

  print(f"Path to Entries: {opt.xml}")
  opt.xml = os.path.abspath(opt.xml)
  main()