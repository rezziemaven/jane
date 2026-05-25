import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # for node in old_nodes:
    #     if node.text_type != TextType.TEXT:
    #         new_nodes.append(node)
    #         continue
    #     if node.text.count(delimiter) % 2 != 0:
    #         raise Exception("Invalid Markdown syntax")
    #     split_text = node.text.split(delimiter)
    #     for text in split_text:
    #         if len(text) == 0:
    #             continue
    #         if text.startswith(" ") or text.endswith(" "):
    #             new_nodes.append(TextNode(text, TextType.TEXT))
    #         else:
    #             new_nodes.append(TextNode(text, text_type))
    # return new_nodes
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
