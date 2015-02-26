# ooma-contact-converter  [![Flattr this][flatter_png]][flatter]

Convert Google contact export to Ooma import format (Outlook 2007 .CSV).

## Usage

1. Install python, and make, if needed.

2. Clone the repo:
	````bash
	git clone git@github.com:rasa/ooma-contact-converter.git
	````

3. Visit `https://mail.google.com/mail/u/0/#contacts`

4. Export your Google Contacts in "Google CSV format". Save the file with the .csv extension in the `ooma-contact-converter` directory.

5. Run:
	````bash
	$ cd ooma-contact-converter
	$ make
	````

6. Visit `https://my.ooma.com/contacts`

7. Select "More", "Import", and "Outlook 2007 CSV".

8. Click [Continue].

9. Click [Choose File], and select the file named `*.ooma.txt`

10. Click [Import].

## Contributing

To contribute to this project, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Bugs

To view existing bugs, or report a new bug, please see [issues](../../issues).

## Changelog

To view the version history for this project, please see [CHANGELOG.md](CHANGELOG.md).

## License

This project is [MIT licensed](LICENSE).

## Contact

This project was created and is maintained by [Ross Smith II][] [![endorse][endorse_png]][endorse]

Feedback, suggestions, and enhancements are welcome.

[Ross Smith II]: mailto:ross@smithii.com "ross@smithii.com"
[flatter]: https://flattr.com/submit/auto?user_id=rasa&url=https%3A%2F%2Fgithub.com%2Frasa%2Fooma-contact-converter
[flatter_png]: http://button.flattr.com/flattr-badge-large.png "Flattr this"
[endorse]: https://coderwall.com/rasa
[endorse_png]: https://api.coderwall.com/rasa/endorsecount.png "endorse"

