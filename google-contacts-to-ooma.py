from __future__ import print_function

import sys
import csv

def warning(*objs):
  print("WARNING:", *objs, file=sys.stderr)

def error(*objs):
  print("ERROR:", *objs, file=sys.stderr)

def fatal(*objs):
  print("FATAL:", *objs, file=sys.stderr)
  sys.exit(1)

if len(sys.argv) != 3:
  sys.exit("Usage: " + sys.argv[0] + " input.csv output.txt")

infile = sys.argv[1]
outfile = sys.argv[2]

# fields in ooma contact export csv file
ofields = [
  "Title",
  "First Name",
  "Middle Name",
  "Last Name",
  "Suffix",
  "Company",
  "Department",
  "Job",
  "Title (duplicate)",
  "Business Street",
  "Business Street 2",
  "Business Street 3",
  "Business City",
  "Business State",
  "Business Postal Code",
  "Business Country/Region",
  "Home Street",
  "Home Street 2",
  "Home Street 3",
  "Home City",
  "Home State",
  "Home Postal Code",
  "Home Country/Region",
  "Other Street",
  "Other Street 2",
  "Other Street 3",
  "Other City",
  "Other State",
  "Other Postal Code",
  "Other Country/Region",
  "Assistant's Phone",
  "Business Fax",
  "Business Phone",
  "Business Phone 2",
  "Callback",
  "Car Phone",
  "Company Main Phone",
  "Home Fax",
  "Home Phone",
  "Home Phone 2",
  "ISDN",
  "Mobile Phone",
  "Other Fax",
  "Other Phone",
  "Pager",
  "Primary Phone",
  "Radio Phone",
  "TTY/TDD Phone",
  "Telex",
  "Account",
  "Anniversary",
  "Assistant's Name",
  "Billing Information",
  "Birthday",
  "Business Address PO Box",
  "Categories",
  "Children",
  "Directory Server",
  "E-mail Address",
  "E-mail Type",
  "E-mail Display Name",
  "E-mail 2 Address",
  "E-mail 2 Type",
  "E-mail 2 Display Name",
  "E-mail 3 Address",
  "E-mail 3 Type",
  "E-mail 3 Display Name",
  "Gender",
  "Government ID Number",
  "Hobby",
  "Home Address PO Box",
  "Initials",
  "Internet Free Busy",
  "Keywords",
  "Language",
  "Location",
  "Manager's Name",
  "Mileage",
  "Notes",
  "Office Location",
  "Organizational ID Number",
  "Other Address PO Box",
  "Priority",
  "Private",
  "Profession",
  "Referred By",
  "Sensitivity",
  "Spouse",
  "User 1",
  "User 2",
  "User 3",
  "User 4",
  "Web Page",
]

omap = {}

# map of field name to index number in output array
for k, v in enumerate(ofields):
  omap[v] = k

otitle_index = omap['Title']
ofirst_index = omap['First Name']
olast_index = omap['Last Name']

# map of google field name to ooma output field name
go_map = {
  'Name': 'Title',
  'Given Name': 'First Name',
  'Family Name': 'Last Name',
  'Organization 1 - Name': 'Company',
}

# map of google phone type value to ooma output field name
gtype_map = {
'Custom': 'Other Phone',
'Google Voice': 'Other Phone',
'Home Fax': 'Other Fax',
'Home': 'Home Phone',
'Main':   "Primary Phone",
'Mobile': 'Mobile Phone',
'Other': 'Other Phone',
'Pager': 'Pager',
'Work Fax': 'Business Fax',
'Work': 'Business Phone',
}

out = '"' + '","'.join(ofields) + '"' + "\n"

gmap = {}

header = False
line_no = 0
with open(infile, 'rb') as csvfile:
  csvreader = csv.reader(csvfile)
  for row in csvreader:
    line_no = line_no + 1
    if not header:
      gfields = row
      for k, v in enumerate(gfields):
        gmap[v] = k
      header = True
      continue
    output = [''] * len(ofields)

    for gname, oname in go_map.items():
      if not gmap.has_key(gname):
        fatal(infile, ': does not contain field', '"' + gname + '"')

      gindex = gmap[gname]
      oindex = omap[oname]
      output[oindex] = row[gindex]

    if output[ofirst_index] == ''  and output[olast_index] == '':
      if not gmap.has_key('Organization 1 - Name'):
        fatal(infile, ': does not contain field "Organization 1 - Name"')

      gindex = gmap["Organization 1 - Name"]
      company = row[gindex]

      if output[otitle_index] == '':
        output[otitle_index] = company

      parts = company.split(' ')

      first = ''
      last = ''
      for part in parts:
        if first > '':
          sp = ' '
        else:
          sp = ''
        if len(first) + len(part) + len(sp) <= 15:
          first = first + sp + part
        else:
          if last > '':
            sp = ' '
          else:
            sp = ''
          last = last + sp + part

      output[ofirst_index] = first
      output[olast_index] = last

    phones_found = 0

    for no in range(1, 20):
      gtype_name = 'Phone %d - Type' % (no)
      if not gmap.has_key(gtype_name):
        break
      gvalue_name = 'Phone %d - Value' % (no)
      if not gmap.has_key(gvalue_name):
        error(infile, ': line', line_no, ': phone', no, ': does not contain field: ', '"' + gvalue_name + '":', output[0])
        continue

      gtype_index = gmap[gtype_name]
      gvalue_index = gmap[gvalue_name]

      field = row[gvalue_index].strip()

      if field == '':
        continue

      gtype = row[gtype_index]
      if gtype_map.has_key(gtype):
        ofield = gtype_map[gtype]
      else:
        error(infile, ': line', line_no, ': phone', no, ': unknown phone type:', '"' + gtype + '", using "Other Phone":', output[0])
        ofield = 'Other Phone'

      phones = field.split(':::')
      # @todo process other phone numbers?

      phone0 = phones[0].strip()

      new = ''

      if phone0[0:2] == '+1':
        phone0 = phone0[2:]

      for c in phone0:
        if len(new) == 0 and c == '+':
          new += c
          continue

        if '0123456789'.find(c) >= 0:
          new += c
          continue
        if "-().".find(c) >= 0:
          continue
        if " \t".find(c) >= 0:
          continue
        if len(new) > 10:
          break;

      if len(new) == 0:
        warning(infile, ': line', line_no, ': phone', no, gtype, ': no phone number found:', output[0])
        continue

      oindex = omap[ofield]
      if phones_found < 4:
        output[oindex] = new
      else:
        error(infile, ': line', line_no, ': phone', no, gtype, new, ': ignoring number, as Ooma has a 4 phone number limit:', output[0])

      phones_found += 1

    if phones_found == 0:
      continue

    out += '"' + ('","'.join(output)) + '"' + "\n"

with open(outfile, 'wb') as fp:
  fp.write(out)
