import mdfrag
import argparse


def main():
    args = parse_args()
    frags = None
    with open(args.src, 'r') as src_file:
        frags = mdfrag.split_markdown(src_file.read(), args.size)

    for count, fragment in enumerate(frags):
        with open(f'{args.dest}_{count}.md', 'w') as dest_file:
            dest_file.write(fragment)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'src',
        help='The file to be split into chunks.'        
    )
    parser.add_argument(
        'size', 
        type=int,
        help='Fragment the file into chunks smaller than this, in bytes.'
    )
    parser.add_argument(
        '--dest',
        default='out',
        help='Filename prefix to use for the generated fragments.'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
