# Markdown Fragmentation

It turns out that the matter of fragmenting a section of Markdown while maintaining the markdown syntax appropriately is quite difficult.
It seems like we need a full on "Markdown Parser" to determine how to do fragmentation.
We will leverage an existing markdown parser, mistletoe.

## Problem Statement

Why am I writing a document about "Markdown Fragmentation?"
We have to ensure that Markdown syntax are correct in each fragment, even when a fragment boundary falls in an inconvenient location.

As an example, imagine that a fragment just happens to end right in the middle of a long, 100 line code block -- we have to ensure that the result is correct!

    ```diff
    ... (A 100s of lines)...
                             <--- Fragment boundary
    ... (B 100s of lines)...
    ```

If we fragment this Markdown document naively at the "Fragment boundary", the results are the following two Fragments:

*`Fragment 1: missing end token (```)`*

    ```diff
    ... (A 100s of lines)...

*`Fragment 2: missing start token (```diff).`*

    ... (B 100s of lines)...
    ```

This does not work.
Honestly, if you render the first fragment, it will probably render just fine.
However, importantly, the second fragment would show the 'B 100s of lines' **without proper syntax.**
Instead, we want the following result if the fragment boundary falls in the middle of a code block.

*`Fragment 1: fixed!`*

    ```diff
    ... (A 100s of lines)...
    ```

*`Fragment 2: fixed!`*

    ```diff
    ... (B 100s of lines)...
    ```

### Reduce to a tree problem

Given that the provided markdown is parsed into a parse tree, we can start reasoning about the problem.
Conceptually, the parse tree can be described as a general tree data structure like the following:
  * The **root node** is the 'document' as a whole.
  * The **internal nodes** hold the structure of the Markdown document.
  * The **leaf nodes** hold the actual markdown content.
  
Given this tree data structure, we can see that fragmentation is really nothing more than slicing the tree.

> Maybe we should try to leverage some existing [Link/cut Tree data structure](https://en.wikipedia.org/wiki/Link/cut_tree)...?

In our case, slicing (fragmenting) the tree may happen at two levels:

* *At the __internal nodes__*: this is essentially traditional tree slicing -- splitting the tree into subtrees (e.g. see [Link/cut tree](https://en.wikipedia.org/wiki/Link/cut_tree)).
    > This corresponds to the discussion of `render_inner()` below.
* *In the __leaf nodes__*: this is actually an operation which slices half of a leaf in the tree.
  * This happens only when a piece of our markdown document is so big that it doesn't fit into a fragment.
  * In this case we need to essentially render the first half of the token (and mark the token as 'partially_rendered').
      > This corresponds to the discussion of `render()` below.

## Assumptions

1. Fragments must be larger than... "TBD" bytes.
   1. I.e. Fragments **must** be large enough to contain *any* valid Markdown *token/syntax-marker*.
2. If a markdown token must be split between multiple fragments, it will be split in the middle.
3. The fragmented Markdown must maintain the syntax from the original document.

## Mistletoe foundational knowledge

This solution for markdown fragmentation leverages an existing markdown parser, [Mistletoe](https://github.com/miyuchina/mistletoe).
Some of the reasons we use Mistletoe: it is performative, simple to extend, and has a standard project configuration (requirements.txt).

In the remainder of this section, we discuss some core features of the Mistletoe project that we use for markdown fragmentation.

### Primary methods: `render` and `render_inner`

It is clear that `render_inner(self, token)` and `render(self, token)` methods are key to the rendering-recursion.
The render() method is the main entry point for the rendering algorithm also.

#### Discussion of `render(self, token)`

When we investigate the `render` method, we see that it is doing nothing more than calling the appropriate `render_xyz` method...
It turns out that the `render` method is no more than a very simple shim (that enables a simple polymorphism hack).
See the code example below that shows effectively what the 'render' method is doing.

    def render(self, token):
      render_map = {
            'Paragraph':      self.render_paragraph,
            'CodeFence':      self.render_block_code,
            # ... some lines omitted for brevity...
            'LineBreak':      self.render_line_break,
            'Document':       self.render_document,
            }
      # E.g. assume the token is a 'paragraph' --> this will call `self.render_paragraph(token)`
      return render_map[token.__class__.__name__](token)

> The `render` method is also the traditional "entry point" for rendering -- but we use the custom 'split' method as our algorithm "entry point" instead (discussed below).

#### Discussion of `render_xyz(self,token)` methods

There are a collection of "render methods" that are actually specified in the `render_map` attribute of the `mistletoe.base_renderer.BaseRenderer` class.
For example, `render_paragraph` is one such method, as well as `render_raw_text`.
These methods are performing the real work of *rendering markdown*.
The `render_xyz` methods are implemented very simply in our renderer -- they render the markdown using the markdown-tokens [suggested in Bitbucket's "Markdown syntax gyide."](https://confluence.atlassian.com/bitbucketserver/markdown-syntax-guide-776639995.html)

#### Discussion of `render_inner(self, token)`

When we look at `render_inner`, this seems to be a location where we can easily 'split tokens'.
Tokens are full of children in many cases -- splitting token into their children is effectively splitting the tree at the 

Each level of the recursion tree produced by running the 'render' method results in calls many calls to 'render' and 'render_inner'.

Example Markdown:

      Below is some random code block.
      ```diff
      - Testing 123
      + Testing 1234
      - Testing 234
      + Testing 2345
      ```

AST for Example Markdown:

    {
      "type": "Document",
      "children": [
        {
          "type": "Paragraph",
          "children": [
            {
              "type": "RawText",
              "content": "Below is some random code block."
            }
          ]
        },
        {
          "type": "CodeFence",
          "language": "diff",
          "children": [
            {
              "type": "RawText",
              "content": "- Testing 123\n+ Testing 1234\n- Testing 234\n+ Testing 2345\n"
            }
          ]
        }
      ]
    }

Example render recursion call-tree for Example Markdown:

| Symbol | Meaning | 
|--------|--------|
| "R -> render_xyz"     | Call the `render()` method, which calls the render_xyz method. |
| "RI ->"    | Call the `renderInner()` method. |

- R -> render_document(token = the whole Document.)
  - RI
    - R -> render_paragraph(token = the Paragraph.)
      - RI
        - R -> render_raw_text(token = 'Below is some random code block.')
    - R -> render_block_code(token = the CodeFence.)
      - RI
        - R -> render_raw_text(token = "- Testing 123\n+ Testing 1234\n- Testing 234\n+ Testing 2345\n")

## Problem Solution foundational knowledge 

So, given this problem statement and a basic understanding of the mistletoe markdown parser, we can discuss the foundational theory, technologies, and concepts that are needed in this solution.

### Store Fragmentation-metadata on Tokens

Part of the solution will certainly include adding some arbitrary 'fragmentation-metadata' attributes to the tokens as needed while we are rendering them.
A simple example that will certainly be in the final solution: set `token.rendered = True` in the `render()` method (and checking for it using python's `hasattr` builtin method):

    def render(self, token):
        if hasattr(token, '_is_rendered'):  # *CHECK* _is_rendered
            return ''
        token._is_rendered = True  # *SET* _is_rendered
        return super().render(self, token)

> The code-example above will ensure that the 'super().render(self, token)' method is called only one time, even if 'render()' is called 1000 times. 

### User experience: provide a 'split()' method

Mistletoe offers a great user experience for rendering a markdown document.
However, our 'fragmentation' scenario does not have a clean user experience with the preexisting `render(token)` method -- the end-user will have to call `render` in a while loop and may even have to handle for FragmentationSizeErrors among other things.

Instead of kicking that to the user, the complexity of 'fragmented rendering' is handled by the `split(str)` method, which encapsulates all the logic discussed above (and even conveniently takes a simple `str` argument instead of a mistletoe `Token`).

## Possible Solution 1: Custom Exception Handling

Mistletoe is a recursive solution to Markdown rendering.
Effectively, mistletoe creates an abstract syntax tree (AST) of markdown tokens.
Then, with a tree of tokens in memory, the `render()` method recursively walks the AST, calling the `render` method on each child token, grandchild token, and so on.

If we want to interrupt the recursive rendering process, it can be done by simply raising an exception.
This is very easy to do, and will certainly have the desired effect of escaping out of the rendering process, which we like.
However, if we do this, then we certainly cannot depend on the standard tail-recursion rendering implementation  -- tail recursion relies on `return`ing the rendered tokens which will not happen if we throw an exception.

> I've spent some time on this possible solution, but switching from tail-recursion to head-recursion is not trivial.

## Possible Solution 2: Return Early

Another approach could be to simply set some boolean variable on the `renderer` when 'fragment_size_exceeded' has happened.
The approach of throwing an exception is nice in how it really does change the control flow immediately to walk up the recursion.
However, we could simply implement that logic ourselves with `return` statements.

    def render(self, token):
        super().render(token) # calls

> We should add the 'partial token' that has not been rendered to the exception -- then it can be pulled from the exception in the render() method and appended before returning.

