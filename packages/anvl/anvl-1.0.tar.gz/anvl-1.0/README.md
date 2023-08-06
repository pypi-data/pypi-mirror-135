# anvl

`anvl` is a Python module designed to serialize and deserialize of 
[A Name-Value Language](https://tools.ietf.org/search/draft-kunze-anvl-02).

## Usage

To decode an ANVL file: `anvl.load(file_name)`. This returns a list of
dictionaries.

To decode an ANVL string: `anvl.loads(anvl_string)`. This returns a list of
dictionaries.

To encode an ANVL file: `anvl.dump(list_of_dict, file_name)`.

To encode an ANVL string: `anvl.dumps(list_of_dict)`. Th`is returns an ANVL
string.

Both dump and dumps can take additional arguments to specify the maximum line
width, the character or characters used for indenting wrapped lines, and the
line endings used. For example:
`anvl.dumps(list_of_dict, width=60, ident="    ", line_end="\n")`
The default line width is 80 characters. The default indentation is a tab
character. The default line ending is "\r\n".
