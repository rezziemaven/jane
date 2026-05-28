import re
from enum import Enum

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown syntax")
        split_text = re.split(
            rf"({re.escape(delimiter)}.*?{re.escape(delimiter)})", node.text
        )
        for text in split_text:
            if len(text) == 0:
                continue
            matches = re.findall(
                rf"{re.escape(delimiter)}(.*?){re.escape(delimiter)}", text
            )
            if len(matches) == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(matches[0], text_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if len(matches) == 0:
        return []
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    if len(matches) == 0:
        return []
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        for text in split_text:
            if len(text) == 0:
                continue
            matches = extract_markdown_images(text)
            if len(matches) == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(matches[0][0], TextType.IMAGE, matches[0][1]))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(?<!!)(\[.*?\]\(.*?\))", node.text)
        for text in split_text:
            if len(text) == 0:
                continue
            matches = extract_markdown_links(text)
            if len(matches) == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(matches[0][0], TextType.LINK, matches[0][1]))
    return new_nodes


def text_to_textnodes(text):
    delimiters = {
        "bold": "**",
        "italic": "_",
        "code": "`",
    }

    nodes = [TextNode(text, TextType.TEXT)]

    for type in TextType:
        old_nodes = nodes.copy()
        if type.value == "plain":
            continue
        elif type.value == "image":
            nodes = split_nodes_image(old_nodes)
        elif type.value == "link":
            nodes = split_nodes_link(old_nodes)
        else:
            delimiter = delimiters[type.value]
            nodes = split_nodes_delimiter(old_nodes, delimiter, type)
    return nodes


def markdown_to_blocks(markdown):
    return [text.strip() for text in markdown.split("\n\n") if len(text.strip()) != 0]


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"


def block_to_block_type(markdown_block):
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if markdown_block.startswith("```\n") and markdown_block.endswith("\n```"):
        return BlockType.CODE

    lines = markdown_block.split("\n")
    if all(
        (line.startswith((">", "> ")) and not line.startswith(" ", 2) for line in lines)
    ):
        return BlockType.QUOTE
    if all((line.startswith("- ") and not line.startswith(" ", 2) for line in lines)):
        return BlockType.UNORDERED
    if all(
        (
            lines[i].startswith(f"{i+1}. ") and not lines[i].startswith(" ", 3)
            for i in range(len(lines))
        )
    ):
        return BlockType.ORDERED
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED:
                children.append(list_to_html_node(block, BlockType.UNORDERED))
            case BlockType.ORDERED:
                children.append(list_to_html_node(block, BlockType.ORDERED))
            case BlockType.CODE:
                text = block.removeprefix("```\n").removesuffix("```")
                text_node = TextNode(text, TextType.CODE)
                code_node = text_node_to_html_node(text_node)
                children.append(ParentNode("pre", [code_node]))
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def list_to_html_node(list_block, block_type):
    list_children = []
    lines = list_block.split("\n")
    for line in lines:
        text = strip_list_marker(line, block_type)
        line_children = text_to_children(text)
        list_children.append(ParentNode("li", line_children))

    if block_type == BlockType.ORDERED:
        return ParentNode("ol", list_children)
    return ParentNode("ul", list_children)


def strip_list_marker(list_item, block_type):
    if block_type == BlockType.ORDERED:
        text = list_item.split(". ", 1)
        return text[1]
    return list_item.removeprefix("- ")


def paragraph_to_html_node(paragraph_block):
    lines = paragraph_block.split("\n")
    text = " ".join(lines)
    paragraph_children = text_to_children(text)
    return ParentNode("p", paragraph_children)


def get_heading_level(heading_block):
    if heading_block.startswith("# "):
        return "h1"
    if heading_block.startswith("## "):
        return "h2"
    if heading_block.startswith("### "):
        return "h3"
    if heading_block.startswith("#### "):
        return "h4"
    if heading_block.startswith("##### "):
        return "h5"
    if heading_block.startswith("###### "):
        return "h6"


def heading_to_html_node(heading):
    heading_level = get_heading_level(heading)
    text = re.split("#{1,6} ", heading, maxsplit=1)
    heading_children = text_to_children(text[1])
    return ParentNode(heading_level, heading_children)


def quote_to_html_node(quote_block):
    lines = quote_block.split("\n")
    for i in range(len(lines)):
        lines[i] = strip_quote_marker(lines[i])
    text = " ".join(lines)
    quote_children = text_to_children(text)
    return ParentNode("blockquote", quote_children)


def strip_quote_marker(quote_item):
    if quote_item.startswith("> "):
        return quote_item.removeprefix("> ")
    return quote_item.removeprefix(">")


def extract_title(markdown):
    # convert markdown to blocks
    blocks = markdown_to_blocks(markdown)
    # check if a block starts with '# '
    for block in blocks:
        if block.startswith("# "):
            # if it does, strip '# ' and return remaining text in block
            title = block.removeprefix("# ")
            return title

        # if doesn't, raise exception.
        raise Exception("No title found")
