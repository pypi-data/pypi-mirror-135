import argparse
import functools
import glob
import logging
import re
import sys
import typing
import importlib.resources as pkg_resources

from lxml import etree


SchemaValidator = typing.Union[etree.DTD, etree.RelaxNG, etree.Schematron]


logger = logging.getLogger(__name__)


def validate(pathname: typing.AnyStr):
    """Validates given path against specified """
    files = glob.iglob(pathname, recursive=True)

    for file in files:
        errors = validate_file(file)
        if errors:
            print_errors(errors, file)


@functools.lru_cache
def load_validator() -> SchemaValidator:
    with pkg_resources.open_binary("schemas", "tei_all.rng") as f:
        return etree.RelaxNG(file=f)


def read_xml(filename: typing.AnyStr) -> etree.Element:
    with open(filename, "rb") as f:
        return etree.parse(f)


def is_tei(xml_root: etree.Element) -> bool:
    """Detects wether xml_root is part of a TEI file by matching the root tag"""
    matcher = tei_matcher()
    match = matcher.match(xml_root.tag)
    return match is not None


@functools.lru_cache
def tei_matcher() -> re.Pattern[typing.AnyStr]:
    """Compiles a regex pattern that can be used to find TEI tags"""
    return re.compile(r"{https?://www.tei-c.org/ns/1.0}/?tei", re.IGNORECASE)


def validate_file(file: typing.AnyStr) -> list:
    """Validates a single file by the schema given, returns a collection of errors"""
    try:
        xml_tree = read_xml(file)
        if not is_tei(xml_tree.getroot()):
            logger.debug(f"File '{file}' is skipped: 'No TEI detected'")
            return []

        validator = load_validator()
        if validator.validate(xml_tree):
            logger.debug(f"File '{file}' is valid.")
            return []

        return validator.error_log.filter_from_errors()
    except etree.XMLSyntaxError as e:
        return [e]


def print_errors(errors: typing.List[typing.AnyStr], file: typing.AnyStr):
    error_messages = "\n".join([f"- {error}" for error in errors])
    logger.error(f"File '{file}' has errors:\n{error_messages}")


def get_arguments():
    argparser = argparse.ArgumentParser(prog="tei-validator")
    argparser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="increases log level to debug",
    )
    argparser.add_argument(
        "--output",
        "-o",
        help="saves the log output to a file",
    )
    argparser.add_argument(
        "path",
        nargs="?",
        default="**/*.xml",
        help="path or glob expression",
    )
    return argparser.parse_args()


def cli():
    args = get_arguments()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.output:
        logger.addHandler(logging.FileHandler(filename=args.output, mode="w"))
        logger.addHandler(logging.StreamHandler(sys.stderr))

    validate(args.path)


if __name__ == "__main__":
    cli()
