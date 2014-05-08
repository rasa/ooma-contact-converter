ooma-contact-converter
======================

Convert Google contact export to Ooma import format (Outlook 2007 .CSV)

To use:

1. Install python, and make, if needed.

2. Clone the repo:
````
git clone git@github.com:rasa/ooma-contact-converter.git
````

3. Visit `https://mail.google.com/mail/u/0/#contacts`

4. Export your Google Contacts in "Google CSV format". Save the file with the .csv extension in the `ooma-contact-converter` directory.

5. Run:
````
$ cd ooma-contact-converter
$ make
````

6. Visit `https://my.ooma.com/contacts`

7. Select "More", "Import", and "Outlook 2007 CSV".

8. Click [Continue].

9. Click [Choose File], and select the file named `*.ooma.txt`

10. Click [Import].
