# Command-Line Interface (CLI) Framework

BuildTools provides a framework for managing a complicated command-line interface that contains many layers of subcommands.
The code that wires up all of the CLI subcommands in BuildTools are the following:

* The `subcommands` package: The actual tools/scripts that are available in BuildTools.
* The `cli` package: provides the CLI Framework (via a Programmatic Interface) to create the BuildTools command-line interface.

> This document discusses the `subcommands` and `cli` package.
> Other 'support packages' are generally undocumented, or may be documented in the other [Software Design documentation](_overview.md).


## `subcommands` package

The `subcommands` package contains **ALL** of the details for the entire BuildTools CLI.
It contains all of the subcommand names, the help messages, and the actual 'main' functionality as well!
In specific, the following **three key details** are captured in this package:

* The `args` associated with each distinct subcommand.
* The `main(args)` function, associated with each distinct subcommand.
* The `help` messages that are associated with each layer of the subcommand.

### `subcommands` package conventions

We use a set of conventions in order to enable the full CLI framework.
These conventions are *quite restrictive*, but without them it would be very difficult to combine all of the subcommands into a single, cohesive 'command-line interface.'

The `subcommands` package follows these conventions to convey its **three key details**:

* Each sub-package within subcommands MUST contain a docstring describing that subcommand-layer.
    * e.g. `subcommands/example/__init__.py` should have a docstring like the following `"""Example subcommands."""`
* All distinct `*.py` modules MUST implement:
    * A `main(args)` function.
    * A module-docstring, describing the `main` functionality.
* Additionally, all distinct `*.py` modules MAY implement:
    * A `config_parser(parser)` function.

### Let's examine an example...

Let's look at an example of how we would expose the following `example hello-world` subcommand via BuildTools:

    $ buildtools example hello-world
    Hello, World!

Let's start by looking at a *simple* example of what the `subcommands` package looks like and all the files within it:

    subcommands/
    ├── __init__.py   
    └── example
        ├── __init__.py
        └── hello_world.py

In this example `subcommands` package, there is a single `hello_world.py` file. That file looks something like the following:

*`subcommands/example/hello_world.py`*

    """Say 'Hello World' (example)."""
    import configargparse

    def config_parser(parser: configargparse.ArgParser):
        # Configure the `args` needed by `main(args)`
        parser.add_argument('--name', help="")

    def main(args: configargparse.Namespace):
        if args.name:
            print(f"Hello, {name}!")
        else:
            print("Hello, World!")
  
Given this package structure, and this `hello_world.py` module, the following functionality will be exposed by BuildTools:

    $ buildtools example hello-world
    Hello, World!
    $ buildtools example hello-world --name Fred
    Hello, Fred!

Further, the docstring provided in the module is provided via `--help`:

    $ buildtools example hello-world --help
        Say 'Hello World' (example).

But what about the `subcommands/example/__init__.py` file?
It MUST contain only a single docstring describing the `example` package! 
So, it will look something like the following:

*`subcommands/example/__init__.py`*

    """Example subcommands."""

Which will provide the 'help' string as appropriate, e.g.:

    $ buildtools example --help
      
    Example Subcommands.
        hello-world: Say 'Hello World' (example).


## `cli` package

Conceptually, at its core, `BuildTools` is a command-line interface (CLI) Framework.
That framework is implemented in the `buildtools.cli` package.

### `cli` Programming Interface

Interacting with the `cli` package happens through its programmatic interface.
The primary functions that are provided are the following:

* `register(package)`: Processes the '`subcommands` package'.
* `run(args)`: Execute the appropriate subcommand, per the the provided `args`.

    > Conceptually, `run(args)` is the entry-point for the whole application. 

> See exactly how the cli Programming Interface is used in `ntsbuildtools.main.py:main()` function.

### "Root" ArgumentParser

Behind the scenes, the `cli` package is implemented via a single `configargparse.ArgumentParser` object. 
We refer to it as 'the "Root" ArgParser.'

### `register(package)`: Constructing the Root ArgumentParser for BuildTools

The `ntsbuildtools.cli.register(package)` function is responsible for defining the Root ArgParser for the entire `buildtools` application.
This function uses Python introspection to inspect the well-structured, convention-based `subcommands` package.

This function relies on several details, that we go on to describe in this section:

* We need to handle the complexity around: `ArgumentParser` 'subparser action objects'.
* We need a Tree data structure, to hold the `ArgumentParser` objects (and the 'subparser action objects').
* We need an Algorithm for constructing the Tree.

### Core Concept: `ArgumentParser` 'subparser action objects'

Python's `ArgumentParser` has an interesting implementation detail when it comes to 'adding multiple subcommands to a parser': It provides a [special 'action object' to manage subcommands](https://docs.python.org/3/library/argparse.html#sub-commands).

Lets look at an example of how this works:

First, setup our `root_parser`:

    root_parser = ArgumentParser()

Then, later on, lets add a 'post' subcommand:

    action_object = root_parser.add_subparsers()
    post_parser = action_object.add_subparser("post")

Finally, lets add a 'get' subcommand to the `root_parser`:

    action_object = root_parser.add_subparsers()
    get_parser = action_object.add_subparser("get")

This second code block will not work, and will raise an error!

    : error: cannot have multiple subparser arguments

So, these ephemeral 'action objects' are a thorn in our side. 
Specifically, these objects are impeding the following functionality:

* *Add multiple subcommands to an ArgumentParser **from multiple scopes***

So, we need some way for to track the 'action object' alongside `root_parser` to enable 'adding subcommands from multiple scopes.'
This might be done by extending `ArgumentParser` with some `add_subcommand(str)` method.
Let's rewrite the example code blocks above assuming we have this new method -- we'll use the class name `SubcommandArgumentParser`.

    root_parser = SubcommandArgumentParser()

The Post parser...

    post_parser = root_parser.add_subcommand("post")

The Get parser...

    get_parser = root_parser.add_subcommand("get")

Unfortunately, a solution that extends `ArgumentParser` like this is quite difficult to implement due to some complications around the `add_subparsers()` method: 

* The 'action object' returned from `add_subparsers` will return an `ArgumentParser` object. It then needs to be turned into a `SubcommandArgumentParser` (if we want to build a whole tree of `SubcommandArgumentParsers`).
* Extending `ArgumentParser` with a method that calls `self.add_subparsers()` **raises a cryptic exception.**

So, it seems that using a tree data structure to maintain all of these pieces is a more appropriate.

### `ArgumentParser` Tree Data Structure

> Motivation: We need some way to manage the 'subparser action objects' (discussed above).

> Additional Motivation: An `ArgumentParser` with layers of subcommands ***is** a Tree data structure.*
> `ArgumentParser` does not contain ANY methods for traversing that tree.

`ArgumentParser` may inherently contain a 'subcommand Tree,' but it does not provide methods or attributes to operate on it.
For example, the following features are not available:

* List the 'child' subparsers (subcommands) associated to an ArgumentParser.
* Get the 'parent' parser associated to a subparser.

We can leverage the `anytree` Package to gain these core features!
Lets imagine some `ArgParserNode` Class to implement all the behaviors we might need.
So, what functionality does this tree need to support?

* Create a 'root' `ArgParserNode`, to represent this Tree. 
    * Implementation Note: It must hold a reference to the "Root ArgumentParser."
* Add multiple 'children' to an `ArgParserNode`.
    * Method signature: `add(subcommand: str, help: str = None) -> ArgParserNode`
    * Implementation Notes: 
        * *Return* the newly created child node (so that grandchildren can be easily added).
        * First time adding a child, *store the 'subparsers action object'* to enable adding future children!

Beyond that basic 'tree functionality', it'd be great to provide some more functionality for managing the underling Root ArgumentParser. 
Precisely, we also need functionality to consume the `main(args)` and the `config_parser(parser)` functions provided by each subcommand.
This functionality can be provided via a pair of methods that take a `Callable` parameter (i.e. a callback function).

* Enable 'setting the default function' for an `ArgParserNode`.
    * Method signature: `set_default_func(func: Callable)`
    * Implementation Notes:
        * Each subcommand has a `main(args)`
        * set_default_func should be invoked with the `main(args)` is the 'main' code that will execute.
* Enable 'configuring the internal `parser`'.
    * Method signature: `config_parser(config_parser: Callable[[ArgParser], None])`
    * Implementation Notes:
        * Each subcommand can provide a `config_parser(parser)` Callable to configure 

#### Example 1

Here is an example of how to use this `ArgParserNode` 'Tree data structure.'
Lets start with the simplest possible example -- adding a simple 'Hello, world!' functionality with the subcommand 'hello':

    import ntsbuildtools.cli.tree
    import configargparse

    #  Setup the "Root ArgParser" and the Tree data structure.
    _root_parser = configargparse.ArgumentParser()
    _tree_root = ntsbuildtools.cli.tree.ArgParserNode(parser=_root_parser)
    
    #  Create the core Callable that define the subcommand's functionality
    def main(args):
        print(f"Hello, {args.name}!")

    #  Add the subcommand to the CLI tree!
    hello_node = _tree_root.add('hello', "Just a simple 'Hello, World!' example subcommand.")
    hello_node.set_default_function(main)

    #  Parse arguments
    parsed_args = _root_parser.parse_args(['hello'])

    #  The default function `func` will be `main(args)` -- since the 'hello' argument was provided to parse_args
    parsed_args.func(parsed_args)

#### Example 2

This is a slightly more complicated example.
It is still a 'hello world' example, but it shows how to provide a `config_parser` Callable that establishes a `--name` argument:

    #  Setup the "Root ArgParser" and the Tree data structure.
    _root_parser = ArgumentParser()
    _tree_root = ArgParserNode(parser=_root_parser)
    
    #  Create the core Callables that define the subcommand's functionality
    def config_parser(parser):
        parser.add_argument('--name')

    def main(args):
        print(f"Hello, {args.name}!")

    #  Add the subcommand to the CLI tree!
    hello_node = _tree_root.add('hello', "Just a simple 'Hello, World!' example subcommand.")
    hello_node.config_parser(config_parser)
    hello_node.set_default_function(main)

    #  Parse arguments -- pass 'hello'
    parsed_args = _root_parser.parse_args(['hello', '--name', 'Fred'])

    #  The default function `func` will be `main(args)` -- since the 'hello' argument was provided to parse_args
    parsed_args.func(parsed_args)


### `register(parser)` Algorithm

With our `ArgParserNode` tree data structure, we can now reason about the actual algorithm for populating the "Root ArgumentParser".

This algorithm is based on a 'breadth-first tree walk' of the `subcommands` package.
Walking a tree is generally most intuitive using a recursive algorithm.

* `_root` is a root node
* For each **subpackage**, create an `ArgParserNode`.
    * The `subcommand` name MUST correspond to the package's name.
    * The `help` message MUST be pulled from the package's docstring.
* For each **module** (in a given subpackage), create an `ArgParserNode`.
    * The `subcommand` name MUST correspond to the module's name.
    * The `help` message MUST be pulled from the module's docstring.
    * The `main(args)` must  
      
