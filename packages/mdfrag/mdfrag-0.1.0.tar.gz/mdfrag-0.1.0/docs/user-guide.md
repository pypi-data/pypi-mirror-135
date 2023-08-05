Have you ever wanted to break a Markdown document into chunks?
You are in luck, because that is what you can do with this package!

## Install

Install this package like any other PyPI package.

    pip install mdfrag

## Examples

This package can be invoked as a CLI tool, or used as a library in your own project.

### CLI Example

To split this document into chunks of 500 bytes, use the following CLI command:

    python -m mdfrag docs/user-guide.md 500 

> For more information, run `python -m mdfrag --help`. Additionally, see `__main__.py`.

### Code Example

Use the `mdfrag.split_markdown()` function to split your markdown document.

> See the docstring for more detailed information.
> Additionally, see `__main__.py` for an implementation of the below example.

    import mdfrag

    frags = None
    with open('docs/user-guide.md', 'r') as f:
        frags = mdfrag.split_markdown(f.read(), 512)

    # Walk through the list of fragments and write them to their appropriate files. 
    for count, fragment in enumerate(frags):
        with open(f'output_{count}.md', 'w') as dest:
            dest.write(fragment)

## Performance Considerations

If you select a small `fragment-size`, and your document contains large blocks of Markdown, the split_markdown function will struggle!
